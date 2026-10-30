#!/bin/zsh
set -euo pipefail

script_dir="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
machine="$(uname -m)"
if [[ "$machine" == "aarch64" ]]; then
  machine="arm64"
fi
bundle_bin="$script_dir/bin/darwin-$machine"
bundled_quarantined=0

if command -v xattr >/dev/null 2>&1; then
  if xattr -p com.apple.quarantine "$bundle_bin/make_transparent" >/dev/null 2>&1 || \
     xattr -p com.apple.quarantine "$bundle_bin/verify_alpha" >/dev/null 2>&1; then
    bundled_quarantined=1
  fi
fi

if [[ -x "$bundle_bin/make_transparent" && -x "$bundle_bin/verify_alpha" && "$bundled_quarantined" -eq 0 ]]; then
  echo "Bundled Apple helpers: ready ($machine)"
elif command -v swiftc >/dev/null 2>&1; then
  if [[ "$bundled_quarantined" -eq 1 ]]; then
    echo "Bundled Apple helpers are quarantined; bundled Swift sources will compile to a temporary cache on first use."
  else
    mkdir -p "$bundle_bin"
    cache_dir="${TMPDIR:-/tmp}/process-transparent-video-swift-cache"
    mkdir -p "$cache_dir"
    CLANG_MODULE_CACHE_PATH="$cache_dir" SWIFT_MODULECACHE_PATH="$cache_dir" \
      swiftc -O "$script_dir/make_transparent.swift" -o "$bundle_bin/make_transparent"
    CLANG_MODULE_CACHE_PATH="$cache_dir" SWIFT_MODULECACHE_PATH="$cache_dir" \
      swiftc -O "$script_dir/verify_alpha.swift" -o "$bundle_bin/verify_alpha"
    echo "Apple helpers: compiled ($machine)"
  fi
else
  echo "Apple helpers are unavailable or quarantined, and swiftc is missing." >&2
  echo "Install the Xcode Command Line Tools with: xcode-select --install" >&2
  exit 2
fi

if ! command -v ffmpeg >/dev/null 2>&1 || ! command -v ffprobe >/dev/null 2>&1; then
  if command -v brew >/dev/null 2>&1; then
    echo "FFmpeg/ffprobe missing; installing with Homebrew..."
    brew install ffmpeg
  else
    echo "FFmpeg and ffprobe are required. Install Homebrew first, then run: brew install ffmpeg" >&2
    exit 3
  fi
fi

ffmpeg -hide_banner -encoders 2>/dev/null | grep -q hevc_videotoolbox || {
  echo "The detected FFmpeg build lacks hevc_videotoolbox." >&2
  exit 4
}

ffmpeg_major="$(ffmpeg -version | sed -n '1s/^ffmpeg version \([0-9][0-9]*\).*/\1/p')"
if [[ -n "$ffmpeg_major" && "$ffmpeg_major" -lt 8 ]]; then
  echo "Warning: FFmpeg $ffmpeg_major detected. HEVC Alpha must pass native AVFoundation verification; use a validated FFmpeg 8.x build if it fails." >&2
fi

echo "process-transparent-video is ready."
echo "ffmpeg: $(command -v ffmpeg)"
echo "ffprobe: $(command -v ffprobe)"
