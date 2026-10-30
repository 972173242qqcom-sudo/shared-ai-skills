# 可复制提示词 / Copyable prompts

将占位路径换成实际路径。未给定目标播放器时，说明用途即可；助手应报告未经实测的兼容性。

## 1. 产品视频 → Lottie（常用）

```text
$process-transparent-video
输入：[视频或透明PNG序列路径]
请制作位图序列型 Lottie JSON，用于 [网页 / iOS / Android + 播放器名称和版本（如已知）]。
保留完整动作，均匀重定时为3秒，背景透明，保留柔和半透明边缘、Logo、孔洞和指示灯原色。
单个JSON不超过5MB，按目标显示尺寸[宽×高]尽量保持清晰。
优先无损PNG、裁空白和资产去重，不能为达标直接遗漏动作。
保留源文件，放入新交付目录；逐帧验证Alpha和可见RGB，记录最终字节、尺寸、时长。
目标播放器能实测就实测；不能实测请明确标注，不要把结构通过写成播放通过。
```

## 2. 同时交付 MOV + GIF + Lottie

```text
$process-transparent-video
处理[路径]，交付透明MOV、透明GIF、位图序列型Lottie JSON。
完整动作3秒，各文件5MB以内，清晰度、原色、边缘和流畅度优先。
MOV用于[平台]，GIF用于[用途]，Lottie用于[播放器]。
从同一高质量透明源分别导出；GIF先合并重复状态再考虑降质，并保护小面积灯光颜色。
不要覆盖源文件，附逐帧/时间线验证和浅、深、彩色底检查图。
```

## 3. GIF 压缩、保原色

```text
$process-transparent-video
把[GIF路径]压到5MB以内，保留透明、完整时长、循环、黑色细节和蓝灯颜色。
先尝试合并完全相同状态并累计延时，逐帧RGBA与时间线比较通过后再接受。
若仍超限，优先适度降低分辨率，比较调色板与抖色方案；不要让透明索引误删黑色。
报告画面有无改变、存储帧数与动作采样的区别，以及最终尺寸和字节。
```

## 4. 仅延长末帧定格

```text
$process-transparent-video
对[路径]保留前段动作速度，只延长最后[蓝灯亮起]状态，使总长3秒。
不要把整段动画再次加速或追加第一帧。保留透明、原色与清晰度。
输出[GIF/Lottie]，单个5MB内，核对末帧状态、停留时长和循环衔接。
```

## 5. 已有透明文件出现黑底

```text
$process-transparent-video
[路径]在[目标软件/播放器]显示黑底。先检查真实Alpha和解码兼容性。
不要直接重新抠像或烘焙背景。保留源文件，给出适配该平台的Lottie/GIF/MOV方案，
说明哪些已实测，哪些需要目标环境验收。
```

## 6. 必须是可编辑矢量 Lottie

```text
$process-transparent-video
我要可编辑、可缩放的矢量Lottie，用于[平台]。输入是[AE/矢量文件/视频路径]。
先判断是否具备矢量源；视频包装成位图序列不能算矢量交付。
如需重建，先说明可保留的视觉与动作、需要重建的部分及方案，再按确定的范围执行。
```

## English: Lottie delivery

```text
$process-transparent-video
Convert [source path] to embedded raster-sequence Lottie JSON for [player/platform/version].
Preserve the full action, original colors, small LEDs, holes and soft Alpha; retime uniformly to 3 seconds.
Keep the JSON under 5 decimal MB at the highest practical resolution for [display size].
Try lossless PNG optimization, cropping and deduplication before reducing dimensions.
Keep originals and write to a new delivery folder. Compare every source instant's Alpha and visible RGB.
Report exact bytes, dimensions, timing, representation type and target-player test status separately.
```

## English: GIF optimization

```text
$process-transparent-video
Optimize [GIF path] under 5 MB while preserving transparency, original duration, loop and LED colors.
Try merging identical visual states first and verify full RGBA timeline equivalence.
Protect opaque dark pixels from the reserved transparent palette index.
If lossy changes are necessary, compare resolution/palette/dithering options and report the chosen tradeoff.
```
