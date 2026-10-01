# Contributing

欢迎改进机制图、网络架构与方法流程的表达方式。本项目不收录统计结果图模板。

## 报告问题

Issue 请提供图 ID 或文件路径、问题描述、复现步骤、预期结果；涉及方法语义时附正式论文链接、图号和页码。不要提交 API key、个人本机路径或未获许可的素材。

## 新增原创模板

1. 提供通用方法结构，明确节点、边、分组和标签；不要精确复制未授权论文图。
2. 提交 `.drawio`、结构 `.json`、`.svg` 和 `.png`，记录主题、主布局和视觉风格。
3. 保证连线端点有效、图元无明显重叠、缩小后标签可读。
4. 确认你有权以本项目 MIT 许可贡献这些原创材料，保留所需署名。

## 新增论文参考

必须记录正式来源 URL、实际公开版本 URL、论文标题/年份/会场、图号、PDF 页码、裁剪或其他修改、明确的许可名称及许可链接、权利人/作者署名和必要例外。原论文中引用的照片、图标或其他第三方图元需独立核查。

只有完成再分发核验的图片才能加入公开发行。单独存在公开下载链接或出处记录不足以证明再分发许可。待审参考可先贡献书目信息与选图建议，不附图片文件。

同步更新 `metadata/rights_review.json`、图库 catalog 和按主题/风格划分的索引；核对副本及预览中是否仍有未授权内容。不要把 `paper_reference` 标为 `original_blueprint`。

## 验证改动

在仓库根目录运行与改动有关的检查：

```bash
python agent-skill/cs-mechanism-imagegen/scripts/library.py verify
python qa/test_skill_tools.py
python qa/test_readme_preservation.py
```

如本机具备完整 PDF/页面预览，再运行 `python tools/validate_library.py`。新机制图需人工看图，核对节点、箭头、循环、分组和标签；文件解析成功不代表算法正确。

## Pull Request

说明具体问题、最终改动、来源/许可与实际验证结果。不要提交 `tools/vendor/`、缓存、原 PDF、重复 ZIP、本机安装目录或临时输出。使用相对路径，保持手工 README，避免完整重采集覆盖已审核数据。
