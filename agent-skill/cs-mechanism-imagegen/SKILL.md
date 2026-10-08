---
name: cs-mechanism-imagegen
description: Use when an agent needs to draw or restyle computer-science paper mechanism diagrams, neural-network architectures, graph diagrams, or method flowcharts with AI image generation and local visual references. Supports topic, layout, and visual-style retrieval plus topology-aware imagegen prompts. Not for statistical plots.
---

# 计算机论文机制图 AI 绘制

从随 skill 打包的真实 PNG/JPEG 图例中选择表达方式，再按用户的方法结构绘制。主题、布局、视觉表达是三个独立字段；“CVPR 风格”等会议名不是风格标签。原论文图作为布局/视觉参考，不能替代用户的算法定义。

## 选图与理解方法

以下命令中的 `scripts/` 相对于此 skill 目录。先用 `python scripts/library.py list` 查看主题与风格，再检索。例如：

```powershell
python scripts/library.py search --topic retrieval --layout L08 --visual V01 --limit 4
python scripts/library.py search --topic graph --layout L05 --limit 4
```

结果包含图 ID、绝对图片路径、布局/视觉标签、来源与用途。筛选是严格的；零结果时主动放宽一个条件，说明取舍，不冒称找到匹配参考。图库包含本库论文参考、原创蓝图和 Top-Conf 导入参考，`kind` 区分三者。检索结果 `matches` 为返回条数，`total_matches` 为全部匹配数。

```powershell
python scripts/library.py search --source topconf --query HippoRAG --reviewed-only
python scripts/library.py search --source topconf --pattern pipeline --venue ACL --year 2026 --limit 4
python scripts/library.py search --source local --topic retrieval --limit 4
```

导入批次有 3,439 张 JPEG，其中 20 张经过本库看图复核，其余保留上游筛选并标为候选。`upstream_pattern` 保留上游原始标签，不能当成本库风格。批量主题由标题推断，候选布局由 pattern 映射；`L00` / `V00` 是待复核标记，**不是生成预设**。优先 `--reviewed-only`；若采用候选图，必须先看图并明确选择 L01–L11、V01–V06。脚本拒绝直接用 L00/V00 生成。作者、论文链接、上游 ID 和 commit 均须保留。图型 teaser 不能自动理解为架构图。详见 [references/topconf-import.md](references/topconf-import.md)。

用 `view_image` 看候选图片，通常选 1–3 张。不要只读文件名、SVG 源码或图注就声称看过图片。优先选标签少、布局清楚、与目标结构相符的图；同主题的相关论文不一定是所选模板的算法来源。需要主题特有的选择建议时读 [references/topics.md](references/topics.md)，需要区分风格时读 [references/style-taxonomy.md](references/style-taxonomy.md)。

把方法整理为节点、边、分组、循环和准确文字。用户已有具体定义时直接使用；未指定的视觉选择可合理决定。只有影响方法真实性的缺失信息才需要澄清。输出可审阅的 `brief.json`，结构见 [references/brief-schema.md](references/brief-schema.md)；可从 [assets/briefs/graph-rag.json](assets/briefs/graph-rag.json) 改写。

## 提示词与 imagegen

```powershell
python scripts/library.py prompt --brief brief.json --refs T17,T18 --layout L08 --visual V01 --out output/diagram
```

脚本校验端点、重复节点/边、分组及明确禁止的连接，生成 `.prompt.txt`、`.references.json` 和规范化 `.brief.json`。它不调用模型，不需要密钥。参考只决定表达方式；完整边清单决定机制。分组框和图标内部的小图边必须与系统箭头区分。

用户要求 AI 绘图时，读取环境中的 **imagegen** skill，使用内置 `image_gen`。按当前工具声明填写参数，读 [references/imagegen-workflow.md](references/imagegen-workflow.md) 中的调用方式：

- 有本地参考路径时，先 `view_image` 查看，再用 `referenced_image_paths` 引用所选 PNG/JPEG；提示词写清每张是布局参考或视觉参考，而非要求复刻其方法。
- 新图没有参考时不传引用参数。修改已生成图时明确 edit target，并保持节点、边、文字等不变项；本地目标先查看。
- 内置模式不索要 API key，不自动切换 CLI，不伪造不存在的 `model`、`size`、`quality` 或输出路径参数。风格提示与画幅要求写在 prompt 中。
- 内置生成图完成后，复制实际输出到用户项目目录。输出是位图；不能改扩展名冒充可编辑 SVG。用户另需准确矢量结构时，依据同一 brief 用 drawio 工作流制作。

## 验收与交付

查看成图，逐条核对节点、系统箭头起终点、方向、循环、分组和文字；再检查缩小后可读性。若发现额外箭头、错字或遗漏，针对该问题编辑，重复写明保留的不变项。建议最多两次定向修复；仍不满足时报告具体缺陷并保留稿件，不标记为投稿终稿。详细核对表见 [references/quality-check.md](references/quality-check.md)。

保存成图、brief、实际最终 prompt、所选参考 ID/来源和检查记录。说明采用的主题、布局与视觉表达，交付绝对路径并展示成图。新增参考图需按 [references/catalog-maintenance.md](references/catalog-maintenance.md) 保留来源和人工风格复核记录。

完整的真实生成实例见 [references/worked-example.md](references/worked-example.md)：GraphRAG、两张布局参考、9 个节点、8 条单向箭头及实际 imagegen 成图。

## 图库文件

- [gallery.html](gallery.html)：可双击离线浏览，主题内按布局和视觉风格筛选。
- [references/catalog.json](references/catalog.json)：机器可检索索引，所有图片路径相对 skill 根目录。
- `assets/images/`：原始精选 PNG；`assets/imported/topconf/`：导入 JPEG。均不依赖原工作区绝对路径。
- [references/style-taxonomy.json](references/style-taxonomy.json)：11 类布局、6 类视觉表达及可组合的 prompt 片段。
- [references/rights.md](references/rights.md)：原论文参考与原创蓝图的来源及使用边界。
