# Lottie delivery workflow

## Choose the representation

Video/photorealistic render -> embedded raster-sequence JSON. This preserves appearance and partial Alpha; it is not editable vector geometry or resolution-independent. Simple shape animation with vector sources -> native vector Lottie via appropriate authoring tools. This skill's script does not vectorize or edit arbitrary Lottie.

Ask or infer the target player, renderer, display size, duration, loop/hold intent, and byte limit. PNG is the default for lossless RGB/Alpha and image interoperability. WebP may reduce bytes but requires a separate explicitly tested export path; the bundled exporter deliberately supports PNG only. JSON with images is not automatically a .lottie ZIP package.

## Prepare frames

Decode existing Alpha with a verified decoder; do not rematte an already transparent source. Use zero-padded PNG names, one common canvas, and the source's verified straight RGBA. HEVC auxiliary Alpha may require the native helper; ordinary FFmpeg output can omit it. Keep the original frames/master.

The bundled exporter distributes all N frames uniformly across T seconds (`fr=N/T`, `ip=0`, `op=N`). It does not preserve variable source durations. For variable cadence or a special final hold, first construct the intended uniform timeline explicitly or use a separately verified timing-aware implementation.

```bash
python3 scripts/lottie_sequence.py build frames animation.json --duration 3 --max-mb 5
python3 scripts/lottie_sequence.py verify animation.json --frames frames --max-mb 5
```

It crops visible Alpha bounds with padding, retains crop positions, deduplicates identical embedded PNGs, merges adjacent identical placements, and represents fully transparent frames as no active layer. It reconstructs every source instant and compares exact Alpha and visible RGB. Reports say `target_player: not_tested`; this is not runtime validation. Over-budget output fails validation and remains a candidate; do not deliver it as meeting the budget. No automatic resolution/quality reduction is performed.

## Optimize and verify

Try asset deduplication/cropping and PNG optimization first. Base64 expands binary data, so measure final JSON bytes. If still too large, create a new resized source-frame set, keep original aspect/canvas alignment, rebuild, and report the chosen size. Do not silently change colors or remove source instants.

Test the actual target player's version and renderer, image loading, fractional framerate, soft Alpha over light/dark/color, crop alignment, first/last state, repeat and final hold, and memory/performance at intended display size. A small JSON may still decode into many large images. Record player/renderer/version and tested results. If unavailable, report untested and deliver a reproducible preview route; do not claim universal iOS/Android/Figma compatibility.

For local web preview, use a trusted/pinned lottie-web runtime with `animationData`, set `loop` explicitly, and serve over localhost. Offline preview requires a local player bundle. Keep user assets local unless upload is explicitly authorized. Lottie upload to an external validator is not required.

Official references: [lottie-web](https://github.com/airbnb/lottie-web), [composition settings](https://github.com/airbnb/lottie-web/wiki/Composition-Settings), [usage](https://github.com/airbnb/lottie-web/wiki/Usage).
