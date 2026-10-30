# Process Transparent Video — V1.1

[中文](#中文) | [English](#english)

[使用教程 / Tutorial](TUTORIAL.md) · [可复制提示词 / Prompts](PROMPTS.md) · [Lottie workflow](references/lottie-workflow.md)

V1.1 (2026-10-30): 正式支持位图序列 Lottie JSON；新增 GIF 关键色/透明索引/可变延时规则和回归检查。
Raster Lottie uses embedded lossless PNGs; it is not vectorization. Player compatibility must be verified separately.

## 中文

### 这是什么

`process-transparent-video` 是一个面向透明背景视频交付的 Codex Skill。它覆盖背景移除、Alpha 保留与检查、完整动作重定时、透明 MOV/WebM/GIF 与位图序列 Lottie JSON 导出、体积限制、边缘修复和多背景质检。

它不适合与透明通道无关的普通剪辑、字幕或调色任务。

### 如何调用

在 Codex 中显式调用：

```text
$process-transparent-video 把这个视频制作成透明背景 MOV，保留完整动作，并验证 Alpha 和边缘质量。
```

也可以直接描述任务，Codex 会在需求匹配时自动选择该 Skill。

建议在请求中说明：

- 源视频；
- 目标格式和使用场景；
- 是否需要保留完整动作；
- 目标时长、尺寸、帧率和最大文件体积；
- 是否保留并同步音频；
- 当前背景或 Alpha 状态；
- 需要重点保护或检查的浅色主体、Logo、孔洞、手指、阴影、反光或发光区域。

示例：

```text
$process-transparent-video 移除 input.mp4 的白色背景，保留完整动作并重定时到 3 秒；
输出适用于 macOS 应用的透明 MOV 和一个透明 GIF，单个文件不超过 2 MB；
保留源文件，并在浅色、深色和彩色背景上检查每一帧。
```

```text
$process-transparent-video 这个透明 MOV 在目标软件里显示为黑底。
先诊断 Alpha 和编解码兼容性，不要直接重新抠像；给出兼容格式或不透明预览的替代方案。
```

### 输出内容

根据任务，通常会得到：

- 高质量透明母版，例如 ProRes 4444 MOV；
- 面向目标平台的透明 MOV、WebM、GIF 或 PNG 序列；
- 时长、帧数、尺寸、码率、编解码器、Alpha 和音频验证结果；
- Alpha 图和浅色、深色、彩色背景合成质检图；
- 兼容性风险、质量取舍和失败原因说明。

默认保留源文件，并从透明母版分别生成各交付格式。

### 快速开始

核心环境：Python 3.10+、FFmpeg/FFprobe。自动语义抠像后端使用 macOS 的 Apple Vision。

新 Mac 可先运行：

```bash
bash scripts/setup_macos.sh
```

基本流程：

```bash
python3 scripts/transparent_video.py inspect "input.mp4"

python3 scripts/transparent_video.py matte "input.mp4" "master.mov"

python3 scripts/transparent_video.py encode "master.mov" "delivery.mov" \
  --format hevc-alpha --duration 3 --max-mb 2

python3 scripts/transparent_video.py verify "delivery.mov" \
  --duration 3 --max-mb 2 --qc-dir "delivery_qc"
```

### 格式选择

- ProRes 4444 MOV：适合作为高质量母版和交换格式，但文件较大。
- HEVC Alpha MOV：适合已验证支持的 Apple 运行环境，必须用能读取辅助 Alpha 的解码器验证。
- VP9 Alpha WebM：适合部分浏览器，某些编辑器会忽略 Alpha。
- 透明 GIF：兼容性广，但只有二值透明、无音频，并受颜色和体积限制。

### 重要限制

- 自动抠像不能可靠覆盖所有浅色产品、反光、手部、发光和封闭孔洞，困难素材需要局部修复。
- H.264 MP4 不能作为透明视频交付格式。
- 透明格式是否可用取决于目标软件的解码支持，文件带 Alpha 元数据不等于实际可见透明。
- 严格体积限制可能需要在分辨率、颜色、帧率和边缘质量之间取舍。

完整执行规则见 [SKILL.md](SKILL.md)。

## English

### What it is

`process-transparent-video` is a Codex Skill for transparent-background video delivery. It covers background removal, Alpha preservation and inspection, full-action retiming, transparent MOV/WebM/GIF and raster-sequence Lottie JSON export, file-size limits, edge repair, and multi-background QA.

It is not intended for ordinary cuts, captions, or color grading when transparency is not part of the task.

### How to invoke it

Invoke it explicitly in Codex:

```text
$process-transparent-video Turn this clip into a transparent MOV, preserve the full action, and verify Alpha and edge quality.
```

You can also describe the task normally. Codex may select the Skill automatically when the request matches its scope.

For best results, provide:

- the source video;
- target format and application;
- whether the full action must be preserved;
- target duration, dimensions, frame rate, and maximum file size;
- whether audio must be preserved and retimed;
- the current background or Alpha state;
- pale subjects, logos, holes, fingers, shadows, reflections, or glow that need special protection or inspection.

Examples:

```text
$process-transparent-video Remove the white background from input.mp4 and preserve the complete action while retiming it to 3 seconds.
Export a transparent MOV for a macOS application and a transparent GIF, each under 2 MB.
Preserve the source and inspect every frame over light, dark, and saturated backgrounds.
```

```text
$process-transparent-video This transparent MOV displays with a black background in the target application.
Diagnose Alpha and codec compatibility before rematting it, then recommend a compatible format or opaque-preview fallback.
```

### Outputs

Depending on the request, the Skill normally produces:

- a high-quality transparent master such as ProRes 4444 MOV;
- target-specific transparent MOV, WebM, GIF, or PNG sequences;
- duration, frame-count, dimensions, bitrate, codec, Alpha, and audio verification;
- Alpha images and composites over light, dark, and saturated backgrounds;
- compatibility caveats, quality tradeoffs, and failure notes.

The source is preserved by default, and each delivery format is generated independently from the transparent master.

### Quick start

Core requirements: Python 3.10+ and FFmpeg/FFprobe. The bundled automatic semantic-matting backend uses Apple Vision on macOS.

On a new Mac, run:

```bash
bash scripts/setup_macos.sh
```

Basic workflow:

```bash
python3 scripts/transparent_video.py inspect "input.mp4"

python3 scripts/transparent_video.py matte "input.mp4" "master.mov"

python3 scripts/transparent_video.py encode "master.mov" "delivery.mov" \
  --format hevc-alpha --duration 3 --max-mb 2

python3 scripts/transparent_video.py verify "delivery.mov" \
  --duration 3 --max-mb 2 --qc-dir "delivery_qc"
```

### Choosing a format

- ProRes 4444 MOV: a high-quality master and interchange format, but large.
- HEVC Alpha MOV: suitable for verified Apple runtimes; verify with a decoder that exposes auxiliary Alpha.
- VP9 Alpha WebM: suitable for some browsers; some editors ignore its Alpha channel.
- Transparent GIF: broadly compatible, but limited to binary transparency, no audio, and constrained color/size quality.

### Important limitations

- Automatic matting cannot reliably handle every pale product, reflection, hand, glow, or enclosed opening; difficult clips need local repair.
- H.264 MP4 is not a transparent delivery format.
- Format metadata is not proof that the target application will display transparency; decoder support must be verified.
- Strict size limits may require tradeoffs among resolution, color, cadence, and edge quality.

See [SKILL.md](SKILL.md) for the complete execution contract.
