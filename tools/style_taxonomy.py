"""Editorial labels for diagram layout and visual treatment, not venue standards."""
LAYOUTS=[
('L01','线性流水线','linear-pipeline','单条主链横向或纵向推进，输入、变换与输出顺序清楚。','输入到输出的顺序方法、数据处理、推理流程。','把真正并行的模态硬挤成一条链。','Use one aligned main pipeline with consistent module sizes; show each transformation in reading order. Route auxiliary links outside the main chain.','2:1'),
('L02','多分支与汇合','parallel-fusion','多条并行编码/处理支路，明确融合、共享或分叉节点。','多模态、双编码器、教师学生、多个任务头。','支路交叉或共享模块语义不清。','Use parallel aligned lanes for the branches, explicit merge/split nodes and a clearly labelled fusion operation. Keep shared and branch-specific modules distinct.','2:1'),
('L03','层级编码解码','hierarchical-encoder-decoder','按层级、分辨率或网络深度排列，跨层联系与跳连可见。','U-Net、FPN、层级网络、深层展开。','没有层级意义却使用复杂U形。','Arrange the network by depth or resolution; align corresponding encoder/decoder levels. Route skip connections in reserved gutters and distinguish add from concat when supplied.','3:2'),
('L04','模块总览与局部放大','modular-inset','外层方法总览加子模块容器/插图，建立整体到细节的层级。','复杂总体框架与一个核心创新模块。','各插图同等拥挤、放大框与总图没有对应。','Create a clear overview and one or two bounded detail insets. Repeat module identifiers to connect overview and detail; group boundaries must not look like data-flow arrows.','2:1'),
('L05','节点关系与消息传递','node-link-graph','显式节点与边，邻居、关系类型或聚合目标以位置/颜色区分。','GNN、知识图谱、因果DAG、关系推理。','把模块之间所有箭头都叫消息传递。','Draw explicit node-link graphs with visible adjacency and relation labels where required. Distinguish internal illustrative graph edges from directed system-flow arrows; highlight the target node and aggregation only if specified.','3:2'),
('L06','token矩阵与算子展开','token-matrix-operator','用token条、矩阵、张量或离散序列展现操作过程。','注意力、mask、patch、索引编码与张量机制。','将概念矩阵画成带数值结果的统计热图。','Use token strips, tensor tiles and operator nodes to expose the computation. Preserve supplied tensor dimensions and sequence order; schematic colors encode roles, not fabricated measurements.','2:1'),
('L07','迭代与反馈回路','iteration-feedback','重复步骤、训练更新或环境交互以回路/时间箭头表达。','扩散逆过程、优化更新、RL、工具循环。','给只读检索系统添加不存在的回答回写。','Make iteration direction and the repeated unit explicit. Route feedback outside the forward path; draw a loop only when the supplied edge list contains it. Separate interaction, learning and control links.','2:1'),
('L08','分阶段泳道','stage-swimlane','离线/在线、训练/推理、客户端/服务端等按容器分轨。','RAG离线在线、训练测试、系统分层工作流。','把分组边界当连线或将阶段混在同一轨。','Use labelled stage or responsibility swimlanes. Align chains within each lane and route cross-lane links through a clear gutter. Stage containers are grouping devices; cross-stage read/write directions must follow the brief.','2:1'),
('L09','多面板机制对照','multi-panel-comparison','以(a)(b)等面板对照结构或机制变化，保留相同基准位置。','基线与新方法、不同阶段、不同机制设计。','用实验结果曲线替代机制对照。','Use comparable panels with aligned input/output positions and consistent visual vocabulary. Emphasize structural differences with one accent color; panels compare mechanisms, not invented numerical performance.','2:1'),
('L10','概念示意与场景隐喻','conceptual-scene','图标、人物、物体或几何场景解释任务、概念与动作。','任务动机、具身环境、科学机制直观说明。','装饰场景代替算法结构或暗示无根据的生物因果。','Use a restrained explanatory scene or a few consistent icons, connected to the stated mechanism. Keep illustration subordinate to scientific meaning; do not add decorative characters or new claims.','3:2'),
('L11','树状层级与路由','tree-hierarchy','自顶向下层次、树节点、搜索路径或分层服务栈。','层次池化、树检索、任务路由、系统栈。','把一般DAG误画成只能有单父节点的树。','Use a clear hierarchy with aligned levels and labelled parent-child or routing relations. Preserve multiple parents if the supplied structure is a DAG; do not force it into a tree.','3:2'),
]
VISUALS=[
('V01','扁平柔和色块','flat-muted','白底、低饱和模块填充、细描边、少量圆角。','#E4EDF6 / #E4F0E8 / #EEE7F4 / #FFF1D7','Flat academic vector-like appearance on white; muted blue, green, lavender and amber functional groups; thin consistent dark-slate outlines; no shadows or gradients.'),
('V02','单色细线','monochrome-line','黑白/灰色线稿，通过边框与线型区分语义。','#FFFFFF / #E5E7EB / #475569 / #111827','Monochrome line art with white and light-gray fills, crisp black/gray outlines and high legibility. Encode distinctions by labels and shapes rather than color alone.'),
('V03','张量层叠与轻透视','tensor-isometric','特征图、张量或网络层以堆叠片、薄立方体和轻透视表达。','#CBDDED / #D3E6D3 / #ECDDC2 / #D9D1E8','Represent supplied feature maps or tensors as thin stacked slabs with restrained consistent isometric perspective. Keep labels flat and legible; avoid glossy rendering, lighting effects or gratuitous depth.'),
('V04','图标场景与框图混合','icon-scene-hybrid','输入样例/场景/图标与模块框图并置，明确图示角色。','#E4EDF6 / #F3E6C9 / #DCE8DE / #243247','Combine clean flat process blocks with a small number of restrained explanatory icons or input-scene thumbnails. Keep a consistent illustration language and ample whitespace; scene content is schematic unless a real input is provided.'),
('V05','彩色节点关系图','colored-node-link','彩色节点和细边，以颜色表示节点角色或关系种类。','#8CCFC5 / #E7BA7A / #A8A1D5 / #8CAED0','Use muted colored circular nodes and fine neutral graph edges; reserve one stronger accent for the target or active neighborhood. Provide labels or a compact legend for semantic node roles, without fabricating graph measurements.'),
('V06','高对比模块强调','high-contrast-modules','较强色彩区分路径或新增模块；保持有限颜色。','#4878B8 / #D9655B / #75A66D / #2F3542','Use a limited high-contrast palette for major branches, with a single accent highlighting the stated contribution. Keep the background white and text dark; avoid neon, glow and visual clutter.'),
]

def taxonomy():
    return {'version':2,'classification_note':'本库人工整理的表达方式标签，不是任何会议期刊的官方绘图规范；配色为绘制建议，未从每张原图精确取色。',
            'layouts':[dict(zip(['id','name','slug','definition','use_when','avoid_when','prompt_clause','suggested_aspect_ratio'],x)) for x in LAYOUTS],
            'visuals':[dict(zip(['id','name','slug','definition','suggested_palette','prompt_clause'],x)) for x in VISUALS]}

TEMPLATE_STYLES={
    'T01':('L01','V01'),'T02':('L02','V01'),'T03':('L03','V01'),'T04':('L03','V01'),
    'T05':('L08','V01'),'T06':('L06','V01'),'T07':('L01','V01'),'T08':('L02','V01'),
    'T09':('L05','V05'),'T10':('L05','V05'),'T11':('L05','V05'),'T12':('L11','V05'),
    'T13':('L07','V01'),'T14':('L04','V01'),'T15':('L07','V01'),'T16':('L02','V01'),
    'T17':('L08','V01'),'T18':('L05','V05'),'T19':('L11','V01'),'T20':('L02','V01'),
    'T21':('L02','V01'),'T22':('L02','V01'),'T23':('L07','V01'),'T24':('L02','V01'),
    'T25':('L07','V01'),'T26':('L02','V01'),'T27':('L02','V01'),'T28':('L02','V01'),
    'T29':('L02','V01'),'T30':('L08','V01'),'T31':('L01','V01'),'T32':('L07','V01'),
    'T33':('L02','V01'),'T34':('L02','V01'),'T35':('L01','V01'),'T36':('L04','V01'),
    'T37':('L05','V05'),'T38':('L07','V01'),'T39':('L02','V01'),'T40':('L02','V01'),
    'T41':('L07','V01'),'T42':('L04','V01'),'T43':('L01','V03'),'T44':('L01','V05'),
    'T45':('L07','V01'),'T46':('L06','V01'),'T47':('L05','V05'),'T48':('L06','V01')}
