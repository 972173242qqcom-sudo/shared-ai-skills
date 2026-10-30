# GIF production rules

## Correctness before compression

- Reserve a transparency palette index exclusively for transparent pixels. Pillow quantization may still choose a padded reserved index for opaque black. Remap those opaque indices to the closest **valid** palette color before assigning transparency from Alpha. Verify opaque black regions against source on every frame.
- Sample critical small colors (LEDs, logos) across **all frames**, including weak-light phases; global thumbnails may omit them. Allocate a configurable dedicated palette and map protected pixels to nearest valid colors. Do not hard-code blue or 64 colors for every product. Measure color error in the same source ROI through time.
- Determine whether the actual decoded RGB is straight or premultiplied using known translucent samples, decoder behavior and light/dark composites. Alpha-zero RGB alone is not proof. Unpremultiply only verified premultiplied input; never blindly reuse a previous product's correction.
- GIF Alpha is binary. A threshold discards soft fades; spatial coverage dithering approximates opacity but may look grainy. Stable blue-noise coverage and a gentle optional Alpha curve can improve a fade, but must be inspected at intended display size. Preserve original Alpha as the reference. Do not bake a background or curve a whole product without the user's requested treatment.

## Budget order

First inspect and merge identical consecutive visual states, accumulating their delays. Verify full-canvas sequential RGBA and timeline equivalence, loop and disposal. `scripts/gif_timeline.py INPUT --merge-to NEW.gif` is a conservative attempt: Pillow may requantize; it deletes mismatched candidates and fails rather than claiming losslessness. For large palettes, use palette/block-preserving operations with the same visual timeline comparison.

Then try a modest resolution decrease, palette allocation and RGB dithering options. Preserve small key colors. Reduce cadence only when necessary and disclose dropped source samples; stored frame count after identical-state merging is not motion sample count.

## Timing and QC

Use each frame's cumulative duration to select a sample; average FPS is wrong for merged states and holds. GIF delay units are 10 ms. Distribute rounding error across delays and report realizable total duration. Explicitly distinguish complete-action speed-up from adding a final hold. Keep source first/last states and inspect loop boundary. Never append frame zero by default.

Decode sequentially from frame zero. Check missing/extra Alpha, opaque dark details, logo and LED RGB, and full-size edges against a reference on light/dark/saturated backgrounds. For retiming/merge compare state + accumulated delay rather than frame counts alone.
