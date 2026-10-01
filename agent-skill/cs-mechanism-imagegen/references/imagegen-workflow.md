# imagegen 实际工作流

此 skill 负责选图和科学结构；环境提供的 imagegen skill 负责生成与编辑。优先内置工具，无需 `OPENAI_API_KEY`。读取当前工具 schema；下面只展示本次环境支持的调用，不承诺其他运行环境参数完全相同。

```javascript
// @exec: {"yield_time_ms": 120000, "max_output_tokens": 1000}
const result = await tools.image_gen__imagegen({
  prompt: finalPrompt,
  referenced_image_paths: selectedAbsolutePngPaths,
  transparent_background: false
});
generatedImage(result);
```

先用 `view_image` 查看每个本地引用。如果是从零生成而没有图片，省略 `referenced_image_paths` 与 `num_last_images_to_include`。不要同时提供两种引用参数。没有本地路径时才按工具要求引用最近对话图片；缺失目标无法引用时请求重新附图。

## 三种任务

1. **新方法 + 风格参考**：新图，提示词注明 Image 1 是布局参考、Image 2 是视觉参考，采用 brief 的模块/箭头/文字，忽略原图里的算法和论文名称。通常两张足够。
2. **修改现有方法图**：目标是 edit target；精确说明改什么、保留什么。箭头结构、模块数量、文字和布局等不变项每次重复。
3. **同一机制做风格变体**：每种风格分别调用内置工具；共享同一 brief，分别保存 prompt、图和检查记录。不能将“批量”自行解释为 API/CLI 授权。

## 内置输出落盘

内置图通常保存到 `$CODEX_HOME/generated_images/…`，具体以实际返回值为准。先生成，再复制选定文件到用户项目；没有文件路径时依据工具实际输出能力保存，不能杜撰路径。用版本名避免覆盖原稿。给用户说明最终路径与实际 prompt，别打印 base64 图像数据。

透明请求使用 `transparent_background: true`，并在保存时保留 alpha。画幅、清晰度、目标版面和文字要求放入 prompt；它们不构成工具的 `size`、`quality` 等参数。位图不能保证文字、连接和数学排版全部准确，必须查看结果验收。

内置失败时说明失败状态与已保存提示词。CLI 是另一条路径，只有用户明确选择才使用原 imagegen skill 的脚本和文档，不能绕过选择自行调用付费 API。

## 定向修复提示

```text
Edit target: Image 1, the generated method diagram.
Change only: <one observed defect>.
Keep: all <N> system nodes, all <M> directed system edges, the supplied labels,
the palette, groups and relative placement unchanged.
Required correction: <exact intended endpoint / spelling / missing label>.
Scientific invariants: <repeat the actual invariants from brief>.
Do not add other nodes, arrows, claims, measurements or captions.
```
