# 方法结构 brief

`library.py prompt` 接收 UTF-8 JSON。模块和连接定义是生成内容的依据，参考图仅提供表达方式。

| 字段 | 含义 |
|---|---|
| `title` | 文件和说明用标题；图内标题由 `show_title` 决定，默认不画 |
| `topic` | 主题编号/别名，例如 `retrieval`、`graph`、`02` |
| `intent` | 生成图的用途与科学含义 |
| `aspect_ratio` | 期望画幅，例如 `2:1`；不是内置工具参数 |
| `background` | `white` 或 `transparent`；透明时工具参数也要设为 true |
| `nodes` | 必填数组，每项 `id`、`label`；可加 `role`、`group`、`icon`、`note` |
| `edges` | 必填数组，每项 `source`、`target`；可加 `label`、`kind`、`line` |
| `groups` | 可选数组，每项唯一 `id`、`label`、`members` |
| `non_edges` | 明确不能出现的 `[source,target]` 数组，例如回答不能回写图谱 |
| `invariants` | 科学约束，如“教师参数冻结”“Q 来自文本，K/V 来自图像” |
| `layout_notes` | 位置、对齐与走线要求；不改变节点关系 |
| `exact_labels` | 额外需原样出现的文字；节点/分组/边标签会自动纳入文字清单 |
| `palette` | 用户明确指定的配色；为空采用所选视觉风格的建议 |
| `avoid` | 与用户意图有关的排除项 |

`kind` 建议用 `data`、`control`、`loss`、`read`、`write`，`line` 为 `solid` 或 `dashed`。这些是 brief 语义，不是 imagegen 参数。内置工具不会自动知道虚线含义，提示词会显式说明。

节点 ID 必须唯一，边端点和分组成员必须存在；同方向同种类边不能重复。`non_edges` 与允许边冲突会报错。脚本不能证明科学正确性；它只排除结构字段上的明显错误。真正存在的双向关系写两条有向边；仅用于图标的小图不算系统流程中的额外箭头。

稠密图不要删掉真实机制来换取美观。可将同一方法拆为总览与局部放大，或多面板保持完整逻辑。最需要准确绘制的结构必须在 brief 中明确，而不能靠模型猜测。
