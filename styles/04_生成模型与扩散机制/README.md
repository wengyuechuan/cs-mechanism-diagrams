## 04_生成模型与扩散机制

生成模型明确前向/逆向方向、条件注入与采样次数；迭代布局适合扩散过程，分支布局适合条件与潜变量。

| 布局 | 图例数 | 代表 ID |
|---|---:|---|
| L00 布局待复核 | 187 | TCF_aaai2026-37480, TCF_aaai2026-42458, TCF_acl2026-2026.acl-long.336 |
| L01 线性流水线 | 67 | TCF_aaai2026-37940, TCF_cvpr2026-He_Re-Align_Structured_Reasoning-guided_Alignment_for_In-Context_Image_Generation_and_Editing_CVPR_2026_paper, TCF_cvpr2026-Ko_Diffusion-Based_sRGB_Real_Noise_Generation_via_Prompt-Driven_Noise_Representation_Learning_CVPR_2026_paper |
| L02 多分支与汇合 | 4 | T16, P136_F2_p03, P159_F1_p03 |
| L03 层级编码解码 | 1 | P141_F3_p04 |
| L04 模块总览与局部放大 | 14 | T14, TCF_cvpr2026-Cao_RDF-MIG_A_Robust_Diffusion_Framework_for_Masked_Image_Generation_to_CVPR_2026_paper, TCF_iclr2026-0421 |
| L06 token矩阵与算子展开 | 1 | P014_F2_p04 |
| L07 迭代与反馈回路 | 7 | T13, T15, TCF_aaai2026-37070 |
| L09 多面板机制对照 | 8 | P123_F1_p01, P123_F2_p03, P135_F2_p03 |
| L10 概念示意与场景隐喻 | 12 | TCF_icml2026-0002, TCF_icml2026-0354, TCF_aaai2025-33314 |

视觉表达：V00 视觉待复核（274）, V01 扁平柔和色块（12）, V02 单色细线（1）, V03 张量层叠与轻透视（4）, V04 图标场景与框图混合（9）, V05 彩色节点关系图（1）。

[打开风格图库](../../风格图库.html)
