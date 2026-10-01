# 扩充与维护

`catalog.json` 每条记录包括唯一 `id`、`kind`、`topic`、`category`、`title`、`layout_style`、`visual_style`、相对路径 `image`、来源/页码和图片 SHA-256。`paper_reference` 与 `original_blueprint` 分开标注。

追加公开论文机制图时保存论文正式来源 URL、实际版本、图号、PDF 页码、裁剪备注与实际图像。筛除统计图、结果样例、正文误识别；混合原图只保留清晰的机制区域并记录裁剪。读取原图后标注主布局和视觉表达，不只靠论文标题或图注自动推断。

风格是多轴分类，当前为一个主布局 + 一个主视觉标签；复杂混合原图可增加 secondary 标签并解释。不要给看不清的图硬贴详细标签。图库人工分类为缩略图层面的表达方式整理，不等于算法审核。风格 taxonomy 的推荐配色不是原图精确取色。

新增图像放在 `assets/images/<topic>/<layout>/<id>.png`，路径保持相对 skill 根目录。更新 JSON 与离线 gallery，运行 `python scripts/library.py verify` 核对文件、PNG 签名、SHA-256、分类和 ID。该脚本不负责语义复核，后者需要查看图像。

只复制图片或图例元数据到可携带 skill 包，原论文 PDF 可保存在完整工作区资料库。跨机器使用时无需原工作区绝对路径。分享含论文原图的包前检查文章许可；本地个人研究用途不自动赋予再分发许可。
