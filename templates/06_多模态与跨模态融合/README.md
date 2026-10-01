# 06_多模态与跨模态融合

## T20 Dual encoder and cross-modal alignment

两种模态各自编码，右侧显示对齐目标；适合 CLIP 类机制。

[可编辑模板](T20_dual_encoder.drawio) · [SVG预览](T20_dual_encoder.svg)

- 替换模块名称、输入输出和张量维度。
- 保留主要信息流方向，新增分支放在空白区域。
- 虚线仅表示辅助联系；按真实方法修改箭头语义。

## T21 Cross-modal attention fusion

明确 Q 与 K/V 来自不同模态，便于展示交互模块创新。

[可编辑模板](T21_cross_modal_fusion.drawio) · [SVG预览](T21_cross_modal_fusion.svg)

- 替换模块名称、输入输出和张量维度。
- 保留主要信息流方向，新增分支放在空白区域。
- 虚线仅表示辅助联系；按真实方法修改箭头语义。

## T22 Audio-visual temporal fusion

时间对齐作为独立模块，适合音视频识别和事件理解。

[可编辑模板](T22_audio_visual.drawio) · [SVG预览](T22_audio_visual.svg)

- 替换模块名称、输入输出和张量维度。
- 保留主要信息流方向，新增分支放在空白区域。
- 虚线仅表示辅助联系；按真实方法修改箭头语义。

## T48 Token-level cross-modal interactions

上下 token 对应边展示模态对齐和交互机制，可改为稀疏或全连接交互。

[可编辑模板](T48_modality_token_alignment.drawio) · [SVG预览](T48_modality_token_alignment.svg)

- 替换模块名称、输入输出和张量维度。
- 保留主要信息流方向，新增分支放在空白区域。
- 虚线仅表示辅助联系；按真实方法修改箭头语义。