# V1.1 validation — 2026-10-30

- Skill frontmatter/naming: official quick validator PASS.
- Synthetic Lottie: exact Alpha and visible RGB, crop offsets, moved/repeated assets, fully transparent frame, exact duration, budget rejection and placement-corruption detection PASS.
- GIF: variable 20/980 ms timing, full RGBA timeline comparison and actual QC midpoint selection PASS.
- MOV: 10 distinct source states retained after 1s -> 0.5s, 0.37s and 2s retiming; frame identities checked by pixel values, frame count and duration verified, retimed audio duration checked. FFmpeg 8.1.2 / macOS.
- Local real-sequence smoke test: 151 source instants, 215×256 test canvas, 3s, 87 embedded PNG assets, 498827 bytes; exact source comparison PASS. Source product media is not included in this repository.
- Target Lottie player/renderer integration: **not tested**. Structural/source checks are separate from runtime compatibility.
- Existing semantic matting / HEVC native helpers were preserved; this release did not re-run all historical product-matting cases or qualify every platform.

Reproduce synthetic checks with Python 3.10+, Pillow and FFmpeg/FFprobe on PATH:

```bash
python3 scripts/test_regressions.py
```
