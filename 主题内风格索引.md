# 主题内选风格

分类字段均可组合，不把论文会场作为绘图风格。下面的图 ID 可用 `library.py search` 检索。

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

## 02_Transformer与注意力

注意力图先写明 Q、K、V 的来源与操作；token/矩阵展开适合局部算子，模块总览适合 Transformer/Mamba 整体架构。

| 布局 | 图例数 | 代表 ID |
|---|---:|---|
| L00 布局待复核 | 424 | TCF_acl2026-2026.acl-long.1458, TCF_acl2026-2026.acl-long.2062, TCF_acl2026-2026.findings-acl.1325 |
| L01 线性流水线 | 29 | T07, TCF_icml2026-0066, TCF_icml2026-0152 |
| L02 多分支与汇合 | 6 | T08, P155_F3_p04, P012_F1_p04 |
| L04 模块总览与局部放大 | 49 | TCF_acl2026-2026.findings-acl.252, TCF_iclr2026-0163, TCF_iclr2026-0199 |
| L06 token矩阵与算子展开 | 5 | T06, T46, P121_F2_p03 |
| L07 迭代与反馈回路 | 2 | T45, P017_F3_p04 |
| L08 分阶段泳道 | 1 | T05 |
| L09 多面板机制对照 | 7 | P121_F3_p05, TCF_acl2025-2025.findings-acl.416, P037_F3_p07 |
| L10 概念示意与场景隐喻 | 44 | TCF_icml2026-0080, TCF_icml2026-0103, TCF_acl2025-2025.acl-long.1522 |

视觉表达：V00 视觉待复核（536）, V01 扁平柔和色块（16）, V02 单色细线（2）, V03 张量层叠与轻透视（7）, V04 图标场景与框图混合（6）。

## 03_图神经网络与关系推理

GNN 先区分图中实体边与系统流程箭头；局部消息传递用节点关系图，完整网络用总览加邻域放大。

| 布局 | 图例数 | 代表 ID |
|---|---:|---|
| L00 布局待复核 | 108 | TCF_aaai2026-37104, TCF_acl2026-2026.acl-long.414, TCF_acl2026-2026.acl-long.942 |
| L01 线性流水线 | 25 | TCF_acl2026-2026.acl-long.172, TCF_cvpr2026-Lv_Robo-SGG_Exploiting_Layout-Oriented_Normalization_and_Restitution_Can_Improve_Robust_Scene_CVPR_2026_paper, P145_F5_p05 |
| L02 多分支与汇合 | 3 | P038_F2_p05, P060_F1_p03, P112_F2_p04 |
| L04 模块总览与局部放大 | 23 | TCF_iclr2026-0130, TCF_iclr2026-0700, TCF_icml2026-0356 |
| L05 节点关系与消息传递 | 12 | T09, T10, T11 |
| L06 token矩阵与算子展开 | 5 | P002_F1_p03, P002_F2_p04, P002_F3_p04 |
| L08 分阶段泳道 | 1 | TCF_icml2026-0336 |
| L09 多面板机制对照 | 4 | P156_F1_p01, P013_F1_p02, P015_F2_p02 |
| L10 概念示意与场景隐喻 | 24 | TCF_icml2026-0031, TCF_icml2026-0091, TCF_icml2026-0146 |
| L11 树状层级与路由 | 1 | T12 |

视觉表达：V00 视觉待复核（167）, V01 扁平柔和色块（8）, V02 单色细线（6）, V03 张量层叠与轻透视（5）, V04 图标场景与框图混合（8）, V05 彩色节点关系图（12）。

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

## 05_检索增强与知识系统

检索类优先区分离线构建与在线查询；GraphRAG 可组合泳道 L08 与节点图 V05。参考模板中的向量索引不能自动搬到图谱方法。

| 布局 | 图例数 | 代表 ID |
|---|---:|---|
| L00 布局待复核 | 11 | TCF_acl2026-2026.acl-long.2144, TCF_cvpr2026-Li_RMIR_A_Benchmark_Dataset_for_Reasoning-Intensive_Multimodal_Image_Retrieval_CVPR_2026_paper, TCF_iclr2026-0164 |
| L01 线性流水线 | 66 | TCF_aaai2026-37741, TCF_cvpr2026-Guo_OpenDPR_Open-Vocabulary_Change_Detection_via_Vision-Centric_Diffusion-Guided_Prototype_Retrieval_for_CVPR_2026_paper, TCF_cvpr2026-Li_Adapting_In-context_Generation_for_Enhanced_Composed_Image_Retrieval_CVPR_2026_paper |
| L02 多分支与汇合 | 1 | P050_F1_p02 |
| L04 模块总览与局部放大 | 13 | TCF_cvpr2026-Chen_Seeing_as_Experts_Do_A_Knowledge-Augmented_Agent_for_Open-Set_Fine-Grained_CVPR_2026_paper, TCF_icml2026-0140, TCF_aaai2025-33036 |
| L05 节点关系与消息传递 | 1 | T18 |
| L07 迭代与反馈回路 | 1 | P124_F3_p04 |
| L08 分阶段泳道 | 2 | T17, TCF_acl2026-2026.acl-long.818 |
| L09 多面板机制对照 | 2 | P176_F3_p05, TCF_neurips2024-1022 |
| L10 概念示意与场景隐喻 | 3 | TCF_icml2026-0343, TCF_iclr2025-2224, TCF_iclr2025-46 |
| L11 树状层级与路由 | 2 | T19, P124_F1_p01 |

视觉表达：V00 视觉待复核（91）, V01 扁平柔和色块（3）, V02 单色细线（1）, V03 张量层叠与轻透视（2）, V04 图标场景与框图混合（2）, V05 彩色节点关系图（2）, V06 高对比模块强调（1）。

## 06_多模态与跨模态融合

多模态要明确各模态输入、单独编码与融合位置；交互注意力的方向由用户方法定义，不能因为对称布局就画成双向。

| 布局 | 图例数 | 代表 ID |
|---|---:|---|
| L00 布局待复核 | 263 | TCF_aaai2026-37184, TCF_aaai2026-37202, TCF_aaai2026-37233 |
| L01 线性流水线 | 22 | TCF_aaai2026-37714, TCF_icml2026-0221, TCF_icml2026-1506 |
| L02 多分支与汇合 | 9 | T20, T21, T22 |
| L04 模块总览与局部放大 | 23 | TCF_aaai2026-37465, TCF_aaai2026-37496, TCF_acl2026-2026.findings-acl.391 |
| L06 token矩阵与算子展开 | 3 | T48, P137_F2_p03, P183_F3_p06 |
| L07 迭代与反馈回路 | 3 | TCF_aaai2026-37613, P063_F3_p04, P075_F2_p02 |
| L08 分阶段泳道 | 1 | P033_F2_p05 |
| L09 多面板机制对照 | 6 | P127_F3_p04, P139_F2_p04, P153_F4_p04 |
| L10 概念示意与场景隐喻 | 47 | TCF_cvpr2026-Clark_Molmo2_Open_Weights_and_Data_for_Vision-Language_Models_with_Video_CVPR_2026_paper, TCF_cvpr2026-Kondic_ChartNet_A_Million-Scale_High-Quality_Multimodal_Dataset_for_Robust_Chart_Understanding_CVPR_2026_paper, TCF_iclr2026-0215 |

视觉表达：V00 视觉待复核（345）, V01 扁平柔和色块（15）, V03 张量层叠与轻透视（4）, V04 图标场景与框图混合（11）, V05 彩色节点关系图（2）。

## 07_强化学习与智能体

强化学习分别表达环境交互与参数学习；智能体工具循环只能画确实存在的反馈。具身场景使用图标辅助说明，不能取代模块定义。

| 布局 | 图例数 | 代表 ID |
|---|---:|---|
| L00 布局待复核 | 101 | TCF_aaai2026-37158, TCF_aaai2026-37248, TCF_acl2026-2026.findings-acl.1811 |
| L01 线性流水线 | 18 | TCF_cvpr2026-Ma_Unifying_Perception_and_Action_A_Hybrid-Modality_Pipeline_with_Implicit_Visual_CVPR_2026_paper, TCF_iclr2026-0104, TCF_iclr2026-0814 |
| L02 多分支与汇合 | 4 | T24, T26, P138_F2_p04 |
| L04 模块总览与局部放大 | 92 | TCF_aaai2026-37152, TCF_aaai2026-37781, TCF_acl2026-2026.acl-long.1272 |
| L07 迭代与反馈回路 | 4 | T23, T25, P178_F2_p04 |
| L08 分阶段泳道 | 3 | TCF_acl2026-2026.findings-acl.412, P149_F1_p01, TCF_neurips2023-0565 |
| L09 多面板机制对照 | 4 | P149_F2_p03, P178_F1_p01, P006_F2_p03 |
| L10 概念示意与场景隐喻 | 20 | TCF_acl2026-2026.acl-long.1773, TCF_icml2026-0216, TCF_icml2026-0398 |

视觉表达：V00 视觉待复核（227）, V01 扁平柔和色块（8）, V02 单色细线（1）, V03 张量层叠与轻透视（1）, V04 图标场景与框图混合（9）。

## 08_训练策略与自监督

训练机制明确冻结与可训练分支、梯度路径、损失与数据流；教师学生、自监督通常适合平行分支或训练推理泳道。

| 布局 | 图例数 | 代表 ID |
|---|---:|---|
| L00 布局待复核 | 63 | TCF_cvpr2026-Feng_Spatial-Aware_VLA_Pretraining_through_Visual-Physical_Alignment_from_Human_Videos_CVPR_2026_paper, TCF_iclr2026-0148, TCF_icml2026-0081 |
| L01 线性流水线 | 40 | TCF_iclr2026-0039, TCF_icml2026-0227, TCF_icml2026-0282 |
| L02 多分支与汇合 | 7 | T27, T28, T29 |
| L04 模块总览与局部放大 | 6 | TCF_cvpr2025-Zhou_Ferret_An_Efficient_Online_Continual_Learning_Framework_under_Varying_Memory_CVPR_2025_paper, P008_F3_p04, TCF_neurips2024-3255 |
| L06 token矩阵与算子展开 | 2 | P077_F1_p01, P023_F3_p05 |
| L08 分阶段泳道 | 1 | T30 |
| L09 多面板机制对照 | 9 | TCF_icml2026-0082, P128_F5_p05, P007_F3_p04 |
| L10 概念示意与场景隐喻 | 73 | TCF_iclr2026-0092, TCF_iclr2026-0119, TCF_iclr2026-0166 |

视觉表达：V00 视觉待复核（178）, V01 扁平柔和色块（11）, V03 张量层叠与轻透视（6）, V04 图标场景与框图混合（4）, V05 彩色节点关系图（2）。

## 09_三维视觉与神经渲染

三维方法可用张量层叠 V03 表达特征、轻场景 V04 表达射线和几何；图示的视角/坐标关系不能随风格改动。

| 布局 | 图例数 | 代表 ID |
|---|---:|---|
| L00 布局待复核 | 102 | TCF_aaai2026-37899, TCF_aaai2026-37929, TCF_cvpr2026-Cai_Exploring_Spatiotemporal_Feature_Propagation_for_Video-Level_Compressive_Spectral_Reconstruction_Dataset_CVPR_2026_paper |
| L01 线性流水线 | 24 | T31, TCF_cvpr2026-An_Learning_Compact_3D_Representations_from_Feed-Forward_Novel_View_Synthesis_CVPR_2026_paper, TCF_cvpr2026-Feng_SR3R_Rethinking_Super-Resolution_3D_Reconstruction_With_Feed-Forward_Gaussian_Splatting_CVPR_2026_paper |
| L02 多分支与汇合 | 4 | T33, TCF_icml2026-0470, P066_F7_p13 |
| L03 层级编码解码 | 1 | P066_F6_p12 |
| L04 模块总览与局部放大 | 8 | TCF_iclr2026-1581, P151_F2_p03, P152_F2_p03 |
| L05 节点关系与消息传递 | 1 | P119_F5_p06 |
| L07 迭代与反馈回路 | 2 | T32, P044_F2_p05 |
| L09 多面板机制对照 | 7 | P152_F1_p02, P044_F3_p07, P054_F2_p03 |
| L10 概念示意与场景隐喻 | 21 | TCF_aaai2026-37416, TCF_aaai2026-38008, TCF_aaai2025-32620 |
| L11 树状层级与路由 | 1 | P054_F4_p05 |

视觉表达：V00 视觉待复核（148）, V01 扁平柔和色块（7）, V02 单色细线（2）, V03 张量层叠与轻透视（11）, V04 图标场景与框图混合（2）, V05 彩色节点关系图（1）。

## 10_计算机系统与数据流程

系统图先确定职责边界、存储组件、读写方向与执行阶段；泳道和层级模块适合数据库、分布式训练和查询执行。

| 布局 | 图例数 | 代表 ID |
|---|---:|---|
| L00 布局待复核 | 37 | TCF_iclr2026-0196, TCF_icml2026-0269, TCF_icml2026-0303 |
| L01 线性流水线 | 6 | T35, P147_F1_p03, TCF_iclr2025-3259 |
| L02 多分支与汇合 | 1 | T34 |
| L04 模块总览与局部放大 | 10 | T36, TCF_neurips2025-3124, P055_F1_p05 |
| L06 token矩阵与算子展开 | 2 | TCF_acl2025-2025.findings-acl.952, P111_F7_p07 |
| L08 分阶段泳道 | 1 | P129_F2_p03 |
| L09 多面板机制对照 | 5 | TCF_iclr2025-0141, P045_F2_p04, P078_F4_p04 |
| L10 概念示意与场景隐喻 | 8 | TCF_icml2026-0270, P078_F1_p01, TCF_cvpr2024-Huang_FedMef_Towards_Memory-efficient_Federated_Dynamic_Pruning_CVPR_2024_paper |
| L11 树状层级与路由 | 1 | P115_F2_p04 |

视觉表达：V00 视觉待复核（48）, V01 扁平柔和色块（15）, V02 单色细线（2）, V04 图标场景与框图混合（5）, V05 彩色节点关系图（1）。

## 11_因果与AI科学机制

因果与科学 AI 区分因果DAG、模型计算图与概念示意；只有用户提供的因果边才标因果，生物/物理机制图必须核对实体语义。

| 布局 | 图例数 | 代表 ID |
|---|---:|---|
| L00 布局待复核 | 55 | TCF_iclr2026-0007, TCF_iclr2026-0052, TCF_iclr2026-0106 |
| L01 线性流水线 | 19 | TCF_icml2026-0114, TCF_icml2026-0331, TCF_aaai2025-31986 |
| L02 多分支与汇合 | 3 | T39, P142_F3_p04, P068_F2_p06 |
| L03 层级编码解码 | 2 | P130_F4_p06, P010_F2_p04 |
| L04 模块总览与局部放大 | 7 | TCF_aaai2026-37058, TCF_icml2026-0148, P130_F3_p05 |
| L05 节点关系与消息传递 | 4 | T37, P142_F2_p03, P010_F1_p03 |
| L06 token矩阵与算子展开 | 1 | P026_F4_p05 |
| L07 迭代与反馈回路 | 5 | T38, P181_F1_p02, P104_F2_p03b |
| L09 多面板机制对照 | 6 | P142_F5_p08, P056_F1_p04, P089_F3_p08 |
| L10 概念示意与场景隐喻 | 28 | TCF_aaai2026-36997, TCF_iclr2026-0049, TCF_icml2026-0202 |

视觉表达：V00 视觉待复核（104）, V01 扁平柔和色块（9）, V02 单色细线（2）, V03 张量层叠与轻透视（4）, V04 图标场景与框图混合（3）, V05 彩色节点关系图（7）, V06 高对比模块强调（1）。

## 12_通用方法与总体框架

通用框架根据数据流选择线性、模块放大或多面板；不要仅用统一方框装饰替代真正的方法结构。

| 布局 | 图例数 | 代表 ID |
|---|---:|---|
| L00 布局待复核 | 717 | TCF_acl2026-2026.acl-long.1489, TCF_acl2026-2026.acl-long.2146, TCF_acl2026-2026.acl-long.801 |
| L01 线性流水线 | 76 | TCF_cvpr2026-Hoe_OneHOI_Unifying_Human-Object_Interaction_Generation_and_Editing_CVPR_2026_paper, TCF_cvpr2026-Huang_Interactive_Tracking_A_Human-in-the-Loop_Paradigm_with_Memory-Augmented_Adaptation_CVPR_2026_paper, TCF_iclr2026-0053 |
| L02 多分支与汇合 | 3 | T40, P090_F2_p13, P117_F1_p12 |
| L03 层级编码解码 | 1 | P090_F3_p14 |
| L04 模块总览与局部放大 | 72 | T42, TCF_iclr2026-0082, TCF_iclr2026-0108 |
| L07 迭代与反馈回路 | 2 | T41, P074_F1_p03 |
| L08 分阶段泳道 | 1 | TCF_acl2026-2026.findings-acl.627 |
| L09 多面板机制对照 | 2 | P109_F1_p02, TCF_neurips2024-1858 |
| L10 概念示意与场景隐喻 | 114 | TCF_cvpr2026-Che_COG_Confidence-aware_Optimal_Geometric_Correspondence_for_Unsupervised_Single-reference_Novel_Object_CVPR_2026_paper, TCF_iclr2026-0064, TCF_iclr2026-0125 |

视觉表达：V00 视觉待复核（974）, V01 扁平柔和色块（3）, V02 单色细线（6）, V03 张量层叠与轻透视（1）, V04 图标场景与框图混合（4）。

