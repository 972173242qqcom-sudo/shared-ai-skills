# Generate Industrial Design Sketches

[中文](#中文) | [English](#english)

## 中文

### 这是什么

`generate-industrial-design-sketches` 是一个面向工业设计前期探索的 Codex Skill。它把 Product Brief、用户场景、竞品结论、机会假设、设计限制和参考图，转成可比较的黑白草图批次，并用统一标准筛选出值得继续验证的方向。

它支持四种模式：

- `plan`：只生成草图计划与提示词，不生成图片；
- `explore`：围绕明确变量分轮探索轮廓、交互、状态和结构；
- `shortlist`：评审已有草图，保留两到四个有本质差异的方向；
- `iterate`：固定方向，只修改一个尚未解决的关系。

### 安装到 Codex

在支持 `$skill-installer` 的 Codex 中发送：

```text
$skill-installer 请从以下 GitHub 目录安装 generate-industrial-design-sketches：
https://github.com/972173242qqcom-sudo/shared-ai-skills/tree/main/skills/generate-industrial-design-sketches
```

也可以下载仓库，将完整的 `generate-industrial-design-sketches` 文件夹复制到 Codex 的用户 Skill 目录。Windows 默认位置为 `%USERPROFILE%\.codex\skills\`，macOS / Linux 通常为 `~/.codex/skills/`。安装后重启 Codex 或开启新会话。

### 如何调用

先生成一批草图：

```text
$generate-industrial-design-sketches 进入 explore 模式。

这是竞品结论、用户场景和设计限制：
【粘贴内容】

第一轮只探索整体体量、状态表达和核心物理操作。
请生成3张黑白工业设计草图板，每张展示若干有本质差异的候选。
不要加入最终颜色与材质，不要生成广告效果图，不要复制竞品的标志性外形。
```

再筛选方向：

```text
$generate-industrial-design-sketches 进入 shortlist 模式。

请评审这些草图：
【附上图片或文件夹】

按场景契合、机制清晰、状态可读、有依据的差异、验证成本和禁止项进行比较。
只保留3个产品逻辑不同的方向，并写清保留理由、主动放弃、最大未知和最低成本测试。
```

### 输出

完整项目包可以包含草图输入与边界、批次计划、草图图片、评审矩阵、保留方向和决策记录。`assets/sketch-brief-template.md` 与 `assets/sketch-review-matrix.md` 可直接复制使用。

### 依赖与限制

- 需要宿主提供图像生成能力，才能直接输出草图图片；否则 Skill 会生成可转交给图片工具的完整 Brief 与提示词。
- Skill 不证明工程、生产、市场或人体工学可行性。
- 参考图只用于提取比例、控制层级、接缝、灯光和表面转折等属性，不用于复刻产品识别特征。
- 默认输出前期黑白草图，不提前进入最终 CMF 或广告级渲染。

## English

### What it is

`generate-industrial-design-sketches` turns product briefs, user scenarios, competitor findings, opportunity hypotheses, constraints, and reference images into controlled industrial-design sketch batches and traceable shortlists.

It provides four modes: `plan`, `explore`, `shortlist`, and `iterate`. The workflow separates silhouette and massing, interaction and state, structural combinations, and focused iteration so candidates remain comparable.

### Example

```text
$generate-industrial-design-sketches Enter explore mode.

Here are the user scenario, competitor findings, and constraints:
[paste material]

Create three black-and-white industrial-design sketch boards.
Change only massing, state expression, and primary physical interaction in this round.
Avoid final CMF, advertising renders, logos, and distinctive competitor forms.
```

### Outputs

A complete package may include an input boundary, batch plan, sketch boards, review matrix, shortlisted directions, and a decision log.

### Dependencies and limitations

- Direct image output requires an image-generation tool in the host environment; otherwise the Skill returns complete briefs and prompts.
- Sketches do not prove engineering, manufacturing, ergonomics, market, or safety feasibility.
- Reference products are translated into transferable attributes rather than copied.
- Early exploration defaults to black-and-white sketch language instead of final rendering.

See [SKILL.md](SKILL.md) for the execution contract.
