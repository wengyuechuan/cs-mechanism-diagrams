# 02_Transformer与注意力

## T05 Transformer encoder-decoder overview

上下双通路展示源端编码、目标端自回归与跨注意力。

[可编辑模板](T05_transformer_encoder_decoder.drawio) · [SVG预览](T05_transformer_encoder_decoder.svg)

- 替换模块名称、输入输出和张量维度。
- 保留主要信息流方向，新增分支放在空白区域。
- 虚线仅表示辅助联系；按真实方法修改箭头语义。

## T06 Q-K-V attention mechanism

三路投影和两阶段矩阵计算分开展示；这里的 A 是注意力权重，不是统计热图。

[可编辑模板](T06_qkv_attention.drawio) · [SVG预览](T06_qkv_attention.svg)

- 替换模块名称、输入输出和张量维度。
- 保留主要信息流方向，新增分支放在空白区域。
- 虚线仅表示辅助联系；按真实方法修改箭头语义。

## T07 Vision Transformer token pipeline

图像到 patch、token 序列、Transformer 和任务头，适合 ViT 类方法。

[可编辑模板](T07_vit_patch_tokens.drawio) · [SVG预览](T07_vit_patch_tokens.svg)

- 替换模块名称、输入输出和张量维度。
- 保留主要信息流方向，新增分支放在空白区域。
- 虚线仅表示辅助联系；按真实方法修改箭头语义。

## T08 State-space block with gating

局部卷积、状态更新和乘性门控的机制示意，需按具体 SSM 实现调整。

[可编辑模板](T08_state_space.drawio) · [SVG预览](T08_state_space.svg)

- 替换模块名称、输入输出和张量维度。
- 保留主要信息流方向，新增分支放在空白区域。
- 虚线仅表示辅助联系；按真实方法修改箭头语义。

## T45 Recurrent computation unrolled in time

按时间步展开循环神经网络，同色模块表示参数共享，横向箭头表示状态传递。

[可编辑模板](T45_rnn_unrolled.drawio) · [SVG预览](T45_rnn_unrolled.svg)

- 替换模块名称、输入输出和张量维度。
- 保留主要信息流方向，新增分支放在空白区域。
- 虚线仅表示辅助联系；按真实方法修改箭头语义。

## T46 Patch image and editable token strip

每个 token 为独立图元，C 表示 CLS token；可替换为 mask、时间或模态 token。

[可编辑模板](T46_patch_token_strip.drawio) · [SVG预览](T46_patch_token_strip.svg)

- 替换模块名称、输入输出和张量维度。
- 保留主要信息流方向，新增分支放在空白区域。
- 虚线仅表示辅助联系；按真实方法修改箭头语义。