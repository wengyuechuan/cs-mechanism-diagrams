# 01_视觉网络与编码解码

## T01 CNN backbone and prediction head

卷积网络的主干—特征—任务头结构，适合分类与特征提取总览。

[可编辑模板](T01_cnn_backbone.drawio) · [SVG预览](T01_cnn_backbone.svg)

- 替换模块名称、输入输出和张量维度。
- 保留主要信息流方向，新增分支放在空白区域。
- 虚线仅表示辅助联系；按真实方法修改箭头语义。

## T02 Residual block with identity path

实线主路径与上方残差旁路分开，突出模块新增计算。

[可编辑模板](T02_residual_block.drawio) · [SVG预览](T02_residual_block.svg)

- 替换模块名称、输入输出和张量维度。
- 保留主要信息流方向，新增分支放在空白区域。
- 虚线仅表示辅助联系；按真实方法修改箭头语义。

## T03 U-shaped encoder-decoder

U 形层级结构与跨层跳连；箭头表示 concat / add 的位置应按方法替换。

[可编辑模板](T03_unet_skip.drawio) · [SVG预览](T03_unet_skip.svg)

- 替换模块名称、输入输出和张量维度。
- 保留主要信息流方向，新增分支放在空白区域。
- 虚线仅表示辅助联系；按真实方法修改箭头语义。

## T04 Feature pyramid and lateral fusion

左右层级对齐，适合 FPN、金字塔特征融合和多尺度检测。

[可编辑模板](T04_feature_pyramid.drawio) · [SVG预览](T04_feature_pyramid.svg)

- 替换模块名称、输入输出和张量维度。
- 保留主要信息流方向，新增分支放在空白区域。
- 虚线仅表示辅助联系；按真实方法修改箭头语义。

## T43 Feature tensors and convolution stages

可编辑立体特征图图元展示空间分辨率下降和通道变化，不要求读者只靠方框理解张量。

[可编辑模板](T43_feature_tensor_cubes.drawio) · [SVG预览](T43_feature_tensor_cubes.svg)

- 替换模块名称、输入输出和张量维度。
- 保留主要信息流方向，新增分支放在空白区域。
- 虚线仅表示辅助联系；按真实方法修改箭头语义。

## T44 Neural network as neuron-node layers

每个神经元与连接都可编辑，适合小型全连接网络、神经网络机制解释。

[可编辑模板](T44_neuron_layers.drawio) · [SVG预览](T44_neuron_layers.svg)

- 替换模块名称、输入输出和张量维度。
- 保留主要信息流方向，新增分支放在空白区域。
- 虚线仅表示辅助联系；按真实方法修改箭头语义。