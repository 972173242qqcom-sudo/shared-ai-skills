# Format and Edge Guide

## Format selection

| Goal | Preferred output | Notes |
|---|---|---|
| High-quality master/editing | ProRes 4444 MOV (`ap4h`) | Robust Alpha and edge fidelity; large files |
| macOS 剪映/CapCut with size limit | HEVC with Alpha MOV (`hvc1`) | Small and compatible on Apple platforms; encode with VideoToolbox |
| Browser delivery | VP9 Alpha WebM | Small, but 剪映 may ignore its separate Alpha stream |
| Figma prototype | Transparent GIF, PNG sequence, mask simulation, or baked H.264 | Figma may ignore HEVC auxiliary Alpha and show transparent RGB as black |
| Universal non-transparent preview | H.264 MP4 | Preview only; cannot carry Alpha |

Do not promise HEVC Alpha portability on Windows, Android, or arbitrary web runtimes without testing the exact target.

## Source classification and edge treatment

### Existing Alpha

Decode a real Alpha plane before transcoding. VP9 Alpha may require the `libvpx-vp9` decoder. Preserve straight/premultiplied semantics during conversion and inspect composites.

### Uniform white matte

Simple chroma/luma keying is acceptable only when the subject contains no similar near-white regions. For white or pale products, use semantic segmentation. Recover edge RGB from the white composite when the mask follows the original antialiased boundary:

`premultiplied_foreground = observed_rgb - white * (1 - alpha)`

If semantic segmentation drops a stable product face against a completely
uniform matte, identify only white background connected to the canvas boundary
and keep enclosed product whites and icons. This is safe only when the true
background reaches the border; verify all frames when the subject approaches it.

### Uniform green matte with enclosed product openings

Do not globally key green when product artwork also contains green. Estimate the
matte from clean corners, restrict candidates by protected ROI, component size,
shape, and location, and clear only the selected matte-connected region. Grow
through a narrow band of nearby spill and keep the physical opening rim opaque.

For small perforations that move along an edge, interpolate a narrow ROI between
time-position anchors. Clear only compact matte-colored components in that ROI
and verify every visible frame. A fixed wide ROI can cross legitimate artwork as
the product rotates.

### Uniform black matte

For black-matte footage, the observed RGB is already close to premultiplied foreground RGB. Copying unassociated source RGB into translucent pixels can produce bright edges.

### Matte changes during the clip

Detect the current matte from clean corner samples per frame. Apply one consistent edge rule after an intentional mask inset. A previous verified case showed that subtracting white again from a newly inset feather darkened early frames while later black-matte frames remained correct.

### Light product, logo, holes, shadows, hands, glow

Use semantic foreground masks and visually protect meaningful regions. Close only tiny false holes. Do not globally fill enclosed areas because rings and product openings may need to stay transparent. Separate the solid product and translucent effect when they need different Alpha logic.

### Unstable contour across frames

First smooth small contour noise, threshold at the 50% contour, and add a controlled narrow feather. For temporal stabilization, motion-align neighboring masks and use an IoU gate; do not majority-vote unregistered moving silhouettes because it trims leading edges.

### Strict GIF budgets with metallic or pale gradients

Low-color/high-loss GIF settings can turn silver, white, or gray gradients into
cloud bands and speckles even when a contact sheet looks acceptable. Inspect the
full-size surface during overlap and motion. Prefer a modest resolution reduction
that allows a larger palette and lower loss before sacrificing motion cadence.

Optimized GIFs may store changed rectangles only. Decode sequentially from frame
0 into complete RGBA frames before QC; independent fast seeks can produce false
blank or partial frames. Sample the final frame at `duration - frame_interval`.
Confirm loop count, disposal, total frames, and per-frame duration.

## Verification matrix

Verify at minimum:

- first and last frame;
- 25%, 50%, and 75% timestamps;
- every matte/background transition;
- fastest motion and maximum subject extent;
- light neutral background (for dark fringes);
- dark neutral background (for white fringes);
- saturated red or blue background (for holes and Alpha inversion);
- original-scale crop of detailed edges, logos, buttons, fingers, and glow.

For short product animations under roughly 200 frames, an all-frame Alpha/contact-sheet pass is practical and preferred when edge consistency is the main concern.
