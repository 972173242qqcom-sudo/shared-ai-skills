# Map User Scenarios

[中文](#中文) | [English](#english)

## 中文

### 这是什么

`map-user-scenarios` 是一个把观察记录、访谈、使用日志和日记研究转成可追溯场景模型的 Codex Skill。它不会先虚构姓名、年龄和生活故事，而是从真实行为中建立核心用户、场景六格、任务流、断点、注意力等级和下一步验证计划。

它提供三种模式：

- `prepare`：还没有真实记录时，生成观察方案和可填写模板；
- `map`：把已有记录整理成行为型用户、场景、任务流和介入机会；
- `audit`：审查已有用户画像、旅程图或场景是否包含伪事实、过度概括和解决方案先行。

### 安装到 Codex

在支持 `$skill-installer` 的 Codex 中发送：

```text
$skill-installer 请从以下 GitHub 目录安装 map-user-scenarios：
https://github.com/972173242qqcom-sudo/shared-ai-skills/tree/main/skills/map-user-scenarios
```

也可以下载仓库，将完整的 `map-user-scenarios` 文件夹复制到 Codex 的用户 Skill 目录。安装后重启 Codex 或开启新会话。

### 如何调用

还没有研究记录时：

```text
$map-user-scenarios 进入 prepare 模式。

研究目标：判断多个 AI Agent 并行时，什么状态值得打断用户。
请生成一次真实任务观察的记录表，不要替我编造过程或结论。
```

已有观察或访谈时：

```text
$map-user-scenarios 进入 map 模式。

这是原始记录与来源索引：
【粘贴资料】

请建立行为型核心用户、场景六格、任务流、状态 × 注意力矩阵和下一步验证计划。
关键结论标记 E / H / D / U，并保留来源 ID。
```

准备进入概念设计前：

```text
$map-user-scenarios 进入 audit 模式，审查下面的用户画像与场景：
【粘贴内容】

找出虚构信息、证据过度概括、不可观察描述、缺失的任务恢复过程，
以及被过早写成产品功能的用户问题。
```

### 输出

完整项目包可以包含：

```text
01_source-index-and-boundary.md
02_behavioral-user-model.md
03_scenario-six-frames.md
04_task-flow-and-breakdowns.md
05_state-attention-matrix.md
06_scenario-priority-and-next-study.md
07_decision-and-change-log.md
```

`references/scenario-schema.md` 定义完整结构和审查标准；`assets/scenario-research-template.md` 是可直接复制的中文工作表。

### 依赖与限制

- 没有固定模型、付费 API、Python 包或外部脚本依赖。
- Skill 不会虚构参与者、访谈原话、时间、频率、情绪或测试结论。
- 单次自我观察可以用于启动假设，但不能证明更广泛用户都存在同一问题。
- 人口信息只有在影响人机、安全、可达性、法规或行为时才进入模型。
- 输出是研究与设计决策辅助，不等于市场验证或工程可行性结论。

## English

### What it is

`map-user-scenarios` turns observations, interviews, diary notes, and usage logs into traceable behavioral user models, six-frame scenarios, task flows, breakdowns, attention levels, and next-study plans. It avoids fictional demographic personas and keeps evidence separate from hypotheses and project decisions.

The Skill provides three modes:

- `prepare`: create a real-event observation plan and editable record sheet;
- `map`: synthesize supplied records into behavior, scenarios, flows, and intervention opportunities;
- `audit`: challenge an existing persona, journey, or scenario for invented facts, overgeneralization, and solution-first framing.

### Example

```text
$map-user-scenarios Enter map mode.

Here are the raw records and source index:
[paste material]

Create a behavioral user model, six-frame scenario, task flow,
state × attention matrix, and next validation plan.
Label consequential claims E / H / D / U and preserve source IDs.
```

### Outputs

A complete saved package may include a source index, behavioral user model, six-frame scenarios, task-flow and breakdown map, state-attention matrix, scenario priorities, next study, and decision log.

### Dependencies and limitations

- No fixed model, paid API, Python package, or external script is required.
- The Skill does not invent participants, quotations, timestamps, frequencies, emotions, or research findings.
- A single self-observation can start a hypothesis but cannot establish a population-wide truth.
- Demographics are included only when they materially affect behavior, access, ergonomics, safety, or regulation.
- Outputs support research and design decisions; they are not market validation or engineering proof.

See [SKILL.md](SKILL.md) for the execution contract.
