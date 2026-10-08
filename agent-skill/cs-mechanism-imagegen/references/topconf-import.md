# Top-Conf reference collection

来源：https://github.com/qwdwqfwq/topconf-paper-figure-gallery
固定快照：`1f49dc03cfbfe12a1b8846815d25d3ec5a8253da`，拉取日期 2026-10-08。

实际索引 3,449 条，导入 3,439 张 JPEG。排除上游 results 4 张及本库抽查发现的结果/混合结果图 6 张。本次查看 26 张联系表：20 张接受并复核主要布局、视觉，6 张排除；不是逐图检查所有导入内容。其余 3,419 张保留上游筛选，仍可能含错误图型或结果元素；使用前先看图。主题默认按标题关键词推断。保留作者、来源、原始 pattern、ID 和 commit，不能将这些会场名当风格。

## Retrieval

```powershell
python scripts/library.py search --source topconf --query HippoRAG --reviewed-only
python scripts/library.py search --source topconf --pattern pipeline --venue ACL --year 2026
python scripts/library.py search --source topconf --layout L08 --visual V06 --reviewed-only
```

`kind=upstream_reference`、`source_collection=topconf`。上游图型有 architecture/pipeline/framework/conceptual/teaser/taxonomy/comparison。图型 teaser 仅说明 Figure 1 / 开篇展示，不保证机制图；本库复核后的布局字段可与原 pattern 不同。

未复核的 `V00` 和未知布局 `L00` 只是占位标记。候选 L01/L04/L10 等由 pattern 自动映射，也未必准确；任何 pending 记录均须看图。正式生成只能选 L01–L11、V01–V06；可检索候选后自行依据视觉选择，而不能声称候选已被本库人工复核。

PNG 和 JPEG 都可传给内置 imagegen。本包图像相对路径位于 `assets/imported/topconf/`，检索返回实际绝对路径；不需要上游 checkout，也不需要网络。`verify` 校验图片路径、头部尺寸、哈希和分类 ID；导入时另做完整 JPEG 解码。

上游 LICENSE/NOTICE/IMAGES_POLICY 保留在 [topconf-notices/](topconf-notices/)。代码 MIT 不涵盖论文图片；本库不重新授权图像。完整再分发核验尚未完成。

## Real imagegen adaptation test

采用 `TCF_acl2026-2026.acl-long.818` 作为阶段容器和高对比标题参考，使用已有 GraphRAG brief 的 9 个节点、8 条边。第一次生成把 Graph index 读取边错误指向 Evidence pack，人工检查后仅修复这一条边，第二版通过拓扑核对。最终图和 prompt 位于 `assets/examples/topconf-graph-rag-v02.*`。参考只提供视觉表达，新方法不复制 HiKEY 的算法。
