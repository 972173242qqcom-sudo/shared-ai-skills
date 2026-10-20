# Competitive Product Analysis

[中文](#中文) | [English](#english)

## 中文

### 这是什么

`competitive-product-analysis` 是一个将已收集的竞品证据转化为比较模型、机会假设和产品决策的 Codex Skill。它适用于实体产品、软件/SaaS、服务、平台、B2B 解决方案以及消费品和零售品类。

它负责分析与决策，不负责大范围搜索、下载、去重或素材授权整理；这些工作应由资料收集 Skill 完成。

### 如何调用

在 Codex 中显式调用：

```text
$competitive-product-analysis 分析这批智能家电竞品资料。
先检查证据和图片覆盖率，再输出比较矩阵、机会地图、推荐方向和验证计划。
```

也可以直接描述竞品分析任务，Codex 会在需求匹配时自动选择该 Skill。

建议在请求中说明：

- 要支持的业务或产品决策；
- 目标用户、场景、地区和产品阶段；
- 已有竞品清单、证据表、图片和来源记录；
- 分析对象属于硬件、软件、服务、平台、B2B 还是消费品；
- 主要分析视角，例如产品体验、定位、商业模式、渠道品牌或合规；
- 希望输出 HTML、DOCX、演示文稿、矩阵还是简短评审。

示例：

```text
$competitive-product-analysis 分析 8 款团队协作 SaaS。
重点比较激活、核心工作流、权限、集成、定价和切换成本，
区分事实、假设与决策，最后给出 3 个可证伪的产品机会。
```

```text
$competitive-product-analysis 分析这批护肤品牌资料。
使用消费品/零售与渠道品牌维度，比较定位、配方与宣称、包装、
价格带、渠道和复购机制，输出机会地图和上市验证计划。
```

### 输入与输出

常见输入：

- 竞品清单、证据表和来源 URL；
- 图片或素材 manifest；
- 用户、场景、地区、价格和市场状态；
- 当前产品方向、约束和需要支持的决策。

常见输出：

- 研究问题、范围、证据覆盖率和已知缺口；
- 直接竞品、相邻方案和类比体验三圈竞品池；
- 按品类选择的比较矩阵和评分依据；
- 代表性深度分析、失败案例和关键权衡；
- 机会地图、3—5 个可验证机会假设；
- 推荐方向、明确的不要做事项、风险和验证计划；
- HTML、DOCX、Slides 或简短决策报告。

### 完整性审计脚本

`scripts/audit_package.py` 使用 Python 标准库检查竞品数量、图片覆盖、缺失状态/价格/来源、重复名称和稳定 ID。没有第三方 Python 包依赖。

```bash
python scripts/audit_package.py competitors.csv \
  --assets assets.csv \
  --require status,price,source \
  --json audit.json
```

对于没有公开价格的 B2B 或服务产品，可以调整检查项：

```bash
python scripts/audit_package.py competitors.csv --require status,source
```

### 工作方式

Skill 先明确要支持的决策，再识别产品类型并选择对应维度包。分析过程中区分证据（E）、假设（H）和决策（D），评分必须保留证据与理由。最终机会必须包含目标用户、未满足任务、机制、最低成本验证、主要风险和证伪条件。

### 依赖与限制

- Skill 本身没有付费 API、固定模型或第三方 Python 包依赖。
- 实际分析可能需要联网搜索、网页访问、文件读取、图片处理或文档生成能力，取决于任务。
- 不会把缺失证据自动当作中性评分，也不会静默删除缺图或缺来源的竞品。
- 分数依赖具体决策，不能作为跨项目的绝对排名。
- 医疗、金融、汽车等强监管领域仍需要相应法规和专业参考材料。
- 资料不足时应返回定向补充清单，而不是无边界地重新搜索。

完整执行规则见 [SKILL.md](SKILL.md)。

## English

### What it is

`competitive-product-analysis` is a Codex Skill that turns collected competitor evidence into comparison models, opportunity hypotheses, and product decisions. It supports physical products, software/SaaS, services, platforms, B2B solutions, and consumer or retail categories.

It owns analysis and decision synthesis, not broad discovery, downloading, deduplication, or licensing work. Those tasks belong in an asset or research collection workflow.

### How to invoke it

Invoke it explicitly in Codex:

```text
$competitive-product-analysis Analyze this smart-appliance competitor package.
Audit evidence and image coverage first, then produce a comparison matrix,
opportunity map, recommendation, and validation plan.
```

You can also describe the analysis task normally. Codex may select the Skill automatically when the request matches its scope.

For best results, provide:

- the business or product decision the analysis must support;
- target users, scenarios, region, and product stage;
- competitor tables, evidence records, images, and source manifests;
- the offering type: hardware, software, service, platform, B2B, or consumer goods;
- the primary lens: product experience, positioning, business model, channel and brand, technology, or compliance;
- the desired output format, such as HTML, DOCX, slides, a matrix, or a short review.

Examples:

```text
$competitive-product-analysis Analyze eight team-collaboration SaaS products.
Compare activation, core workflow, permissions, integrations, pricing, and switching cost.
Separate evidence, hypotheses, and decisions, then propose three falsifiable opportunities.
```

```text
$competitive-product-analysis Analyze this skincare competitor package.
Use the consumer-goods/retail and channel/brand dimensions to compare positioning,
formulation and claims, packaging, price architecture, channels, and repeat purchase.
```

### Inputs and outputs

Typical inputs:

- competitor, evidence, and source tables;
- image or asset manifests;
- user, scenario, region, price, and market-status context;
- the current product direction, constraints, and target decision.

Typical outputs:

- the research question, scope, coverage, and evidence gaps;
- direct competitors, adjacent solutions, and analogous experiences;
- category-appropriate comparison dimensions and score rationale;
- representative deep dives, negative cases, and trade-offs;
- an opportunity map and three to five testable hypotheses;
- a recommendation, anti-goals, risks, and validation plan;
- HTML, DOCX, slides, or a compact decision review.

### Package-audit script

`scripts/audit_package.py` uses only the Python standard library. It checks competitor count, image coverage, missing status/price/source fields, duplicate names, and stable IDs.

```bash
python scripts/audit_package.py competitors.csv \
  --assets assets.csv \
  --require status,price,source \
  --json audit.json
```

For B2B or service offerings without public pricing, adjust the required groups:

```bash
python scripts/audit_package.py competitors.csv --require status,source
```

### How it works

The Skill defines the target decision first, classifies the offering type, and selects the relevant dimension pack. It separates evidence (E), hypotheses (H), and decisions (D); scores retain their evidence and rationale. Each final opportunity includes a target user, unmet task, mechanism, lowest-cost test, primary risk, and falsification condition.

### Dependencies and limitations

- The Skill has no paid API, fixed-model, or third-party Python-package dependency.
- A real analysis may require web research, browser access, file inspection, image processing, or document-generation tools depending on the request.
- Missing evidence is not converted into a neutral score, and competitors with missing images or sources are not silently removed.
- Scores are decision-specific and should not be treated as universal rankings.
- Regulated categories such as healthcare, finance, and automotive still require domain-specific regulatory and expert references.
- When evidence is insufficient, the workflow returns a targeted collection request instead of restarting unbounded research.

See [SKILL.md](SKILL.md) for the complete execution contract.
