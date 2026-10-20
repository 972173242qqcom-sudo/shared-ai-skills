---
name: collect-design-assets
description: Collect, filter, organize, and document design reference assets across images, video/motion, websites/cases, and editable source materials. Use when a task needs reusable asset discovery, source tracking, quality screening, deduplication, downloads, curated collections, or failure recovery for design research. Do not use for ordinary video editing, background removal, or generating new assets when collection is not the main task.
---

# Skill Name

`collect-design-assets`

# Version

V1.0 — consolidated from verified image, product-render, official-site, motion-case, product-video, website-case, and editable-motion collection work.

# Purpose

Collect design reference assets that can be reviewed, reused as internal references, or handed to designers with clear source records. The skill turns a broad visual request into structured search terms, candidate sources, quality filters, deduplication, downloads, naming, folder organization, attribution notes, and recovery logs.

Keep one unified workflow. Select the collection strategy by asset type instead of splitting the task into separate skills.

# Scope

## Use This Skill When

- A user asks to collect, download, curate, organize, or document design reference assets.
- The target assets are images, product renders, website/case-platform examples, video or motion references, UI/product interaction recordings, editable motion assets, or source files such as JSON, dotLottie, SVG, AE templates, or transparent video.
- The deliverable needs a manifest, source list, contact sheet, overview image, key frames, clip index, attribution file, or reusable folder structure.
- The task requires recovering from broken links, blocked downloads, noisy search results, duplicate responsive variants, unclear licensing, or over-strict filtering.

## Do Not Use This Skill When

- The user primarily wants to generate new images, illustrations, videos, or animations from prompts.
- The user primarily wants to edit a video, add captions, remove a background, or export transparent media after the asset is already chosen.
- The request depends on paid downloads, login-gated workspaces, subscriptions, or purchases that the user has not authorized or completed.
- The task is only a quick web lookup and does not require collecting or organizing assets.

# Inputs

- `goal`: target asset type, design use, desired quantity or breadth, and whether the output is a large library or a small curated set.
- `context`: reference images, links, product category, audience, platform, design direction, required dimensions, and any exclusion rules.
- `sources`: allowed or preferred source types, such as official pages, official videos, manuals, tutorial videos, case platforms, public asset libraries, or direct URLs.
- `licensing`: whether assets are only for internal reference, need attribution, must be commercially reusable, or cannot come from unclear sources.
- `preferences`: naming language, folder layout, output formats, review artifacts, and quality thresholds.

# Outputs

- Downloaded or linked assets organized by source, asset type, task dimension, or curated collection.
- A machine-readable manifest or index containing at least file path, source URL, source page when available, bytes, hash, dimensions or media metadata, tags, decision, and license note.
- Human-readable source notes such as `README.md`, `SOURCE_AND_LICENSE.txt`, `案例清单与来源.md`, `来源索引.tsv`, `截取参数.tsv`, or `文件索引.tsv`, depending on asset type.
- A review artifact such as a contact sheet, overview image, key frames, storyboard, previews, or case thumbnails.
- A skipped/failure report with rejected reason, retry status, and any quarantined duplicates or discarded assets.

# Process

1. Clarify the collection target: asset type, design purpose, quantity, quality floor, source boundaries, and licensing requirement.
2. Build anchors from the user's examples or constraints. Extract object/category words, brand/model words when relevant, scene or feature words, visual style words, motion/action words, source-type words, and negative filters.
3. Expand keywords by source type. Use official names and functional terms for real products; use category, interaction, flow, and motion terms for inspiration cases. Switch language by source instead of forcing every query to be bilingual.
4. Choose sources deliberately. Prefer official pages, official videos, manuals, and source files when the user needs traceability; use case platforms for inspiration; use public asset libraries only with license and attribution records.
5. Save candidates before downloading. Keep URL lists, page caches, structured records, candidate tables, or resource manifests so retries do not restart from search.
6. Download or capture into a working area first. Do not put noisy candidates directly into the final deliverable folder.
7. Apply basic quality checks: reachable URL, allowed format, file size, dimensions or duration, clear subject, relevance to the goal, and no obvious watermark or low-resolution preview.
8. Deduplicate in layers: normalized URL, content hash, perceptual similarity, responsive variant grouping, crop/subject-normalized similarity when available, and semantic duplication by brand, function, action, or case.
9. Create review artifacts. Use contact sheets for images and static assets; use key frames, storyboard frames, overview grids, or short previews for video and motion cases.
10. Curate and organize final assets. Move duplicates, rejects, and uncertain files into quarantine or discarded folders rather than deleting them.
11. Record sources and licensing. Every selected asset must remain traceable to a source URL or source page; editable and public-library assets need explicit author, license, license page, and download date when available.
12. Validate the handoff. Confirm files open, metadata is plausible, manifests match files, previews represent the final set, and failure logs explain skipped material.

# Search And Source Rules

- Convert the request into concrete dimensions: object, product/category, brand/model, scene, function, visual style, motion/action, source type, and exclusions.
- For real products or interfaces, combine `brand/model + app/support/tutorial/settings/control/setup` or the equivalent source-language terms.
- For interaction inspiration, combine `category + pairing/onboarding/device control/interaction/motion/flow`.
- For product animation, combine `product category or brand/model + product film/official/introducing/design/animation`.
- For editable motion, combine action terms such as `tap`, `press`, `hold`, `long press`, `swipe`, `double tap`, `pinch`, `rotate` with `Lottie`, `animation`, `AE template`, `transparent`, or source-file terms.
- Use official international sources, video platforms, case platforms, and editable-motion libraries with English keywords by default. Use Chinese keywords when targeting Chinese brands, local tutorials, Chinese product names, or domestic app/software references.
- Do not turn a user's reference social post into a reusable asset source unless its license explicitly allows reuse. Treat it as style direction only.
- Prefer original CDN/media URLs for downloads, but record the human-readable page URL as the source page.

# Source Selection

- Official pages: best for clean, high-resolution, traceable product images, renders, interface screenshots, PDFs, and structured page data. Expect noise from icons, logos, social previews, UI screenshots, feature illustrations, and responsive variants.
- Official videos and support/tutorial channels: best for real app flows, onboarding, device settings, product animation, and operation states.
- Manuals and PDFs: useful when software or interface pages are clearer in documentation than in video.
- Case platforms: useful for product + UI motion inspiration, device pairing, onboarding, hardware/software interaction, and visual rhythm. Prefer original MP4/GIF/PNG resources over screenshots or thumbnails.
- Public asset libraries: useful for illustrations, gestures, icons, Lottie/dotLottie, SVG, AE templates, and transparent assets. Always preserve license and attribution.
- Review/tutorial videos: acceptable when official sources do not show the needed real interface or operation state. Label them as non-official.
- E-commerce and social/image platforms: useful for discovery or style expansion, but licensing and quality are often weaker; record uncertainty and avoid implying commercial reuse.

# Quality Screening

- Default image floor: downloadable image, accepted format, width at least 640 px, height at least 480 px, long edge at least 1000 px, and total pixels at least 800000 unless the task justifies smaller assets.
- Product/reference images should have a clear subject, complete composition, useful lighting, sufficient resolution, and no obvious watermark.
- When choosing one image per case, rank product/case relevance before raw pixel count. A very large concept background, app mockup, or feature illustration is weaker than a smaller image that clearly shows the hardware or official case focus.
- For responsive variants, keep the clearest or largest useful version, usually the one with more pixels and larger bytes after near-duplicate grouping.
- White or near-white background ratio is only an auxiliary signal. Do not use it as a hard default because it can reject valid dark-background, gray-studio, or mood-render assets.
- For product renders, positive signals include transparent or stable background, clear product edges, reasonable subject bounding box, and filenames or metadata that indicate product/device/finish/view.
- Negative image signals include icons, logos, QR codes, small color chips, social preview images, UI-only feature art, tiny squares, and unrelated decorative illustrations.
- Video or motion cases must contain reusable action: pairing, scanning, connecting, state feedback, control changes, gestures, parameter feedback, product rotation, open/close, assembly, color switching, structure reveal, or lightweight function visualization.
- Avoid pure advertising atmosphere, unboxing, talking-head sections, outdoor lifestyle scenes, or unrelated scrolling when the task asks for product motion or interface reference.
- Editable sources must be inspectable, preserve the source file when available, and not rely solely on a compressed preview.

# Deduplication And Quantity Control

- Treat duplicate control as more than same URL removal. Also remove or lower priority for repeated brand/function combinations, repeated video sections, same shot variants, same author series with little variation, and case-platform resources that only differ by thumbnail size.
- For images, use URL normalization, SHA-256, perceptual hash, filename/spec-token normalization, and crop/subject-normalized comparison when the collection is large or responsive variants are noisy.
- For videos, avoid collecting multiple segments that show the same ordinary setup, EQ, pairing, gesture, or status unless the user explicitly wants variants.
- Use quotas only when the task requires coverage: by source, brand, product family, interaction scenario, function dimension, visual type, or final count. Do not hardcode counts from prior projects as defaults.
- Prefer quarantine folders such as `_duplicates`, `_discarded`, or `_review` over deletion.

# Download, Naming, And Folder Rules

- Use browser-like headers when needed, and include a source-page referer for official/CDN assets when that improves reliability.
- Check file size before download when the server provides it; after download, infer extension from content or MIME rather than trusting the URL suffix.
- Generate a content hash for every downloaded file. Hash-based names are useful for large libraries; semantic names are better for small curated sets.
- For curated sets, use stable sortable names such as `01_brand_product_scene.ext` or `01_visual-description.ext`. Keep official brand/model spelling when present.
- Keep process and final folders separate. Working candidates, page caches, rough storyboards, and failed downloads belong in an analysis or working folder; final folders should contain selected assets, previews, source records, and overview artifacts.
- Use folder dimensions that match the task, such as `source/type`, `brand/product/action`, `model/color/index`, `case-number`, `product-group`, `images`, `videos`, `previews`, `keyframes`, or `editable-source`.
- Do not overwrite sources by default. Preserve originals alongside optimized, extracted, clipped, or rendered outputs.

# Manifest And Source Records

Minimum fields for image/static manifests:

- `file`
- `source_url`
- `source_page`
- `width`
- `height`
- `bytes`
- `sha256`
- `source_type`
- `tags`
- `license_note`
- `decision`
- `created_at`

Minimum fields for video/motion indexes:

- `file`
- `source_url`
- `source_page`
- `source_type`
- `duration`
- `resolution`
- `fps`
- `video_codec`
- `audio_codec`
- `clip_start`
- `clip_end`
- `selection_reason`
- `sha256`

Minimum fields for editable or public-library assets:

- `asset`
- `author`
- `source`
- `license`
- `license_page`
- `download_date`
- `source_files`
- `derived_outputs`
- `usage_note`

# Asset-Type Strategies

## Images And Product Renders

- Extract candidates from direct URLs, page HTML, `srcset`, lazy-load attributes, Open Graph tags, CSS `url(...)`, inline JSON, and CDN links.
- For official pages, discover related pages from seed URLs only within the relevant product or content scope, and exclude non-asset pages such as support, compare, specs, account, cart, and generic shop pages when they pollute results.
- For platform pages, prefer original image URLs over page screenshots, thumbnails, or previews.
- Generate contact sheets early and after final selection. Use them to catch automatic-filter mistakes and style drift.
- For small curated collections, manual quality selection and semantic names are acceptable; do not force large-library automation.
- For large official-site collections, use staged passes: page discovery, image extraction, download, hash dedupe, perceptual dedupe, classification, and refinement.

## Video And Motion References

- Separate real app/interface recordings, official product films, and white/light-background product-motion clips. They answer different design questions and should not be mixed without labels.
- Build a candidate table before downloading. Record case number, brand/product when relevant, scenario/action, source type, URL or video ID, and initial reason.
- Download candidates to a working folder, generate rough storyboards, then create finer key-frame or per-second review only for high-value candidates.
- Record clip ranges before cutting. For non-continuous selected moments from one source, record each segment and the stitched output.
- Common proven outputs are H.264 MP4 at 30 fps with no audio for app or white-background motion clips, and 1920x1080 H.264 plus AAC when preserving a complete official product video.
- Export key frames and an overview grid for designer review.
- Verify final videos with media metadata and full decode checks when files are delivered, not only linked.

## Websites And Case Platforms

- Judge case-platform assets by similarity to the design problem: product hero, hardware + UI relation, pairing, discovery, scanning, state changes, control feedback, page hierarchy, product scale, button placement, and motion rhythm.
- Command-line page fetches may be blocked by WAF. If that happens, use a browser or saved resource list to identify the original CDN media while preserving the page URL as provenance.
- Prefer original MP4/GIF for dynamic cases and original PNG/WebP/JPEG for static pages. Screenshots are fallback records, not the preferred asset.
- For one case with multiple resources, name them by role: main motion, page image, cover, still frame, or secondary detail.

## Editable Assets

- Prefer editable sources in this order when the task requires adaptation: Lottie JSON/dotLottie, AE project/template, transparent video, MP4/GIF preview, then static SVG/PNG for reconstruction.
- Use concrete detail pages or source records over heavy category pages when possible.
- Save source files, not only rendered previews.
- Record author, source, license, license page, and download date.
- If a preview has a solid background but an editable vector source exists, rebuild or render transparency from the source rather than keying the preview.
- For transparent derived outputs, keep RGB clean under transparent pixels, provide black or contrasting previews, and verify alpha with screenshots or decoded frames.
- If login, subscription, purchase, or workspace save is required, stop and ask the user to handle authorization instead of bypassing it.

# Failure Recovery

- If search returns thumbnails or previews, inspect page resources, `srcset`, structured page data, or CDN variants for larger originals.
- For official image proxies or responsive CDNs, cautiously try visible width/quality parameters such as `w`, `width`, or `q` to request a larger variant, then keep only responses that decode and pass the quality/relevance checks.
- If downloads fail with 403, timeout, or SSL errors, keep the candidate URL, retry in smaller batches, add browser headers or referer when appropriate, and try known format variants only when the URL pattern supports it.
- If filters reject visually valid material, preserve skipped reasons and adjust the specific over-strict rule rather than discarding the batch.
- If official pages produce icons, logos, QR codes, UI screenshots, or feature art, add negative filename and image-feature rules, then rerun classification/refinement.
- If responsive variants explode collection size, group near-duplicates and keep the best-quality representative.
- If a single capture is incomplete, write structured records for the missing dimensions and rerun only the incomplete subset.
- If licensing is unclear, keep the asset out of reusable deliverables or mark it as reference-only with a clear note.

# Rules

- Stay platform-neutral and source-traceable. Do not require a single provider, browser, downloader, or model when equivalent tools can produce the same manifest and validation.
- Do not include personal absolute paths, one-time URLs, project-specific brands, fixed quantities, private chat details, or temporary filenames in reusable prompts or skill outputs.
- Do not claim commercial reuse unless the source license supports it.
- Do not treat automatic filters as final aesthetic judgment. Use review sheets, key frames, or overview grids.
- Do not delete duplicates or failures by default; quarantine them.
- Do not mix raw candidates with final curated deliverables.
- Do not invent source metadata. If source page, author, license, or dimensions are unavailable, mark them unknown.

# Success Criteria

- The collection has clear scope, source boundaries, and licensing notes.
- Search terms and sources follow from the user's actual design target.
- Selected assets are relevant, high enough quality for the stated use, and not dominated by duplicates.
- Files are named and organized so a designer can browse them without reading the entire manifest.
- Every selected asset has source provenance and review status.
- Review artifacts make quality and coverage visible at a glance.
- Failures, rejects, duplicates, and uncertain licensing are recoverable and auditable.

# Failure Cases

- Required assets are behind login, subscription, purchase, or unavailable permissions.
- The user requires commercial-ready assets but available sources do not provide adequate licensing.
- Search results do not contain enough relevant assets after expanding source type, language, and keywords.
- Downloaded material cannot be validated, decoded, opened, or traced to a source.
- The collection becomes mostly thumbnails, duplicates, ads, icons, UI noise, or unrelated inspiration.

# Handoff Notes

Report:

- final folder structure;
- number of selected assets and quarantined or skipped candidates;
- source types used and any licensing caveats;
- manifest/index files created;
- review artifacts created;
- validation performed;
- failures that need user action, such as login, paid access, missing permission, or unclear license.

# Future Split Points

Keep V1.0 unified because the verified projects shared the same backbone: keyword expansion, source choice, candidate capture, download, filtering, dedupe, organization, source recording, review artifacts, and recovery. Consider separate skills only if a strategy becomes independently reusable and complex enough to maintain on its own:

- large-scale official-site image crawling and classification;
- video case discovery, clipping, storyboard, and decode validation;
- editable motion asset sourcing, licensing, alpha rendering, and source preservation;
- case-platform media extraction and provenance capture.

# Changelog

## V1.0 — 2026-09-12

- Consolidated verified design-asset collection practices into one unified Skill.
- Covered shared search, keyword expansion, source choice, quality screening, deduplication, download, naming, folder organization, source recording, and failure recovery rules.
- Preserved strategy-specific rules for images/product renders, video/motion references, websites/case platforms, and editable assets.
- Added real-task-test corrections: rank product/case relevance before raw pixel count, and cautiously validate larger official image-proxy/CDN variants.
