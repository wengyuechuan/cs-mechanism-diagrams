## 01_视觉网络与编码解码

视觉网络先确定尺度与跳连关系；层级编码解码适合 U-Net/FPN，总图与核心模块分开展示适合复杂分割方法。

| 布局 | 图例数 | 代表 ID |
|---|---:|---|
| L00 布局待复核 | 241 | TCF_aaai2026-36960, TCF_aaai2026-36998, TCF_aaai2026-37094 |
| L01 线性流水线 | 29 | T01, T43, T44 |
| L02 多分支与汇合 | 6 | T02, TCF_cvpr2026-Chen_F2Net_A_Frequency-Fused_Network_for_Ultra-High_Resolution_Remote_Sensing_Segmentation_CVPR_2026_paper, P167_F3_p05 |
| L03 层级编码解码 | 2 | T03, T04 |
| L04 模块总览与局部放大 | 14 | TCF_acl2026-2026.findings-acl.1245, TCF_acl2026-2026.findings-acl.538, TCF_cvpr2026-Liu_AeroAgent_A_Vision-Physics-Decision_Framework_for_Aerodynamic_Vehicle_Design_CVPR_2026_paper |
| L06 token矩阵与算子展开 | 2 | TCF_iclr2026-0347, P167_F6_p14 |
| L08 分阶段泳道 | 1 | P120_F12_p11 |
| L09 多面板机制对照 | 7 | P143_F2_p03, TCF_icml2025-1268, TCF_icml2024-0853 |
| L10 概念示意与场景隐喻 | 48 | TCF_acl2026-2026.acl-long.1716, TCF_acl2026-2026.acl-long.490, TCF_acl2026-2026.findings-acl.1365 |

视觉表达：V00 视觉待复核（327）, V01 扁平柔和色块（7）, V02 单色细线（1）, V03 张量层叠与轻透视（6）, V04 图标场景与框图混合（7）, V05 彩色节点关系图（2）。

[打开风格图库](../../风格图库.html)
