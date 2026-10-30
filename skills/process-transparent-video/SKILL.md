---
name: process-transparent-video
description: Build and verify transparent-background video deliverables while controlling duration, dimensions, codec, compatibility, and file size. Use for background removal, Alpha preservation, transparent MOV, GIF, or raster-sequence Lottie export, complete-animation retiming, compression, format conversion, halo repair, or transparent-video quality control. Do not use for ordinary editorial cutting, captions, or color grading when transparency is not part of the task.
---

# 1. Skill Name

`process-transparent-video`

# 2. Version

V1.1 — 2026-10-30. Lottie delivery, GIF correctness, variable timing, and production QC.

# 3. Purpose

Turn an edited or generated source video into a delivery-ready transparent asset with explicit control over Alpha, full-animation timing, resolution, codec, compatibility, audio, and maximum file size. Preserve the source and a high-quality transparent master so later revisions do not compound losses.

The workflow is platform-neutral at the specification level. The bundled automatic semantic-matting backend uses Apple Vision on macOS; other environments may substitute an equivalent matte generator while keeping the same master, export, and verification contract.

# 4. Trigger / 什么时候使用

Use this Skill when the request includes background removal; Alpha creation, preservation, repair, or inspection; transparent MOV/GIF/PNG delivery; exact complete-animation retiming; strict file size; target-runtime compatibility; or diagnosis of halos, missing regions, matte-colored holes, GIF artifacts, or unstable contours.

# 5. Inputs

Required:

- source video or existing transparent animation;
- output format or target application;
- requested duration or instruction to preserve source timing;
- maximum file size when constrained.

Resolve or infer whether the full action must remain, whether audio must remain and be retimed, required dimensions/fps, current matte/Alpha state, and risk areas such as pale product, dark trim, logo, holes, fingers, shadows, glow, metal, or spill.

# 6. Outputs

Produce only requested outputs, normally a loss-minimized transparent master, target delivery file(s), machine-readable verification, and Alpha/composite QC images. Report absolute path, exact bytes and decimal MB, duration, decoded frame count, dimensions, fps/timestamps, codec, Alpha and audio status, and visual checks.

Never overwrite the source by default. Write to a new file or sibling delivery folder.

# 7. Dependencies / Tools

Core dependencies are Python 3.10+, FFmpeg/FFprobe with required codecs, `scripts/transparent_video.py`, and an image decoder that preserves GIF frame composition.

The bundled macOS backend uses AVFoundation, Core Image, Apple Vision, `scripts/make_transparent.swift`, `scripts/verify_alpha.swift`, precompiled Apple Silicon helpers or `swiftc`, and VideoToolbox-capable FFmpeg. Optional advanced repairs use Pillow/NumPy; strict GIF optimization may use `gifsicle`.

Run `bash scripts/setup_macos.sh` on a new Mac. Downloaded helpers may have Gatekeeper quarantine; the launcher detects this and compiles bundled Swift sources into a temporary cache when possible.

# Lottie and advanced GIF routing

Lottie is a first-class delivery format. For video/PNG input, read [Lottie workflow](references/lottie-workflow.md): export an explicitly labeled **raster-sequence Lottie**, not a vector animation. Use the lossless PNG exporter and source comparison verifier. If editable vectors are required, obtain vector/source animation assets or agree on reconstruction; wrapping video does not create vectors. Treat target-player testing as separate from structural/source validation.

For GIF compression, color or fade problems, read [GIF production rules](references/gif-production.md). For user-facing setup and reusable prompts, see [Tutorial](TUTORIAL.md) and [Prompts](PROMPTS.md).

# 8. Standard Workflow

1. **Inspect.** Run `python3 scripts/transparent_video.py inspect INPUT`. Record actual decoded frame count where timing matters; do not trust `r_frame_rate` alone. Inspect first/last frames, motion extremes, transitions, and reported defects.
2. **Classify.** Read `references/format-and-edge-guide.md`. Choose existing-Alpha transcode, constrained uniform-matte removal, semantic matte plus edge cleanup, connected-boundary matte removal, or protected local repair.
3. **Create a transparent master.** On macOS run `python3 scripts/transparent_video.py matte INPUT MASTER.mov`. Add only justified options such as `--erode-radius`, `--uniform-edge-sigma`, `--contour-smooth-sigma`, `--preserve-premultiplied-edge-rgb`, or `--precomputed-mask-dir`. Prefer ProRes 4444.
4. **Repair before delivery encoding.** Check missing subject regions, enclosed background, spill, halos, and temporal contours. Rebuild from source/master, not a compressed delivery.
5. **Set duration while preserving intent.** “Compress to 3 seconds” normally means preserve the full action and retime it. For `N` source frames and target duration `T`, assign uniform timestamps and use fps `N/T` when supported. Retime audio with the same ratio. Do not force back to source fps or append frame 0. With FFmpeg `setpts` + `-r` + CFR, cap with `-frames:v N`; verify frame count and timestamp deltas.
6. **Choose formats.** Include requested Lottie using the dedicated reference. Use the compatibility table. Generate MOV and GIF separately because their Alpha, cadence, palette, and size tradeoffs differ.
7. **Encode to budget.** Example: `python3 scripts/transparent_video.py encode MASTER.mov OUTPUT.mov --format hevc-alpha --duration 3 --max-mb 2`. Use decimal MB and leave 2–4% headroom.
8. **Verify.** Run `python3 scripts/transparent_video.py verify OUTPUT --duration 3 --max-mb 2 --qc-dir QC_DIR`. Review Alpha and composites over light, dark, and saturated backgrounds. Inspect every frame for short/risky clips.
9. **Deliver.** Confirm copies by SHA-256 when crossing folders and report compatibility caveats or quality concessions.

# 9. Core Rules

- Metadata is not proof of transparency. Decode Alpha and inspect composites.
- H.264 MP4 is not a transparent deliverable; use it only for opaque preview or baked background.
- Keep RGB zero where Alpha is zero. In partial Alpha, preserve correct premultiplied/straight semantics or reverse the matte.
- Never globally key a color also present in the product. Use connectivity, shape/location constraints, or tracked ROI.
- Erosion is last-mile cleanup; excess erosion removes structure, reflections, rings, and leading edges.
- Close only tiny false holes. Global filling can destroy real openings and animated rings.
- Preserve dark trim, pale logos, fingers, shadows, glow, reflections, and intentional translucency.
- Detect changing matte per frame and use one consistent edge-color rule after controlled inset/feather.
- Keep a high-quality master and generate each delivery independently.
- Prefer a tested FFmpeg build. One verified FFmpeg/VideoToolbox path produced HEVC Alpha that AVFoundation could not decode; FFmpeg 8.1.2 succeeded.
- An inconclusive HEVC Alpha check is neither PASS nor proof of opacity. Retry natively or change format.

# 10. Parameters / Export Rules

## Size

- `1 MB = 1,000,000 bytes` unless MiB is explicit.
- Budget approximately `max_bytes × 8 × 0.96–0.98`; reserve audio/container overhead.
- If oversized, re-encode from the master and adjust codec settings, palette, dimensions, or cadence deliberately.

## Master

- Prefer ProRes 4444 MOV (`ap4h`) or RGBA PNG sequence for per-frame repair.
- Mux/retime audio after slow frame processing when simultaneous writing causes backpressure.

## HEVC Alpha MOV

- Use only for Apple/runtime paths known to support it.
- Typical FFmpeg path: `hevc_videotoolbox -pix_fmt bgra -tag:v hvc1`, with explicit bitrate and `alpha_quality`.
- Verify with AVFoundation/VideoToolbox or another decoder known to expose auxiliary Alpha.

## ProRes 4444 MOV

- Preferred interchange/master; expect large files.
- Typical settings: `prores_ks -profile:v 4 -pix_fmt yuva444p10le -alpha_bits 8`.

## VP9 Alpha WebM

- Use `libvpx-vp9`, `yuva420p`, and `-auto-alt-ref 0` for compatible browsers.
- Some editors, including macOS 剪映 in verified use, ignore its Alpha.

## Transparent GIF

- GIF has binary transparency and no audio; it is not full 8-bit Alpha.
- Use a global palette and explicit loop/disposal; verify frame count, per-frame duration, transparency, and complete composition.
- Search dimensions, fps/frame count, colors, and loss; never optimize only for bytes.
- For metallic/pale gradients, trade modest resolution for more colors and lower loss before reducing cadence. A verified 3 MB case improved from 712×712/96 colors/lossy 160 to 592×592/224 colors/lossy 40.
- A verified 2 MB, 3-second product GIF required 424×424, 20 fps, 60 frames, 80 colors. Treat this as evidence, not a preset.

# 11. Success Criteria

All applicable conditions pass: source preserved; output opens in target runtime; Alpha decodes and is not inverted; duration tolerance is met; full-action retime has correct sequence, frame count, and uniform timestamps; exact byte ceiling is met; requested dimensions/cadence/loop/audio are correct; subject structure and effects remain; no matte islands or colored/black/white fringe appears across light/dark/saturated composites; temporal edges are stable; short/risky clips pass all-frame review; copied deliverables match verified files.

# 12. Failure Cases

- Product disappears/Alpha inverted: wrong key or polarity.
- Pale product/logo missing: global white key or semantic confusion.
- Enclosed opening retains matte: semantic mask treated surrounded background as product.
- Moving side holes retain green: fixed/global logic missed motion or risks legitimate green artwork.
- White/black halo: contaminated partial-Alpha RGB, wrong Alpha semantics, or outward blur.
- Contour breathes/loses leading edge: unstable masks or unaligned temporal voting.
- HEVC Alpha displays black: target ignores auxiliary Alpha; zero transparent RGB becomes visible.
- HEVC Alpha decode errors (`PPS id out of range`, AVFoundation `-11801`/`-12713`): incompatible encoder/decoder path.
- Retimed clip stutters/has extra tail: incorrect rate assumption, forced fps, or CFR duplication.
- GIF QC is blank/partial: independently seeking an optimized delta-frame GIF.
- GIF metal has cloud bands/speckles: palette too small and loss too high.
- Audio ends short: filtered encode dropped a final AAC packet.
- Slow matte deadlocks: simultaneous audio/video writing hit backpressure.
- Native helper fails: quarantine or architecture mismatch.

# 13. Recovery / 修正方式

- Rebuild from source/master; never stack repairs on a delivery encode.
- For inverted/missing Alpha, inspect grayscale Alpha on saturated background and correct polarity or mask method.
- For uniform white matte with semantic jumps, remove only background connected to the canvas boundary; preserve enclosed whites/icons; optionally inset 1–2 px and add a narrow feather, then verify all frames.
- For enclosed white/green openings, estimate corner matte, restrict by ROI/shape/size, clear only the matching component, and repair its narrow spill ring.
- For moving holes, interpolate a narrow ROI between time-position anchors, clear compact matte-colored components, keep the rim opaque, and verify every visible frame.
- For halos, reverse known matte or extend clean interior RGB into the feather; set RGB=0 at Alpha=0 and avoid outward blur.
- For contour instability, smooth small noise, threshold near the 50% contour, add one feather, and motion-align masks before IoU-gated temporal stabilization.
- For HEVC failure, retry with validated FFmpeg/VideoToolbox and native verification; otherwise use ProRes 4444, GIF, PNG sequence, VP9 Alpha, or baked preview based on target.
- For retiming, count decoded frames, rebuild uniform PTS at `N/T`, cap to `N`, and inspect deltas plus the loop seam.
- For GIF QC, decode sequentially from frame 0 into full RGBA frames. Sample final frame at `duration - frame_interval`, not `duration × 0.999`.
- For GIF gradient artifacts, compare a risk ROI with a clean reference and trade resolution for palette/lower loss.
- For audio issues, process video first, retime audio separately, then mux and verify duration.
- For quarantine, compile Swift sources into a temporary cache.

# 14. Usage Examples

```bash
python3 scripts/transparent_video.py inspect "input.mp4"

python3 scripts/transparent_video.py matte "input.mp4" "master.mov" \
  --erode-radius 0.8 --contour-smooth-sigma 1.3 \
  --uniform-edge-sigma 1.2 --preserve-premultiplied-edge-rgb

python3 scripts/transparent_video.py encode "master.mov" "delivery.mov" \
  --format hevc-alpha --duration 3 --max-mb 2 --audio-kbps 64

python3 scripts/transparent_video.py verify "delivery.mov" \
  --duration 3 --duration-tolerance 0.01 --max-mb 2 --qc-dir "delivery_qc"
```

Natural-language examples:

- “Remove the white background, preserve the full animation, and create 3-second transparent MOV and GIF files under 2 MB each.”
- “This transparent MOV looks black in Figma; diagnose compatibility before modifying it.”
- “Repair only the green screen visible through the camera opening and moving side holes.”

# 15. Limitations

- Bundled automatic semantic matting is macOS-specific; other systems need another mask backend.
- No model handles every pale product, reflection, hand, glow, and enclosed opening automatically; difficult clips need inspected local repairs.
- HEVC Alpha support varies; Figma Design and many browsers/editors may ignore it.
- GIF has palette color, binary transparency, no audio, and large quality tradeoffs under strict limits.
- The current CLI automates MOV/WebM better than optimized GIF search; advanced GIF tuning may still require FFmpeg/gifsicle and visual comparison.
- Arbitrary exact fps such as `124/3` may not be accepted by every runtime.
- Product-specific ROI coordinates are intentionally not core defaults.

# 16. 可组合的其他 Skills

- media matting/background removal for alternative mask generation;
- general video editing for cuts, captions, overlays, and audio before transparency processing;
- image/frame repair for difficult masks and tracked regions;
- visual QA/contact-sheet tools for batch inspection;
- deployment/runtime compatibility tools for the final target.

# 17. 未来可拆分的子 Skills

Keep the core workflow unified because real deliveries normally require `inspect → matte → retime → encode → verify`. Consider later extraction only when independently reused:

1. `transparent-video-matte` — masking, spill, and hole repair.
2. `video-retime-complete-cycle` — exact duration, uniform PTS, audio, loop continuity.
3. `transparent-gif-optimize` — palette, cadence, disposal, compression, sequential QC.
4. `alpha-video-verify` — native/FFmpeg Alpha checks and multi-background review.
5. `video-size-budget` — codec-independent byte budgeting.
6. `video-format-compatibility` — runtime selection and fallbacks.

# 18. Changelog

## V1.0 — 2026-09-11

- Retained inspect, Vision matte, ProRes master, HEVC/ProRes/VP9 export, byte budgeting, and multi-background verification.
- Made the specification platform-neutral while documenting the bundled macOS backend.
- Added decoded-frame-count retiming, uniform `N/T` fps, audio retiming, and duplicate-tail prevention.
- Added GIF export rules, sequential delta-frame QC, final-frame sampling, disposal/loop checks, and metallic-gradient tradeoffs.
- Added connected-boundary white-matte recovery, enclosed white/green opening repair, and tracked moving-hole repair.
- Added spill, edge-RGB, changing-matte, and temporal-contour recovery.
- Added tested FFmpeg selection, native HEVC Alpha verification, quarantine recovery, and compatibility fallbacks.
- Added Figma HEVC Alpha diagnosis and opaque preview alternatives.
- Excluded one-off coordinates, product filenames, webpage prototype work, unverified attempts, and chat history.

## V1.1 — 2026-10-30

- Added first-class raster Lottie build/verify, embedded lossless PNG assets, crop offsets, deduplication, exact source-frame comparison and explicit player-test status.
- Added GIF transparent-index safety, full-timeline key-color sampling, source-specific straight/premultiplied checks, fade handling and lossless-first budgeting.
- Fixed MOV `--duration` to retime all decoded frames instead of truncating; retime audio and verify output count/duration. Reject direct FFmpeg transcode when only the native decoder exposes HEVC Alpha.
- Fixed GIF QC selection to use cumulative frame delays, including final holds.
- Added GIF timeline inspection/verified merge, synthetic regression cases, bilingual tutorial and copyable prompts.
