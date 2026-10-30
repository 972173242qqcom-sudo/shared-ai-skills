#!/usr/bin/env python3
"""Inspect, size-budget encode, and verify transparent videos on macOS."""

import argparse
from bisect import bisect_right
import json
import math
import os
import platform
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
MACHINE = platform.machine().lower()
MACHINE = "arm64" if MACHINE in ("arm64", "aarch64") else MACHINE
BUNDLED_BIN_DIR = SCRIPT_DIR / "bin" / f"{sys.platform}-{MACHINE}"
NATIVE_CACHE = Path(os.environ.get(
    "PROCESS_TRANSPARENT_VIDEO_CACHE",
    str(Path(tempfile.gettempdir()) / "process-transparent-video-native"),
))


def tool(name: str) -> str:
    candidates = [
        str(BUNDLED_BIN_DIR / name),
        f"/opt/homebrew/bin/{name}",
        f"/usr/local/bin/{name}",
        shutil.which(name),
        str(Path.home() / ".local" / "bin" / name),
    ]
    for candidate in candidates:
        if candidate and Path(candidate).is_file():
            return candidate
    raise SystemExit(f"Missing required tool: {name}")


FFMPEG = tool("ffmpeg")
FFPROBE = tool("ffprobe")


def run(args, *, capture=False):
    return subprocess.run(args, check=True, text=True, capture_output=capture)


def is_quarantined(path: Path) -> bool:
    """Return whether macOS tagged a downloaded helper with Gatekeeper quarantine."""
    if sys.platform != "darwin":
        return False
    xattr = shutil.which("xattr") or "/usr/bin/xattr"
    if not Path(xattr).is_file():
        return False
    result = subprocess.run(
        [xattr, "-p", "com.apple.quarantine", str(path)],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return result.returncode == 0


def native_tool(name: str) -> Path:
    """Compile a bundled macOS Swift helper on demand and cache the binary."""
    bundled = BUNDLED_BIN_DIR / name
    if bundled.is_file() and os.access(bundled, os.X_OK) and not is_quarantined(bundled):
        return bundled
    source = SCRIPT_DIR / f"{name}.swift"
    if not source.is_file():
        raise SystemExit(f"Missing bundled native source: {source}")
    compiler = shutil.which("swiftc") or "/usr/bin/swiftc"
    if not Path(compiler).is_file():
        raise SystemExit("Missing swiftc. Install the Xcode Command Line Tools on macOS.")
    NATIVE_CACHE.mkdir(parents=True, exist_ok=True)
    binary = NATIVE_CACHE / name
    if not binary.is_file() or source.stat().st_mtime > binary.stat().st_mtime:
        module_cache = NATIVE_CACHE / "module-cache"
        module_cache.mkdir(parents=True, exist_ok=True)
        environment = os.environ.copy()
        environment["CLANG_MODULE_CACHE_PATH"] = str(module_cache)
        environment["SWIFT_MODULECACHE_PATH"] = str(module_cache)
        subprocess.run(
            [compiler, "-O", str(source), "-o", str(binary)],
            check=True,
            text=True,
            env=environment,
        )
    return binary


def native_verify(path: Path, output_dir: Path, *, dump_all=False):
    output_dir.mkdir(parents=True, exist_ok=True)
    environment = os.environ.copy()
    if dump_all:
        environment["DUMP_ALL_FRAMES"] = "1"
    return subprocess.run(
        [str(native_tool("verify_alpha")), str(path), str(output_dir)],
        text=True,
        capture_output=True,
        env=environment,
    )


def probe(path: Path) -> dict:
    result = run([
        FFPROBE, "-v", "error", "-show_streams", "-show_format", "-of", "json", str(path)
    ], capture=True)
    return json.loads(result.stdout)


def video_stream(info: dict) -> dict:
    return next(s for s in info["streams"] if s.get("codec_type") == "video")


def alpha_status(path: Path):
    command = [FFMPEG, "-hide_banner", "-loglevel", "error"]
    info = probe(path)
    stream = video_stream(info)
    if stream.get("codec_name") == "vp9" and stream.get("tags", {}).get("alpha_mode") == "1":
        command += ["-c:v", "libvpx-vp9"]
    command += ["-i", str(path), "-vf", "alphaextract", "-frames:v", "1", "-f", "null", "-"]
    if subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0:
        return "decoded"

    # FFmpeg commonly exposes Apple's HEVC-with-Alpha as ordinary yuv420p and
    # drops the auxiliary Alpha layer. Use the bundled AVFoundation verifier.
    if stream.get("codec_name") == "hevc":
        if sys.platform == "darwin":
            with tempfile.TemporaryDirectory(prefix="transparent-alpha-") as temp_dir:
                native = native_verify(path, Path(temp_dir))
                alpha_images = list(Path(temp_dir).glob("alpha_*.png"))
                zero_match = re.search(r"alpha_zero=(\d+)", native.stdout)
                if native.returncode == 0 and alpha_images and zero_match:
                    if int(zero_match.group(1)) > 0:
                        return "decoded-native"
        return "inconclusive-hevc-alpha"
    return "not-decoded"


def summary(path: Path) -> dict:
    info = probe(path)
    video = video_stream(info)
    audios = [s for s in info["streams"] if s.get("codec_type") == "audio"]
    fmt = info.get("format", {})
    duration = float(fmt.get("duration") or video.get("duration") or 0)
    size = int(fmt.get("size") or path.stat().st_size)
    return {
        "path": str(path.resolve()),
        "size_bytes": size,
        "size_mb_decimal": round(size / 1_000_000, 4),
        "duration_seconds": round(duration, 6),
        "width": video.get("width"),
        "height": video.get("height"),
        "fps": video.get("avg_frame_rate") or video.get("r_frame_rate"),
        "codec": video.get("codec_name"),
        "codec_tag": video.get("codec_tag_string"),
        "pixel_format": video.get("pix_fmt"),
        "audio_streams": len(audios),
        "alpha_status": alpha_status(path),
    }


def inspect_cmd(args):
    print(json.dumps(summary(Path(args.input)), ensure_ascii=False, indent=2))


def matte_cmd(args):
    if sys.platform != "darwin":
        raise SystemExit("Apple Vision foreground masking requires macOS.")
    source = Path(args.input)
    output = Path(args.output)
    if source.resolve() == output.resolve():
        raise SystemExit("Source and output must be different files")
    output.parent.mkdir(parents=True, exist_ok=True)
    environment = os.environ.copy()
    environment.update({
        "ALPHA_ERODE_RADIUS": str(args.erode_radius),
        "ALPHA_EDGE_CONTRAST": str(args.edge_contrast),
        "ALPHA_UNIFORM_EDGE_SIGMA": str(args.uniform_edge_sigma),
        "ALPHA_CONTOUR_SMOOTH_SIGMA": str(args.contour_smooth_sigma),
    })
    if args.preserve_premultiplied_edge_rgb:
        environment["PRESERVE_PREMULTIPLIED_EDGE_RGB"] = "1"
    if args.copy_audio:
        environment["COPY_AUDIO_IN_WRITER"] = "1"
    if args.hevc_alpha:
        environment["HEVC_ALPHA"] = "1"
    if args.repair_lower_left_product_zone:
        environment["REPAIR_LOWER_LEFT_PRODUCT_ZONE"] = "1"
    if args.precomputed_mask_dir:
        environment["PRECOMPUTED_MASK_DIR"] = str(Path(args.precomputed_mask_dir).resolve())
    subprocess.run(
        [str(native_tool("make_transparent")), str(source), str(output)],
        check=True,
        env=environment,
    )
    print(json.dumps(summary(output), ensure_ascii=False, indent=2))


def encode_cmd(args):
    source = Path(args.input)
    output = Path(args.output)
    if source.resolve() == output.resolve():
        raise SystemExit("Source and output must be different files")
    info = summary(source)
    duration = args.duration or info["duration_seconds"]
    if not math.isfinite(duration) or duration <= 0:
        raise SystemExit("Cannot determine a positive target duration")
    if info["alpha_status"] not in ("decoded", "decoded-native"):
        raise SystemExit("Input has no decodable Alpha; create a transparent master first")

    if info["alpha_status"] == "decoded-native":
        raise SystemExit("FFmpeg cannot decode this HEVC auxiliary Alpha. Decode a verified RGBA/ProRes master with the native helper before encoding.")
    command = [FFMPEG, "-hide_banner", "-y"]
    if info["codec"] == "vp9":
        command += ["-c:v", "libvpx-vp9"]
    command += ["-i", str(source)]
    command += ["-map", "0:v:0", "-map", "0:a?", "-map_metadata", "0"]
    source_frames = None
    if args.duration:
        counted = run([FFPROBE, "-v", "error", "-count_frames", "-select_streams", "v:0",
                       "-show_entries", "stream=nb_read_frames,duration", "-of", "json", str(source)], capture=True)
        stream = json.loads(counted.stdout)["streams"][0]
        source_frames = int(stream["nb_read_frames"])
        if source_frames <= 0:
            raise SystemExit("Source has no decoded frames")
        fps = source_frames / duration
        # Assign every decoded source frame a uniform timestamp; never truncate.
        command += ["-vf", f"settb=AVTB,setpts=round(N*1000000/({fps:.12f})),fps=fps={fps:.12f}:start_time=0:round=near",
                    "-r", f"{fps:.12f}", "-fps_mode", "cfr", "-frames:v", str(source_frames)]
        if info["audio_streams"]:
            source_duration = float(stream.get("duration") or info["duration_seconds"])
            if source_duration <= 0:
                raise SystemExit("Cannot determine audio retiming ratio")
            ratio = source_duration / duration
            factors = []
            while ratio > 2:
                factors.append(2); ratio /= 2
            while ratio < .5:
                factors.append(.5); ratio /= .5
            factors.append(ratio)
            tempo = ",".join(f"atempo={f:.12f}" for f in factors)
            command += ["-af", tempo + f",apad,atrim=duration={duration:.12f},asetpts=PTS-STARTPTS"]

    if args.format == "hevc-alpha":
        if not args.max_mb:
            video_kbps = args.video_kbps or 1200
        else:
            total_bits = args.max_mb * 1_000_000 * 8 * 0.97
            audio_kbps = args.audio_kbps if info["audio_streams"] else 0
            video_kbps = math.floor(total_bits / duration / 1000 - audio_kbps - 24)
            if video_kbps < 120:
                raise SystemExit("Size/duration budget is too small at the current audio and dimensions")
        command += [
            "-c:v", "hevc_videotoolbox", "-pix_fmt", "bgra", "-alpha_quality", str(args.alpha_quality),
            "-allow_sw", "1", "-b:v", f"{video_kbps}k", "-tag:v", "hvc1",
        ]
    elif args.format == "prores4444":
        command += [
            "-c:v", "prores_ks", "-profile:v", "4", "-pix_fmt", "yuva444p10le",
            "-alpha_bits", "8", "-q:v", str(args.prores_q), "-vendor", "apl0",
        ]
    else:
        command += [
            "-c:v", "libvpx-vp9", "-pix_fmt", "yuva420p", "-crf", str(args.vp9_crf),
            "-b:v", "0", "-deadline", "good", "-cpu-used", "4", "-row-mt", "1", "-auto-alt-ref", "0",
        ]

    if info["audio_streams"]:
        audio_codec = "libopus" if args.format == "vp9-alpha" else "aac"
        command += ["-c:a", audio_codec, "-b:a", f"{args.audio_kbps}k"]
    if output.suffix.lower() == ".mov":
        command += ["-movflags", "+faststart"]
    command += [str(output)]
    run(command)
    result = summary(output)
    if source_frames is not None:
        counted = run([FFPROBE, "-v", "error", "-count_frames", "-select_streams", "v:0",
                       "-show_entries", "stream=nb_read_frames", "-of", "json", str(output)], capture=True)
        result["decoded_frames"] = int(json.loads(counted.stdout)["streams"][0]["nb_read_frames"])
        if result["decoded_frames"] != source_frames or abs(result["duration_seconds"] - duration) > .05:
            raise SystemExit("Retiming frame-count/duration verification failed; output is only a candidate")
    if args.max_mb and result["size_bytes"] > args.max_mb * 1_000_000:
        raise SystemExit(f"Output exceeds ceiling: {result['size_bytes']} bytes > {int(args.max_mb * 1_000_000)}")
    print(json.dumps(result, ensure_ascii=False, indent=2))


def qc_frames(path: Path, qc_dir: Path):
    qc_dir.mkdir(parents=True, exist_ok=True)
    info = summary(path)
    colors = {"light": "edf8fc", "dark": "242424", "red": "d71920"}
    if info["codec"] == "hevc" and info["alpha_status"] == "decoded-native":
        native = native_verify(path, qc_dir)
        if native.returncode != 0:
            raise SystemExit(native.stderr or "Native HEVC Alpha QC failed")
        for rgba in sorted(qc_dir.glob("rgba_*.png")):
            suffix = rgba.stem.removeprefix("rgba_")
            for label, color in colors.items():
                out = qc_dir / f"{suffix}_{label}.png"
                graph = (
                    f"color=c=0x{color}:s={info['width']}x{info['height']}[bg];"
                    "[bg][0:v]overlay=format=auto"
                )
                run([FFMPEG, "-hide_banner", "-loglevel", "error", "-y", "-i", str(rgba),
                     "-filter_complex", graph, "-frames:v", "1", str(out)])
        return
    duration = info["duration_seconds"]
    try:
        fps_num, fps_den = (float(value) for value in str(info["fps"]).split("/", 1))
        frame_interval = fps_den / fps_num
    except (TypeError, ValueError, ZeroDivisionError):
        frame_interval = min(0.04, duration)
    last_frame_time = max(0, duration - frame_interval)
    times = sorted(set([duration * fraction for fraction in (0, .25, .5, .75)] + [last_frame_time]))
    with tempfile.TemporaryDirectory(prefix="transparent-gif-qc-") as temp_dir:
        decoded_gif_frames = []
        gif_starts = []
        if path.suffix.lower() == ".gif":
            pattern = Path(temp_dir) / "frame_%06d.png"
            run([FFMPEG, "-hide_banner", "-loglevel", "error", "-y", "-i", str(path),
                 "-fps_mode", "passthrough", str(pattern)])
            decoded_gif_frames = sorted(Path(temp_dir).glob("frame_*.png"))
            from PIL import Image
            with Image.open(path) as gif:
                elapsed = 0.0
                for frame_no in range(gif.n_frames):
                    gif.seek(frame_no)
                    gif_starts.append(elapsed)
                    delay = gif.info.get("duration", 0) / 1000
                    if delay <= 0:
                        raise SystemExit("GIF has missing/zero frame delay; resolve timing before QC")
                    elapsed += delay
            if len(gif_starts) != len(decoded_gif_frames):
                raise SystemExit("GIF decoder frame count differs from timing table")
            times = sorted(set([elapsed * fraction for fraction in (0, .25, .5, .75)] + [gif_starts[-1]]))

        for index, timestamp in enumerate(times):
            if decoded_gif_frames:
                frame_index = min(len(decoded_gif_frames) - 1, max(0, bisect_right(gif_starts, timestamp) - 1))
                source_args = ["-i", str(decoded_gif_frames[frame_index])]
                seek_args = []
            else:
                source_args = ["-i", str(path)]
                seek_args = ["-ss", str(timestamp)]
            alpha = qc_dir / f"{index:02d}_{timestamp:.3f}_alpha.png"
            run([FFMPEG, "-hide_banner", "-loglevel", "error", "-y", *source_args, *seek_args,
                 "-vf", "alphaextract", "-frames:v", "1", str(alpha)])
            for label, color in colors.items():
                out = qc_dir / f"{index:02d}_{timestamp:.3f}_{label}.png"
                graph = f"color=c=0x{color}:s={info['width']}x{info['height']}[bg];[bg][0:v]overlay=format=auto"
                run([FFMPEG, "-hide_banner", "-loglevel", "error", "-y", *source_args, *seek_args,
                     "-filter_complex", graph, "-frames:v", "1", str(out)])


def verify_cmd(args):
    path = Path(args.input)
    result = summary(path)
    failures = []
    if result["alpha_status"] == "not-decoded":
        failures.append("Alpha cannot be decoded")
    elif result["alpha_status"] == "inconclusive-hevc-alpha":
        failures.append("HEVC Alpha verification is inconclusive; rerun with AVFoundation access")
    if args.max_mb and result["size_bytes"] > args.max_mb * 1_000_000:
        failures.append("File exceeds maximum size")
    if args.duration and abs(result["duration_seconds"] - args.duration) > args.duration_tolerance:
        failures.append("Duration is outside tolerance")
    if args.qc_dir:
        qc_frames(path, Path(args.qc_dir))
        result["qc_dir"] = str(Path(args.qc_dir).resolve())
    result["verification"] = "PASS" if not failures else "FAIL"
    result["failures"] = failures
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if failures:
        raise SystemExit(2)


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser()
    sub = root.add_subparsers(dest="command", required=True)
    inspect_p = sub.add_parser("inspect")
    inspect_p.add_argument("input")
    inspect_p.set_defaults(func=inspect_cmd)

    matte = sub.add_parser("matte", help="Create a transparent master with Apple Vision on macOS")
    matte.add_argument("input")
    matte.add_argument("output")
    matte.add_argument("--erode-radius", type=float, default=0.0)
    matte.add_argument("--edge-contrast", type=float, default=1.0)
    matte.add_argument("--uniform-edge-sigma", type=float, default=0.0)
    matte.add_argument("--contour-smooth-sigma", type=float, default=0.0)
    matte.add_argument("--preserve-premultiplied-edge-rgb", action="store_true")
    matte.add_argument("--copy-audio", action="store_true")
    matte.add_argument("--hevc-alpha", action="store_true")
    matte.add_argument("--repair-lower-left-product-zone", action="store_true")
    matte.add_argument("--precomputed-mask-dir")
    matte.set_defaults(func=matte_cmd)

    encode = sub.add_parser("encode")
    encode.add_argument("input")
    encode.add_argument("output")
    encode.add_argument("--format", choices=("hevc-alpha", "prores4444", "vp9-alpha"), default="hevc-alpha")
    encode.add_argument("--duration", type=float)
    encode.add_argument("--max-mb", type=float)
    encode.add_argument("--video-kbps", type=int)
    encode.add_argument("--audio-kbps", type=int, default=64)
    encode.add_argument("--alpha-quality", type=float, default=.75)
    encode.add_argument("--prores-q", type=int, default=9)
    encode.add_argument("--vp9-crf", type=int, default=18)
    encode.set_defaults(func=encode_cmd)

    verify = sub.add_parser("verify")
    verify.add_argument("input")
    verify.add_argument("--max-mb", type=float)
    verify.add_argument("--duration", type=float)
    verify.add_argument("--duration-tolerance", type=float, default=.05)
    verify.add_argument("--qc-dir")
    verify.set_defaults(func=verify_cmd)
    return root


if __name__ == "__main__":
    arguments = parser().parse_args()
    arguments.func(arguments)
