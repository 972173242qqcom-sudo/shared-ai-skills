# 使用教程 / User guide — V1.1

## 中文

### 1. 安装

需要 Codex、本地 Python 3.10+、Pillow，以及可用的 FFmpeg/FFprobe。自动抠像和 HEVC Alpha 编码使用 macOS 工具链；Lottie PNG 序列打包与 GIF 时间线工具可以跨平台运行。

```bash
python3 -m pip install Pillow
```

从公开仓库下载整个 `skills/process-transparent-video` 文件夹（私有仓库中位于 `skills/video/process-transparent-video`），复制到 `~/.codex/skills/process-transparent-video`。如果此位置已有旧版，先备份再替换；不要把两个同名 skill 同时放进扫描目录。重新打开会话，使用 `$process-transparent-video` 调用。命令行示例均在 skill 文件夹内运行。macOS 自动抠像首次配置：

```bash
bash scripts/setup_macos.sh
```

### 2. 准备输入

提供视频或 PNG 序列路径，写明目标平台、MOV/GIF/Lottie、完整动作还是末帧停留、时长与单文件大小限制。PNG 名称按 `frame_000001.png` 排序，画布一致。已有 Alpha 的输入优先直接保留，不必重新抠像。源文件不覆盖，输出到新目录。

### 3. 透明 MOV

```bash
python3 scripts/transparent_video.py inspect input.mp4
python3 scripts/transparent_video.py matte input.mp4 master.mov
python3 scripts/transparent_video.py encode master.mov delivery.mov --format hevc-alpha --duration 3 --max-mb 5
python3 scripts/transparent_video.py verify delivery.mov --duration 3 --max-mb 5 --qc-dir delivery_qc
```

Apple HEVC 辅助 Alpha 必须经原生解码验证。普通播放器显示黑底时，先判断播放器是否支持，不要立即重新抠像。

### 4. Lottie（重点）

产品渲染视频转换为**位图序列型 Lottie**，保留半透明，但不会自动变成矢量动画。默认内嵌无损 PNG；JSON 可独立携带图片，但图片越多，运行内存越大。

已有正确透明 MOV 时，可先由已验证能保留该格式 Alpha 的解码器生成 PNG。ProRes 示例：

```bash
ffmpeg -i master.mov -fps_mode passthrough frames/frame_%06d.png
python3 scripts/lottie_sequence.py build frames animation.json --duration 3 --max-mb 5
python3 scripts/lottie_sequence.py verify animation.json --frames frames --max-mb 5
```

先创建 `frames` 目录。检查 PNG 的实际 Alpha 与边缘；HEVC Alpha 不应直接假设 FFmpeg 能保留。工具将 N 张图均匀放入指定时长，原有可变延时/额外定格需要先整理成对应时间线。输入帧名称只按字典序排序。

超过大小限制时命令会失败，文件作为候选保留；不能把它当作达标交付。先压缩 PNG、去重，再按显示尺寸缩小整组画布重建；不要默默抽帧或改颜色。

验证报告中的 `source_comparison: PASS` 表示逐帧 Alpha 和可见 RGB 一致；`target_player: not_tested` 表示尚未在目标播放器验收。需要在实际 App/网页播放器测试透明、位置、循环、性能。该验证器只支持本工具导出的子集，不是通用 Lottie 校验器。没有承诺原生矢量或 `.lottie` 打包功能。

### 5. GIF 优化与检查

```bash
python3 scripts/gif_timeline.py input.gif
python3 scripts/gif_timeline.py input.gif --merge-to merged.gif
```

合并工具比较完整视觉时间线；如果 Pillow 重新量化改变像素，会删除不合格候选并退出。通过验证也不保证体积一定减少，比较实际字节后选更小版本。复杂 GIF 可采用保留调色板的块级合并，再运行独立时间线对比。

需要生成 GIF 时，让 Codex 按 [GIF 规则](references/gif-production.md) 制作：透明索引独占、关键色全帧取样、保留蓝灯等细节、按实际延时检查。当前通用 CLI 没有“一键全自动优化 GIF”承诺。GIF 的二值透明无法真正保留连续半透明；渐隐质量优先可选 Lottie/MOV，指定固定背景时可另做烘焙背景版本。

### 6. 验收与交付

确认时长、完整动作或定格意图、总字节（1MB=1,000,000 字节）、尺寸、Alpha、颜色、孔洞、边缘和循环。短片优先逐帧对比，附浅/深/彩色底检查图。最终只交付请求的格式与必要报告，标出哪些目标播放器已经实测、哪些没有。

提示词见 [PROMPTS.md](PROMPTS.md)。开发者回归检查：`python3 scripts/test_regressions.py`。

## English

Copy the entire skill folder to `~/.codex/skills/process-transparent-video`, backing up an existing installation first. Start a new Codex chat and invoke `$process-transparent-video`. Install Python 3.10+, Pillow and FFmpeg/FFprobe. Run `scripts/setup_macos.sh` for the bundled macOS matting pipeline. Run all example commands from the skill directory.

Provide source paths, target runtime, formats, full-action versus final-hold intent, duration and per-file byte limit. Keep originals. Existing Alpha should be preserved, not rematted unnecessarily.

For raster Lottie, prepare verified straight-RGBA PNGs on a common canvas with zero-padded filenames. Run the `lottie_sequence.py build` and `verify` commands above. The exporter embeds lossless PNGs, crops transparent margins with placement offsets, reuses duplicate images and compares every source instant. All N frames receive uniform timing over the requested duration; variable delays must be prepared separately. This creates raster-sequence Lottie, not editable vectors or a `.lottie` archive.

A size-budget failure leaves a candidate, not an accepted delivery. Reduce canvas dimensions only after lossless optimizations, rebuild from the source frames and disclose the chosen dimensions. The verifier supports this exporter's subset only. Structural/source comparison does not establish target-player compatibility: test the actual player/renderer/version for soft Alpha, cropping, loop, timing and memory use.

For GIF, inspect timing with `gif_timeline.py`; its optional merge is accepted only after full visual-timeline equivalence. Palette requantization may cause safe failure. Compare byte sizes before selecting the result. Protect small critical colors and reserved transparency indices. GIF has binary Alpha; prefer MOV/Lottie when smooth partial transparency is essential.

Use [PROMPTS.md](PROMPTS.md) for ready-to-copy requests and [SKILL.md](SKILL.md) for the execution workflow.
