# Shared AI Skills

可安装、可复用的 AI 工作流。目前提供一个 Skill：

| Skill | 功能 | 使用说明 |
| --- | --- | --- |
| [collect-design-assets](skills/collect-design-assets/SKILL.md) | 设计素材搜索、筛选、下载、去重、整理和来源记录 | [中文 / English](skills/collect-design-assets/README.md) |

## 环境与依赖

这是指导 AI 助手执行任务的工作流，不是独立运行的爬虫或素材库。需要支持 Skill 的 AI 助手，以及任务所需的联网搜索、网页访问、文件下载和本地文件处理能力；仅安装本目录不会自动赋予这些工具权限。

- 没有固定的 Python 包、付费 API Key 或指定素材网站依赖。
- 图片联系表、感知去重可按任务使用 Python/Pillow 等工具；视频抽帧、元数据检查可按任务使用 FFmpeg/FFprobe。这些不是阅读或安装 Skill 的前置条件。
- 受限来源可能需要用户自行登录、订阅或取得授权。
- Skill 本身没有操作系统专属后端；实际可执行范围取决于宿主工具和权限。

## 安装到 Codex

### 方式一：让 Codex 安装

在支持 `$skill-installer` 的 Codex 中发送：

```text
$skill-installer 请从以下 GitHub 目录安装 collect-design-assets：
https://github.com/972173242qqcom-sudo/shared-ai-skills/tree/main/skills/collect-design-assets
```

安装后重启 Codex 或开启新会话，确认可以调用 `$collect-design-assets`。如果当前客户端没有安装器，请使用手动方式。

### 方式二：手动安装

下载本仓库 ZIP 或克隆仓库，将完整的 `skills/collect-design-assets` 文件夹放到 Codex 的用户 Skill 目录。以下沿用 `~/.codex/skills/`；若设置了 `CODEX_HOME`，请使用对应目录。

macOS / Linux（需要 Git；以下命令在仓库尚未克隆时执行）：

```bash
git clone https://github.com/972173242qqcom-sudo/shared-ai-skills.git
cd shared-ai-skills
skill_root="${CODEX_HOME:-$HOME/.codex}/skills"
mkdir -p "$skill_root"
if [ -e "$skill_root/collect-design-assets" ] || [ -L "$skill_root/collect-design-assets" ]; then
  echo "已存在同名 Skill，请先检查现有内容，再手动更新。"
else
  cp -R skills/collect-design-assets "$skill_root/collect-design-assets"
fi
```

Windows：下载 ZIP 并解压，将 `skills/collect-design-assets` 整个文件夹复制到 `%USERPROFILE%\.codex\skills\`；如配置了 `CODEX_HOME`，改用其下的 `skills` 文件夹。遇到同名目录请先检查，避免覆盖自己的修改。

安装完成的目录应包含：

```text
~/.codex/skills/collect-design-assets/
├── SKILL.md
└── README.md
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

安装验证：在新会话中要求 Codex“读取 collect-design-assets，概述它的用途和交付内容，暂不联网或下载”。如果未识别，请检查目录层级和 `SKILL.md` 文件名。

## 更新与卸载

- 更新：在克隆目录运行 `git pull --ff-only`，检查变化后，将最新 Skill 文件夹复制到安装目录；ZIP 安装用户重新下载。复制安装不会自动更新。
- 卸载：移除安装目录中的 `collect-design-assets` 文件夹；如有自定义修改，先备份。

## 素材授权

公开分享此工作流不代表第三方素材可以自由复用。每项素材仍须按原作者或来源网站的许可使用；授权不明时标为待复核或仅作参考。工作流不绕过登录、付费或访问权限限制。
