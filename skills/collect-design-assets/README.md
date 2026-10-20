# Collect Design Assets

[中文](#中文) | [English](#english)

## 中文

### 这是什么

`collect-design-assets` 是一个面向设计研究和素材整理的 Codex Skill。它用于搜索、筛选、下载、去重和组织图片、产品渲染图、视频/动效、网站案例以及可编辑素材，并保留来源与授权记录。

它适合需要形成可复查素材库或设计交接包的任务，不适合单纯查一个链接、生成新素材或对已选素材进行普通编辑。

### 如何调用

在 Codex 中显式调用：

```text
$collect-design-assets 为智能硬件配网体验收集设计参考，优先官方来源，整理来源、授权和预览图。
```

也可以直接描述收集目标，Codex 会在需求匹配时自动选择该 Skill。

建议在请求中说明：

- 素材类型：图片、产品渲染图、视频/动效、网站案例或可编辑源文件；
- 设计用途和目标受众；
- 期望数量、覆盖范围或精选程度；
- 优先或禁止的来源；
- 分辨率、尺寸、时长、格式等质量门槛；
- 授权要求：仅内部参考、需要署名或必须可商用；
- 命名语言、文件夹结构和交付格式。

示例：

```text
$collect-design-assets 收集 12 个智能家居设备配网与状态反馈案例。
优先官方产品页、官方视频和公开案例平台；排除纯广告氛围图和无来源素材。
输出精选素材、来源清单、授权备注、去重记录和一张总览图。
```

```text
$collect-design-assets 收集可编辑的点击、长按和滑动动效素材。
优先 Lottie JSON、dotLottie、SVG 或 AE 模板；记录作者、许可页面和下载日期，
并把授权不明确的项目放入待复核清单。
```

### 输出内容

根据任务，通常会得到：

- 按来源、类型、品牌、产品或场景整理的素材；
- 包含 URL、文件信息、哈希、标签、选择结果和授权备注的 manifest/index；
- README、来源索引或授权说明；
- 图片联系表、视频关键帧、故事板或案例总览；
- 重复项、淘汰项、失败项和授权不明项的记录。

### 工作方式

Skill 会先明确目标和来源边界，再建立候选清单；素材先进入工作区，经过质量筛选、分层去重和人工可视化复核后，才进入最终交付目录。每个入选素材都应能追溯到来源页面或原始 URL。

### 重要限制

- 不会绕过登录、付费、订阅或权限限制。
- 授权不明确的素材不会被宣称为可商用。
- 社交帖子和图片平台通常只适合发现灵感，不能自动视为可复用来源。
- 自动筛选不能替代最终视觉判断，应通过联系表、关键帧或总览图复核。

完整执行规则见 [SKILL.md](SKILL.md)。

## English

### What it is

`collect-design-assets` is a Codex Skill for design research and asset curation. It searches, filters, downloads, deduplicates, organizes, and documents images, product renders, video/motion references, website cases, and editable source assets while preserving provenance and licensing notes.

It is intended for reviewable collections and designer handoffs, not a one-link lookup, new asset generation, or ordinary editing of an already selected asset.

### How to invoke it

Invoke it explicitly in Codex:

```text
$collect-design-assets Collect design references for a smart-hardware onboarding experience, prioritize official sources, and organize provenance, licensing, and previews.
```

You can also describe the collection task normally. Codex may select the Skill automatically when the request matches its scope.

For best results, provide:

- asset types: images, product renders, video/motion, website cases, or editable source files;
- design purpose and audience;
- desired quantity, breadth, or curation level;
- preferred and prohibited sources;
- resolution, dimensions, duration, format, or other quality thresholds;
- licensing requirements: internal reference, attribution required, or commercial reuse;
- naming language, folder structure, and delivery formats.

Examples:

```text
$collect-design-assets Collect 12 smart-home onboarding and status-feedback cases.
Prioritize official product pages, official videos, and public case platforms; exclude pure advertising imagery and untraceable assets.
Deliver selected assets, a source list, licensing notes, deduplication records, and an overview sheet.
```

```text
$collect-design-assets Collect editable tap, long-press, and swipe motion assets.
Prefer Lottie JSON, dotLottie, SVG, or After Effects templates; record the author, license page, and download date,
and place unclear-license items in a review list.
```

### Outputs

Depending on the request, the Skill normally produces:

- assets organized by source, type, brand, product, or scenario;
- a manifest/index with URLs, file metadata, hashes, tags, decisions, and licensing notes;
- a README, source index, or licensing record;
- contact sheets, key frames, storyboards, or case-overview grids;
- records for duplicates, rejects, failures, and unclear licensing.

### How it works

The Skill defines the goal and source boundaries first, then builds a candidate list. Assets enter a working area before quality screening, layered deduplication, and visual review. Only selected items enter the final delivery folder, and each selected asset should remain traceable to a source page or original URL.

### Important limitations

- It does not bypass login, payment, subscription, or permission barriers.
- Assets with unclear licensing are not presented as commercially reusable.
- Social posts and image platforms are usually discovery sources, not automatic reuse permission.
- Automated filters do not replace final visual judgment; review contact sheets, key frames, or overview grids.

See [SKILL.md](SKILL.md) for the complete execution contract.
