# 输入、风格包与输出

## 任务

UTF-8 JSONL，一行一张，允许 BOM。`id` 限英文数字、短横线、下划线且不重复，`topic` 必填。主题可中文，文件名使用稳定 ID，不拼接主题为路径。

```json
{"id":"001","topic":"周末阅读","scene":"一位成人坐在巨大折页旁阅读","composition":"斜向近景"}
```

可选：`size:[1080,1920]`、`must_show` 字符串列表、`character_lock` 主角描述。不指定角色锁时不强制同一主角。文字任务必填原文 `copy`，`copy_layout` 可为 `center` 或 `vertical`，用换行分行/分列。任务表不重复风格描述，助手先丰富故事再写入 `scene`。

## 风格包 v1

```json
{
  "schema_version":1,
  "id":"my-style",
  "version":"1.0.0",
  "category":"illustration",
  "name":"自己的系列",
  "default_size":[1080,1920],
  "style_prompt":"完整描述色彩、线条、材质和氛围",
  "avoid":["不适用于本系列的特征"],
  "composition_presets":["仰视动势","俯视物件","安静近景"],
  "text_mode":"none",
  "review_checks":["style","semantic","clean"]
}
```

`category` 为 `illustration`、`wallpaper`、`photo-cover`；`text_mode` 为 `none` 或 `overlay`。这是脚本当前范围，其他媒介可扩展但不能假称已支持。默认尺寸可被任务覆盖，实际生成后必须测量。

文字包需 `text_mode:"overlay"`、`text_color:"#RRGGBB"`，可选 `text_area:[left,top,right,bottom]`，坐标0–1。审核项必须含 `text`。字体以命令参数提供，不写死本机路径。仅暖色壁纸示例有暖色约束。

## 输出

```text
batch/
  plan.json                 风格快照、全部任务、提示词
  manifests/<id>.json       单张施工单
  originals/<id>.<ext>      输入原字节
  finals/<id>.png           交付图
  records/<id>.json         哈希、尺寸、裁切、字体及排字证据
  reviews/<id>.json         有责任主体及证据的视觉检查
  report.json               技术和视觉状态
  contact-sheet.jpg         整批总览
  preview.html              图片内嵌，可单独发送
```

审核 JSON：

```json
{
  "reviewer":"assistant-visual",
  "checks":{
    "style":{"pass":true,"evidence":"保留三至六色平涂与简化人物"},
    "semantic":{"pass":true,"evidence":"主题动作在缩略图可辨认"},
    "clean":{"pass":true,"evidence":"已查看主体与四周，无乱码和多余肢体"}
  },
  "notes":"记录检查限制或修改理由"
}
```

壁纸再加 `text`：逐字对比终稿与 `copy`，不能只对比输入字符串。审核绑定当前计划及终稿 SHA-256，改图后旧审核失效。脚本只验证记录格式，不能证实 evidence 内容，必须实际看图。

输出批次必须不存在，避免误覆盖。一个任务一个终稿，候选图不计为额外交付。需要两个候选时分别生成并选一个导入，不把双候选作为默认开销。返工用新目录，只含失败 ID，另记母批次。生成式图像无法保证像素复现；确定性排字也取决于相同字体与运行环境。
