# Define Product Requirements

[中文](#中文) | [English](#english)

## 中文

### 这是什么

`define-product-requirements` 是一个把模糊产品需求转化为可追溯、可验证 Product Brief 的 Codex Skill。它适用于工业设计、消费产品、智能硬件、软件、服务和其他需要在研究或概念阶段前明确问题、范围与验证计划的项目。

它提供三种工作模式：

- `clarify`：整理原始需求，区分 E（证据）、H（假设）、D（决定）和 U（未知），发现冲突并排列澄清问题；
- `build`：生成或修订完整 Product Brief、范围边界、成功标准和最小验证计划；
- `audit`：在竞品研究或概念生成前，对已有任务书做反方审查。

### 如何调用

第一次面对模糊需求时：

```text
$define-product-requirements 进入 clarify 模式。

原始需求：做一个与 AI Agent 有关的桌面硬件。
已知背景：我会同时运行多个 Agent 任务，本阶段只完成概念设计提案。

请先建立 E/H/D/U 信息表，指出会改变项目方向的信息缺口，
不要生成造型，不要编造用户研究、市场数据或工程结论。
```

已有资料、需要生成任务书时：

```text
$define-product-requirements 进入 build 模式。

这是原始需求、真实观察、已知约束和 E/H/D/U 信息表：
【粘贴资料】

请生成完整 Product Brief、准备度评分和最小验证计划。
证据不足的内容保留为 H 或 U。
```

准备进入研究或概念阶段前：

```text
$define-product-requirements 进入 audit 模式，审查这份 Product Brief：
【粘贴任务书】

检查伪事实、解决方案先行、过宽用户与场景、目标冲突、
无法检查的成功标准和会导致概念无限发散的表达。
```

也可以直接描述任务。Codex 会在请求符合范围时自动选择该 Skill。

### 输入与输出

常见输入：

- 客户、团队或个人的原始需求；
- 项目背景、商业目标和交付范围；
- 用户、场景、任务、当前替代方案与约束；
- 访谈、观察、客服、销售、竞品或其他已有证据；
- 现有 Product Brief 或待审查任务书。

常见输出：

- 中性项目复述和 E/H/D/U 信息表；
- 信息冲突、关键未知与按风险排序的澄清问题；
- 核心用户、场景、任务链和问题定义；
- Job Statement、How Might We 和价值假设；
- Must / Should / Won't、Anti-goals 和目标冲突；
- 可观察的成功标准和最小验证计划；
- 20 分准备度审查与下一阶段建议；
- 保存到项目中时，可输出输入索引、信息表、Product Brief、验证计划和决定日志。

### 文件结构

```text
define-product-requirements/
├── SKILL.md
├── README.md
├── agents/
│   └── openai.yaml
├── references/
│   └── brief-schema.md
└── assets/
    └── product-brief-template.md
```

`references/brief-schema.md` 定义完整任务书、准备度评分与审查分类。`assets/product-brief-template.md` 是可以复制和修改的中文空白模板。

### 工作方式

Skill 不要求资料完整后才开始工作。信息不足时，它会生成暂定任务书，保留未知，并说明哪些决定因此不能完成。所有关键内容按 E/H/D/U 管理，避免把单次观察、AI 推理或营销说法升级为普遍事实。

任务书只有在核心用户、场景、任务、阻碍、范围、成功标准和下一步验证都足够清楚时，才会被判断为可以进入定向研究或受控概念探索。

### 依赖与限制

- 没有固定模型、付费 API、Python 包或外部脚本依赖。
- Skill 不会编造访谈、市场规模、法规、价格、测试结果或工程可行性。
- Skill 不会因为原始需求要求硬件，就自动把硬件当作正确答案。
- `高级`、`智能`、`年轻`、`简约`、`好用` 等词必须转译为可观察要求后才能进入任务书。
- 医疗、金融、汽车等强监管领域仍需要相应法规、专业人员和验证材料。
- 其他支持 Skill 的 AI 工具可以读取完整文件夹；原生安装方式和可用权限取决于具体客户端。

完整执行规则见 [SKILL.md](SKILL.md)。

## English

### What it is

`define-product-requirements` is a Codex Skill that turns vague product requests into traceable, testable Product Briefs. It supports industrial design, consumer products, smart hardware, software, services, and other projects that need a clear problem, scope, and validation plan before research or concept work.

It provides three modes:

- `clarify`: organize raw input, separate evidence (E), hypotheses (H), decisions (D), and unknowns (U), expose conflicts, and prioritize clarification questions;
- `build`: create or revise a complete Product Brief, scope boundaries, success criteria, and minimum validation plan;
- `audit`: challenge an existing brief before competitor research or concept generation.

### How to invoke it

For an early, vague request:

```text
$define-product-requirements Enter clarify mode.

Original request: Build a desktop device related to AI agents.
Known context: I run several agent tasks in parallel, and this stage ends with a concept proposal.

Create an E/H/D/U register and identify the gaps that could change the project direction.
Do not generate form concepts or invent user research, market data, or engineering conclusions.
```

When enough material exists to build a brief:

```text
$define-product-requirements Enter build mode.

Here are the original request, real observations, constraints, and E/H/D/U register:
[paste material]

Create a complete Product Brief, readiness score, and minimum validation plan.
Keep unsupported claims as H or U.
```

Before research or concept work:

```text
$define-product-requirements Enter audit mode and review this Product Brief:
[paste brief]

Check for unsupported facts, solution-first framing, overly broad users or scenarios,
conflicting goals, untestable success criteria, and language that permits uncontrolled scope.
```

You can also describe the task normally. Codex may select the Skill automatically when the request matches its scope.

### Inputs and outputs

Typical inputs:

- an original request from a client, team, or individual;
- project context, business goals, and delivery boundaries;
- users, scenarios, tasks, current workarounds, and constraints;
- interviews, observations, support or sales material, competitor evidence, and other sources;
- an existing Product Brief or requirement document to audit.

Typical outputs:

- a neutral project restatement and E/H/D/U register;
- conflicts, critical unknowns, and risk-ranked clarification questions;
- target users, scenarios, task chains, and a problem statement;
- a Job Statement, How Might We question, and value hypothesis;
- Must / Should / Won't boundaries, anti-goals, and goal conflicts;
- observable success criteria and a minimum validation plan;
- a 20-point readiness review and next-stage recommendation;
- optional saved files for source indexing, the evidence register, Product Brief, validation plan, and decision log.

### Package structure

```text
define-product-requirements/
├── SKILL.md
├── README.md
├── agents/
│   └── openai.yaml
├── references/
│   └── brief-schema.md
└── assets/
    └── product-brief-template.md
```

`references/brief-schema.md` defines the complete brief, readiness score, and audit classifications. `assets/product-brief-template.md` is an editable Chinese template.

### How it works

The Skill does not wait for perfect information. When evidence is incomplete, it creates a provisional brief, preserves unknowns, and states which decisions remain blocked. Consequential statements use E/H/D/U status so that observations, model inference, and marketing claims are not silently promoted into general facts.

A brief is considered ready only when the primary user, scenario, task, obstacle, scope, success criteria, and next validation action are clear enough to support targeted research or controlled concept exploration.

### Dependencies and limitations

- There is no fixed-model, paid-API, Python-package, or external-script dependency.
- The Skill does not invent interviews, market size, regulations, prices, test results, or engineering feasibility.
- A request for hardware does not make hardware the correct answer by default.
- Terms such as “premium,” “smart,” “young,” “minimal,” or “easy to use” must be translated into observable requirements.
- Regulated fields such as healthcare, finance, and automotive still require appropriate regulatory and professional evidence.
- Other Skill-capable AI tools can read the full package, but native installation and permissions depend on the host client.

See [SKILL.md](SKILL.md) for the complete execution contract.
