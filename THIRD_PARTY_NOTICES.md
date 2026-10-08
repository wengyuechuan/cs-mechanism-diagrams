# 第三方论文图片与发布范围

## 不属于本项目 MIT 的材料

`paper_reference` 图例来自论文机制区域裁剪。原作者、出版商或原素材权利人保留权利，包括：

- `references/**/figures/P*_F*.png` 与对应的 PDF 裁剪 `.svg`。
- `agent-skill/cs-mechanism-imagegen/assets/images/**/P*_F*.png` 中的相同图片副本。
- `qa/style_review/`、`qa/v2_review/` 和 `qa/风格图库预览.png` 中可能包含的论文图片拼接/缩略图。
- 本地 PDF、整页预览及未纳入 Git 的压缩包中携带的相应材料。

图库 HTML 引用这些图片，ZIP/Skill 副本、预览和旧 Git 提交也应纳入发布检查。改变目录名、文件类型、画幅或添加出处不会自动改变原素材的许可。

## 当前核验状态

本库保留出处、公开版本地址、图号、PDF 页码和裁剪说明，但 **223 张论文参考尚未完成逐图再分发核验**。状态见 [metadata/rights_review.json](metadata/rights_review.json)。`unverified` 表示缺少完整核验，不能理解为确认禁止使用，也不能理解为已获授权；`cleared_for_public_distribution` 当前均为 `false`。

原创通用蓝图标为 `original_blueprint`，其结构、说明、代码与分类体系采用项目 MIT。AI 示例采用两张原创蓝图作表达参考，不是对某张论文图的复刻。

## 如何补齐记录

每张拟公开图片需记录：明确适用的许可名称、许可文本/正式文章页、作者/权利人署名、原图出处、裁剪或修改说明、图内第三方素材的例外情况，以及需要时的授权证据。项目不能以其 MIT 许可重新授权这些图片。

作为可核查的政策线索，[ACL Anthology 官方 FAQ](https://aclanthology.org/faq/) 说明 2016 年及之后的 ACL 材料采用 CC BY 4.0，并明确该政策不覆盖第三方材料。该通用政策不能替代确认具体文章、图中素材和署名要求；当前核验索引不因此自动标记任何图片为完成。其他来源按各文章/出版商的实际条款核对，不从会议名称或“open access”字样推断统一许可。

## 公开发布前

可保留原创代码、原创蓝图和来源索引；对拟携带的论文图片，补齐许可及必要署名，或从发布内容中排除尚未核验的图片。删除图片时同步检查 skill 图片副本、缩略图、拼接预览和压缩包，更新索引，避免公开图库指向缺失文件。

初始本地 Git 提交已经包含论文图片。后续删除文件或加入 `.gitignore` 只影响后续版本，不会自动从提交历史移除。发布只含原创内容的版本时，应从审核过的文件建立独立干净发布历史，或在明确理解影响后整理历史；不要把未审核的旧历史一起推送。完整本地资料可另外保留。

本说明记录项目的实际素材边界和待核验事项，不作出已完成所有论文版权审查的声明。

## 2026-10-08 Top-Conf 扩充

另导入 3,439 张 `upstream_reference` JPEG，来源、作者和固定版本见 [导入报告](metadata/topconf_import_report.json)，逐图权利状态见 [核验索引](metadata/topconf_rights_review.json)。原图放在 `agent-skill/cs-mechanism-imagegen/assets/imported/topconf/`；联系表和浏览器截图也可能包含其缩略图。保留的上游 [LICENSE](third_party/topconf-paper-figure-gallery/LICENSE)、[NOTICE](third_party/topconf-paper-figure-gallery/NOTICE.md) 和 [IMAGES_POLICY](third_party/topconf-paper-figure-gallery/IMAGES_POLICY.md) 明确区分代码许可与论文图片权利。图像不因上游或本库代码 MIT 而变为 MIT。
