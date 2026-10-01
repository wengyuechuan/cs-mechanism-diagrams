# CS Mechanism Diagram Library

**计算机论文机制图、神经网络架构图与流程图模板库，以及面向 AI agent 的绘图 Skill。**

从真实论文图中整理表达方式，把“方法主题”“布局结构”“视觉风格”分开选择，再依据自己的节点、连接和分组绘制方法图。支持离线浏览、draw.io 编辑和 imagegen 工作流。

[快速开始](#快速开始) · [风格分类](#风格分类) · [AI-绘图-skill](#ai-绘图-skill) · [贡献](CONTRIBUTING.md) · [许可与公开发布](#许可与公开发布)

> **许可范围：** 原创代码、说明、分类体系和结构蓝图采用 MIT。论文参考图采用各自的许可，223 张参考图的逐图再分发核验尚未完成；当前完整参考版不能整体视为 MIT 授权。公开发布前请按 [第三方素材说明](THIRD_PARTY_NOTICES.md) 补齐许可或排除未核验图像。

## 项目内容

| 内容 | 数量 | 说明 |
|---|---:|---|
| 真实 PNG 图例 | **271** | 223 张论文机制参考 + 48 张原创结构蓝图，图片哈希各不相同 |
| 原创可编辑模板 | **48 套** | 每套包含 `.drawio`、`.svg`、`.png` 与结构 `.json` |
| 论文来源记录 | **184 篇** | 出处、公开版本地址、年份、PDF 页数与 SHA-256；完整 PDF 未纳入 Git |
| 主题类别 | **12** | 覆盖视觉、Transformer、GNN、生成、检索、多模态、智能体、系统等 |
| 布局风格 | **11** | 描述模块、分支、层级和阅读路径 |
| 视觉表达 | **6** | 描述图元、线条、色彩与透视方式 |

资料整理日期：2026-10-01。覆盖 CVPR、ICCV、ECCV、NeurIPS、ICML、ICLR、ACL、JMLR、TPAMI、IJCV、TOG/SIGGRAPH、PVLDB、Nature 与 Nature Machine Intelligence 的代表性论文。它是参考集合，未穷尽这些会议和期刊。最近一次扩充新增 52 篇 ICCV/ICML/ACL 2025 论文，筛选保留 61 张机制图。

适合模型架构、方法总览、消息传递、训练策略、检索流程与智能体工作流。统计曲线、柱状图、结果热图不属于本库模板范围。

## 预览

下面是按两张原创蓝图选取表达方式、实际调用 imagegen 得到的 GraphRAG 示例：

![GraphRAG：离线图谱构建与在线检索回答](examples/imagegen/graph-rag-v01.png)

示例采用 **L08 分阶段泳道 + V01 扁平柔和色块**，包含 9 个系统节点和 8 条单向箭头。可查看 [方法定义](examples/imagegen/graph-rag-v01.brief.json)、[最终提示词](examples/imagegen/graph-rag-v01.final.prompt.txt) 和 [人工核对记录](examples/imagegen/graph-rag-v01.review.json)。这是一份演示方法，不代表所有 GraphRAG 系统的统一算法。

## 快速开始

### 浏览图库

下载或克隆仓库后，在本地双击：

- **[风格图库.html](风格图库.html)**：按主题、布局、视觉表达、来源类型和关键词组合筛选。
- **[index.html](index.html)**：浏览原创模板、论文机制参考和论文来源清单。
- **[Skill 独立图库](agent-skill/cs-mechanism-imagegen/gallery.html)**：浏览随 skill 携带的 PNG 图例。

页面内嵌索引，不需要服务器、网络或 Python。GitHub 的文件页面展示 HTML 源码；下载到本地后打开才是交互图库。仓库未附带完整 PDF、整页预览和 ZIP，因此这些本地资料入口需要额外下载或构建。

### 编辑原创模板

在 `index.html` 中选择模板，点击“在线编辑”，或把 `templates/` 下的 `.drawio` 文件导入 [diagrams.net](https://app.diagrams.net/)。更改模块、张量尺寸、连接和分组后，从编辑器导出 SVG/PDF。

模板是原创通用结构蓝图，使用前应与自己的方法核对。仓库 SVG 预览由相同 JSON 定义生成，未声称是 draw.io 原生导出的文件。

## AI 绘图 Skill

[cs-mechanism-imagegen](agent-skill/cs-mechanism-imagegen/SKILL.md) 包含真实图片、机器可检索索引、风格提示片段、方法 brief 格式、提示词脚本和检查流程。检索脚本只依赖 Python 标准库；AI 生成需要 agent 环境提供 imagegen 工具。

### 安装

把 `agent-skill/cs-mechanism-imagegen/` **整个目录**复制到个人 skill 目录，保留 `assets/`、`references/` 和 `scripts/`。例如：

**Windows PowerShell**，在仓库根目录执行：

```powershell
$skillDestination = Join-Path $env:USERPROFILE '.codex/skills/cs-mechanism-imagegen'
if (Test-Path -LiteralPath $skillDestination) { throw '目标已存在，请先检查现有版本。' }
New-Item -ItemType Directory -Force -Path (Split-Path $skillDestination) | Out-Null
Copy-Item -LiteralPath 'agent-skill/cs-mechanism-imagegen' -Destination $skillDestination -Recurse
```

**macOS / Linux**：

```bash
mkdir -p ~/.codex/skills
test ! -e ~/.codex/skills/cs-mechanism-imagegen && cp -R agent-skill/cs-mechanism-imagegen ~/.codex/skills/
```

上述复制不覆盖已有安装。其他 agent 环境可按自身的 skill 加载方式使用同一目录。

### 调用

```text
使用 $cs-mechanism-imagegen 和 $imagegen，先选取合适参考，再绘制我的方法图。
主题：图神经网络；布局：节点关系与消息传递；视觉：彩色节点关系图。
我的节点、连接、分组与精确标签如下：……
```

工作流程：**检索 → 查看 PNG → 定义方法 brief → 校验结构 → 组合提示词 → imagegen → 查看并核对成图 → 保存交付记录**。

参考图决定表达方式，用户提供的方法决定结构。脚本会拒绝不存在的端点、重复节点/边、无效分组和明确禁止的连接；图像生成后仍需核对，脚本不能保证生成模型完全遵守提示。

### 命令行选图与提示词

从仓库根目录进入 skill 目录：

```bash
cd agent-skill/cs-mechanism-imagegen
python scripts/library.py list
python scripts/library.py search --topic retrieval --layout L08 --visual V01 --limit 4
python scripts/library.py search --topic graph --layout L05 --limit 4
python scripts/library.py prompt --brief assets/briefs/graph-rag.json --refs T17,T18 --layout L08 --visual V01 --out output/graph-rag
python scripts/library.py verify
```

`prompt` 生成 `.brief.json`、`.prompt.txt` 和 `.references.json`，不会调用模型或要求密钥。筛选是严格的：没有匹配时返回零结果，需要放宽条件。图片路径相对 skill 根目录保存，迁移后仍可检索。

## 风格分类

三种字段独立组合；同一主题不限定一种风格，也不保证每个主题都有全部风格组合。

| 布局 ID | 结构表达 | 常见用途 |
|---|---|---|
| L01 | 线性流水线 | 输入—处理—输出、数据流程 |
| L02 | 多分支与汇合 | 多模态、双编码器、教师学生 |
| L03 | 层级编码解码 | U-Net、FPN、跳连 |
| L04 | 模块总览与局部放大 | 整体框架与核心模块 |
| L05 | 节点关系与消息传递 | GNN、图谱、因果 DAG |
| L06 | token 矩阵与算子展开 | 注意力、mask、patch、张量操作 |
| L07 | 迭代与反馈回路 | 扩散、优化、RL、智能体循环 |
| L08 | 分阶段泳道 | 离线/在线、训练/推理、系统职责 |
| L09 | 多面板机制对照 | 基线与改进、阶段变化 |
| L10 | 概念示意与场景隐喻 | 任务动机、环境与概念 |
| L11 | 树状层级与路由 | 层次池化、树检索、分层路由 |

视觉表达：**V01** 柔和色块、**V02** 单色细线、**V03** 张量层叠与轻透视、**V04** 图标场景与框图混合、**V05** 彩色节点、**V06** 高对比模块强调。

主题涵盖视觉网络、Transformer/注意力、图神经网络、生成/扩散、检索/知识系统、多模态、强化学习/智能体、训练/自监督、三维视觉、计算机系统、因果/AI 科学机制和通用方法。

这些标签是本库人工整理的表达方式，配色是绘制建议，不是会议官方规范。参见 [风格指南](风格分类指南.md) 与 [主题内风格索引](主题内风格索引.md)。

## 仓库结构

```text
agent-skill/cs-mechanism-imagegen/   完整 skill、271 张 PNG 与相对路径索引
templates/                         48 套原创可编辑模板
references/                        论文机制裁剪图与来源元数据
metadata/                          论文、图例、模板、风格和许可待核验索引
styles/                            每个主题内部的布局分组
examples/imagegen/                 真实生成例子与交付记录
tools/                             采集、筛选、构建、打包和校验脚本
qa/                                检查记录与测试
```

原 PDF、整页预览、依赖与 HTTP 缓存、ZIP 和重复解压目录已在 `.gitignore` 中排除。下载目录保留历史位置，当前主题分类以图库和元数据为准。

## 构建与验证

检索和测试无需额外依赖。在仓库根目录执行：

```bash
python agent-skill/cs-mechanism-imagegen/scripts/library.py verify
python qa/test_skill_tools.py
python qa/test_readme_preservation.py
```

重建图库和模板预览需要 `requirements.txt` 中的依赖，建议使用 Python 3.12 与虚拟环境：

```bash
python -m venv .venv
# 选择自己的平台激活虚拟环境后：
python -m pip install -r requirements.txt
python tools/build_style_library.py
python tools/build_gallery.py
python tools/package_style_skill.py
```

当前模板预览渲染脚本使用 Windows 字体目录；在其他平台构建前应设置合适的字体路径。浏览现有 PNG 与运行 skill 检索不依赖该字体目录。手工维护的 README 不会被图库构建覆盖。

`tools/validate_library.py` 检查全量本地资料，运行时还需要被 Git 忽略的 PDF 和整页预览。采集工具会生成待审候选，完整重采集可能更新元数据，不能替代人工筛选。

现有检查记录包含图片路径/哈希、PDF 页数、SVG/XML、模板几何、严格筛选和非法连接测试。论文图做过缩略图类型及风格检查，未做全部算法的专家审核；AI 例子做过节点、箭头和文字核对，未验证特定期刊的投稿版面。

## 贡献与反馈

欢迎通过 Issue 报告来源错误、裁剪问题、标签问题、失效链接或绘图流程缺陷；通过 Pull Request 提交原创模板、明确授权的参考、分类修正和脚本改进。请附图 ID、复现步骤及预期结果。

新增论文图片需提供来源、图号/页码、裁剪说明、明确许可与必要署名，不接受仅凭“可公开下载”判断为可再发布。详细要求见 [CONTRIBUTING.md](CONTRIBUTING.md)。

## 许可与公开发布

- **原创材料：** 代码、说明、分类体系和 `original_blueprint` 模板采用 [MIT License](LICENSE)。
- **论文参考：** `paper_reference` PNG、PDF 裁剪 SVG 及其他论文素材保留原作者/出版商权利，排除在本项目 MIT 范围外。
- **核验记录：** [metadata/rights_review.json](metadata/rights_review.json) 标记当前逐图状态；[THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) 说明覆盖路径与核验方法。

**公开 GitHub 发布前，需补齐相应图片的再分发许可、署名及修改说明，或从发布内容中排除未核验图片。** 已进入提交历史的素材，仅在后续提交删除或加入 `.gitignore` 不会从历史中消失；发布前也应核对所推送的历史内容。当前尚未创建远程仓库或推送。

参考原图时应重新定义自己的算法、标签与素材；出处完整不等于已获得任意使用许可。
