# 04_生成模型与扩散机制

## T13 Forward noising and reverse denoising

上下分层区分前向加噪与学习的反向去噪，避免把两个方向混成一条线。

[可编辑模板](T13_diffusion_forward_reverse.drawio) · [SVG预览](T13_diffusion_forward_reverse.svg)

- 替换模块名称、输入输出和张量维度。
- 保留主要信息流方向，新增分支放在空白区域。
- 虚线仅表示辅助联系；按真实方法修改箭头语义。

## T14 Latent diffusion with conditioning

编码到潜空间、条件注入与图像解码，适合条件生成总图。

[可编辑模板](T14_latent_diffusion.drawio) · [SVG预览](T14_latent_diffusion.svg)

- 替换模块名称、输入输出和张量维度。
- 保留主要信息流方向，新增分支放在空白区域。
- 虚线仅表示辅助联系；按真实方法修改箭头语义。

## T15 Adversarial generator-discriminator loop

真假样本合流及训练反馈放在下方，适合 GAN 与对抗机制。

[可编辑模板](T15_gan_adversarial.drawio) · [SVG预览](T15_gan_adversarial.svg)

- 替换模块名称、输入输出和张量维度。
- 保留主要信息流方向，新增分支放在空白区域。
- 虚线仅表示辅助联系；按真实方法修改箭头语义。

## T16 Variational latent reparameterization

概率变量与采样节点分开，清晰显示可微重参数化结构。

[可编辑模板](T16_vae_latent.drawio) · [SVG预览](T16_vae_latent.svg)

- 替换模块名称、输入输出和张量维度。
- 保留主要信息流方向，新增分支放在空白区域。
- 虚线仅表示辅助联系；按真实方法修改箭头语义。