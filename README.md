# Shared AI Skills

可安装、可复用的 AI 工作流。目前提供三个 Skills：

| Skill | 功能 | 使用说明 |
| --- | --- | --- |
| [collect-design-assets](skills/collect-design-assets/SKILL.md) | 设计素材搜索、筛选、下载、去重、整理和来源记录 | [中文 / English](skills/collect-design-assets/README.md) |
| [competitive-product-analysis](skills/competitive-product-analysis/SKILL.md) | 跨品类竞品证据审计、比较框架、机会假设、产品策略和验证计划 | [中文 / English](skills/competitive-product-analysis/README.md) |
| [define-product-requirements](skills/define-product-requirements/SKILL.md) | 把模糊需求转成可追溯、可验证的 Product Brief、范围边界和验证计划 | [中文 / English](skills/define-product-requirements/README.md) |

## 环境与依赖

这些是指导 AI 助手执行任务的工作流，不是独立应用、爬虫或素材库。需要支持 Skill 的 AI 助手，以及具体任务所需的联网搜索、网页访问、文件下载和本地文件处理能力；仅安装本目录不会自动赋予这些工具权限。

- 没有固定的 Python 包、付费 API Key 或指定素材网站依赖。
- 图片联系表、感知去重可按任务使用 Python/Pillow 等工具；视频抽帧、元数据检查可按任务使用 FFmpeg/FFprobe。这些不是阅读或安装 Skill 的前置条件。
- 受限来源可能需要用户自行登录、订阅或取得授权。
- Skill 本身没有操作系统专属后端；实际可执行范围取决于宿主工具和权限。
- `competitive-product-analysis` 附带的 `scripts/audit_package.py` 只使用 Python 标准库；运行该脚本需要 Python 3。

## 安装到 Codex

### 方式一：让 Codex 安装

在支持 `$skill-installer` 的 Codex 中发送：

```text
$skill-installer 请从以下 GitHub 目录安装 collect-design-assets：
https://github.com/972173242qqcom-sudo/shared-ai-skills/tree/main/skills/collect-design-assets
```

安装竞品分析 Skill：

```text
$skill-installer 请从以下 GitHub 目录安装 competitive-product-analysis：
https://github.com/972173242qqcom-sudo/shared-ai-skills/tree/main/skills/competitive-product-analysis
```

安装需求澄清与产品定义 Skill：

```text
$skill-installer 请从以下 GitHub 目录安装 define-product-requirements：
https://github.com/972173242qqcom-sudo/shared-ai-skills/tree/main/skills/define-product-requirements
```

安装后重启 Codex 或开启新会话，确认可以调用所选 Skill。如果当前客户端没有安装器，请使用手动方式。

### 方式二：手动安装

下载本仓库 ZIP 或克隆仓库，将需要的完整 Skill 文件夹放到 Codex 的用户 Skill 目录。以下沿用 `~/.codex/skills/`；若设置了 `CODEX_HOME`，请使用对应目录。

macOS / Linux（需要 Git；以下命令在仓库尚未克隆时执行）：

```bash
git clone https://github.com/972173242qqcom-sudo/shared-ai-skills.git
cd shared-ai-skills
skill_root="${CODEX_HOME:-$HOME/.codex}/skills"
mkdir -p "$skill_root"
# 改成要安装的目录名，例如 collect-design-assets
skill_name="competitive-product-analysis"
if [ -e "$skill_root/$skill_name" ] || [ -L "$skill_root/$skill_name" ]; then
  echo "已存在同名 Skill，请先检查现有内容，再手动更新。"
else
  cp -R "skills/$skill_name" "$skill_root/$skill_name"
fi
```

Windows：下载 ZIP 并解压，将选中的 `skills/<skill-name>` 整个文件夹复制到 `%USERPROFILE%\.codex\skills\`；如配置了 `CODEX_HOME`，改用其下的 `skills` 文件夹。遇到同名目录请先检查，避免覆盖自己的修改。

安装完成的目录应包含：

```text
~/.codex/skills/<skill-name>/
├── SKILL.md
├── README.md
├── agents/        # 若该 Skill 提供
├── references/    # 若该 Skill 提供
├── assets/        # 若该 Skill 提供
└── scripts/       # 若该 Skill 提供
```

其他支持 Skill 的 AI 工具：将完整文件夹安装到该工具规定的 Skill 目录；工具支持和权限需按对应客户端配置。

## 使用示例

```text
$collect-design-assets 收集 12 个智能家居设备配网与状态反馈案例。
优先官方产品页、官方视频和公开案例平台，排除纯广告氛围图。
整理到当前工作区的 design-references 文件夹。
输出精选素材、来源清单、授权备注、去重记录和总览图。
素材仅用于内部设计参考。
```

建议说明素材类型、设计用途、数量、来源偏好、分辨率/格式、授权要求和输出目录。通常交付素材目录、来源索引、预览总览，以及重复、失败和待复核项记录。完整示例见 [Skill 使用说明](skills/collect-design-assets/README.md)。

竞品分析示例：

```text
$competitive-product-analysis 分析这批智能家电竞品资料。
先审计证据与图片覆盖率，再输出比较矩阵、机会地图、推荐方向和验证计划。
```

建议说明要支持的决策、目标用户与地区、分析对象类型、已有证据和输出格式。完整示例见 [竞品分析 Skill 使用说明](skills/competitive-product-analysis/README.md)。

需求澄清与产品定义示例：

```text
$define-product-requirements 进入 clarify 模式。
原始需求：做一个与 AI Agent 有关的桌面硬件。
请建立 E/H/D/U 信息表，指出会改变项目方向的信息缺口，
不要生成造型，不要编造用户研究、市场数据或工程结论。
```

它支持 `clarify`、`build` 和 `audit` 三种模式，可输出 Product Brief、Must / Should / Won't、成功标准、准备度评分和最小验证计划。完整示例见 [需求澄清与产品定义 Skill 使用说明](skills/define-product-requirements/README.md)。

安装验证：在新会话中要求 Codex 读取已安装 Skill，概述其用途和交付内容，暂不执行外部操作。如果未识别，请检查目录层级和 `SKILL.md` 文件名。

## 更新与卸载

- 更新：在克隆目录运行 `git pull --ff-only`，检查变化后，将最新 Skill 文件夹复制到安装目录；ZIP 安装用户重新下载。复制安装不会自动更新。
- 卸载：移除安装目录中对应的 `<skill-name>` 文件夹；如有自定义修改，先备份。

## 授权与使用边界

公开分享这些工作流不代表第三方素材、数据或来源内容可以自由复用。每项素材和证据仍须按原作者或来源网站的许可使用；授权不明时标为待复核或仅作参考。工作流不绕过登录、付费或访问权限限制。
