"""Original editable mechanism blueprints. SVG sidecars are rendered from the same JSON geometry.
These are reusable structural patterns, not literal reproductions of cited papers.
"""
from pathlib import Path
import json, html, math, textwrap, xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1]
COLORS={'input':('#E4F0E8','#63836B'),'module':('#E4EDF6','#637E9E'),'attention':('#EEE7F4','#89719C'),'latent':('#FFF1D7','#AE8C4C'),'loss':('#F7E5E4','#B67975'),'neutral':('#F1F3F5','#7F8994')}
CATS=['01_视觉网络与编码解码','02_Transformer与注意力','03_图神经网络与关系推理','04_生成模型与扩散机制','05_检索增强与知识系统','06_多模态与跨模态融合','07_强化学习与智能体','08_训练策略与自监督','09_三维视觉与神经渲染','10_计算机系统与数据流程','11_因果与AI科学机制','12_通用方法与总体框架']
SPECS=[]
def N(id,label,x,y,kind='module',shape='box',w=170,h=68):return dict(id=id,label=label,x=x,y=y,w=w,h=h,kind=kind,shape=shape)
def E(a,b,label='',style='solid',via=None):return dict(source=a,target=b,label=label,style=style,via=via or [])
def G(title,x,y,w,h):return dict(title=title,x=x,y=y,w=w,h=h)
def add(cat,slug,title,description,nodes,edges,groups=None,tips=None):
 SPECS.append(dict(id=f'T{len(SPECS)+1:02}',category=CATS[cat-1],slug=slug,title=title,description=description,nodes=nodes,edges=edges,groups=groups or [],tips=tips or ['替换模块名称、输入输出和张量维度。','保留主要信息流方向，新增分支放在空白区域。','虚线仅表示辅助联系；按真实方法修改箭头语义。'],width=1320,height=max(720,max(n['y']+n['h'] for n in nodes)+130)))
def row(labels,y=300,x=65,gap=210,kinds=None):
 return [N(str(i),label,x+i*gap,y,(kinds or ['module']*len(labels))[i]) for i,label in enumerate(labels)]
def seq(nodes):return [E(a['id'],b['id']) for a,b in zip(nodes,nodes[1:])]
# 01: spatial and multiscale network layouts.
n=row(['Image\nB x 3 x H x W','Conv stem\nB x C x H/4 x W/4','Residual stages\nC -> 2C -> 4C','Global pooling\nB x 4C','Prediction head\nB x K'],kinds=['input','module','module','latent','input']);add(1,'cnn_backbone','CNN backbone and prediction head','卷积网络的主干—特征—任务头结构，适合分类与特征提取总览。',n,seq(n))
n=[N('x','Input feature x',70,315,'input'),N('c1','Conv + Norm',330,315),N('c2','Activation + Conv',570,315),N('sum','+',835,319,'latent','ellipse',60,60),N('out','Output: x + F(x)',1010,315,'input')];add(1,'residual_block','Residual block with identity path','实线主路径与上方残差旁路分开，突出模块新增计算。',n,[E('x','c1'),E('c1','c2'),E('c2','sum'),E('sum','out'),E('x','sum','identity','dashed',[(155,230),(865,230)])])
n=[N('e1','Encoder 1\nH x W',65,210),N('e2','Encoder 2\nH/2 x W/2',295,325),N('b','Bottleneck\nH/4 x W/4',545,440,'attention'),N('d2','Decoder 2\nH/2 x W/2',795,325),N('d1','Decoder 1\nH x W',1025,210),N('o','Segmentation map',1025,495,'input')];add(1,'unet_skip','U-shaped encoder-decoder','U 形层级结构与跨层跳连；箭头表示 concat / add 的位置应按方法替换。',n,[E('e1','e2','downsample'),E('e2','b','downsample'),E('b','d2','upsample'),E('d2','d1','upsample'),E('d1','o'),E('e1','d1','skip connection','dashed',[(150,150),(1110,150)]),E('e2','d2','skip connection','dashed',[(380,265),(880,265)])])
n=[N('c2','Backbone C2',125,200),N('c3','Backbone C3',125,330),N('c4','Backbone C4',125,460),N('p2','Lateral + fuse P2',545,200,'attention'),N('p3','Lateral + fuse P3',545,330,'attention'),N('p4','Lateral + fuse P4',545,460,'attention'),N('head','Multi-scale head',1005,330,'input')];add(1,'feature_pyramid','Feature pyramid and lateral fusion','左右层级对齐，适合 FPN、金字塔特征融合和多尺度检测。',n,[E('c2','c3'),E('c3','c4'),E('c2','p2'),E('c3','p3'),E('c4','p4'),E('p4','p3','up'),E('p3','p2','up'),E('p2','head'),E('p3','head'),E('p4','head')],[G('Backbone',75,140,280,410),G('Feature pyramid',490,140,280,410)])
# 02: transformer and state-space structures.
n=[N('tok','Source tokens',65,210,'input'),N('emb','Embedding + position',285,210),N('enc','Encoder stack\nSelf-attn -> FFN',525,210,'attention'),N('tgt','Target tokens',65,450,'input'),N('temb','Shifted embedding',285,450),N('dec','Decoder stack\nMasked + cross-attn',765,450,'attention'),N('prob','Linear + softmax',1045,450,'input')];add(2,'transformer_encoder_decoder','Transformer encoder-decoder overview','上下双通路展示源端编码、目标端自回归与跨注意力。',n,[E('tok','emb'),E('emb','enc'),E('tgt','temb'),E('temb','dec'),E('enc','dec','K, V'),E('dec','prob')],[G('Source sequence',40,150,670,170),G('Autoregressive target sequence',40,390,1200,170)])
n=[N('x','Input tokens X\nB x T x D',65,335,'input'),N('q','Query projection Q',320,185,'attention'),N('k','Key projection K',320,335,'attention'),N('v','Value projection V',320,485,'attention'),N('s','QK^T / sqrt(d)\nsoftmax over keys',640,250,'latent',w=205),N('a','Weighted values\nA V',910,335,'attention'),N('o','Output projection',1130,335,'input',w=150)];add(2,'qkv_attention','Q-K-V attention mechanism','三路投影和两阶段矩阵计算分开展示；这里的 A 是注意力权重，不是统计热图。',n,[E('x','q'),E('x','k'),E('x','v'),E('q','s'),E('k','s'),E('s','a','A'),E('v','a','V'),E('a','o')])
n=row(['Image\nH x W x C','Patchify\np x p patches','Patch embedding\nN x D + position','Transformer blocks\nN x D','CLS / pooled head'],kinds=['input','module','latent','attention','input']);add(2,'vit_patch_tokens','Vision Transformer token pipeline','图像到 patch、token 序列、Transformer 和任务头，适合 ViT 类方法。',n,seq(n)+[E('1','3','class token + position','dashed',[(360,210),(780,210)])])
n=[N('x','Token sequence',65,310,'input'),N('proj','Input projection',285,310),N('conv','Local convolution',525,210),N('ssm','Selective state space\ns_t = A_t s_(t-1) + B_t x_t',765,210,'attention',w=245),N('gate','Gating branch',525,435,'latent'),N('mul','x',1075,320,'latent','ellipse',60,60),N('out','Output projection',1070,500,'input')];add(2,'state_space','State-space block with gating','局部卷积、状态更新和乘性门控的机制示意，需按具体 SSM 实现调整。',n,[E('x','proj'),E('proj','conv'),E('conv','ssm'),E('proj','gate'),E('ssm','mul'),E('gate','mul'),E('mul','out')])
# 03: graph diagrams use actual node-link geometry, not only module boxes.
n=[N('v','v',350,345,'attention','ellipse',62,62),N('u1','u1',130,220,'input','ellipse',60,60),N('u2','u2',130,470,'input','ellipse',60,60),N('u3','u3',480,190,'input','ellipse',60,60),N('agg','Aggregate neighbors\nSUM / MEAN',685,330,'latent',w=210),N('upd','Update node feature\nh_v^(l+1)',1035,330,'input',w=205)];add(3,'message_passing','Neighborhood message passing','节点—边结构突出邻居消息汇聚和目标节点更新。',n,[E('u1','v','m_1v'),E('u2','v','m_2v'),E('u3','v','m_3v'),E('v','agg'),E('agg','upd')],[G('Local graph neighborhood',80,145,525,455)])
n=[N('v','v',360,345,'attention','ellipse',66,66),N('u1','u1',140,210,'input','ellipse',62,62),N('u2','u2',140,480,'input','ellipse',62,62),N('u3','u3',490,205,'input','ellipse',62,62),N('h1','Attention head 1',715,200,'attention'),N('h2','Attention head 2',715,365,'attention'),N('h3','Attention head H',715,525,'attention'),N('cat','Concat / average\nNode output',1045,365,'input')];add(3,'graph_attention','Graph attention and multi-head aggregation','权重标在真实图边上；右侧展示多头聚合，不使用统计热图。',n,[E('u1','v','alpha_v1'),E('u2','v','alpha_v2'),E('u3','v','alpha_v3'),E('v','h1'),E('v','h2'),E('v','h3'),E('h1','cat'),E('h2','cat'),E('h3','cat')])
n=[N('user','User node',115,210,'input','ellipse',120,72),N('item','Item node',115,465,'latent','ellipse',120,72),N('rel1','User-item relation',435,210),N('rel2','Item-item relation',435,465),N('agg','Relation-aware\naggregation',775,340,'attention'),N('pred','Link prediction',1075,340,'input')];add(3,'heterogeneous_graph','Heterogeneous graph relations','用节点颜色和关系分支区分异构实体，适合推荐与知识图谱。',n,[E('user','rel1','interacts'),E('item','rel1'),E('item','rel2','similar'),E('rel1','agg'),E('rel2','agg'),E('agg','pred')])
n=[N('g1','Fine graph\nNode embeddings',100,310,'input',shape='graph',w=210,h=150),N('pool','Learned assignment\nS: N x K',425,340,'attention'),N('g2','Coarsened graph\nK supernodes',760,310,'latent',shape='graph',w=210,h=150),N('read','Graph readout',1080,350,'input')];add(3,'hierarchical_graph','Hierarchical graph pooling','真实节点图元加聚合模块，展示图到粗粒度图再到图级表示。',n,[E('g1','pool'),E('pool','g2','pool'),E('g2','read')])
# 04: generative mechanisms.
n=[N('x0','Clean sample x_0',75,230,'input'),N('xt','Noisy sample x_t',420,230,'latent'),N('xT','Noise x_T',765,230,'neutral'),N('net','Denoiser epsilon_theta\ncondition + time t',420,460,'attention',w=245),N('out','Reconstructed sample',1035,460,'input')];add(4,'diffusion_forward_reverse','Forward noising and reverse denoising','上下分层区分前向加噪与学习的反向去噪，避免把两个方向混成一条线。',n,[E('x0','xt','q(x_t | x_0)'),E('xt','xT','noise schedule'),E('xT','net','reverse sampling'),E('net','out'),E('xt','net','training input','dashed')],[G('Forward process',40,165,1210,160),G('Learned reverse process',40,390,1210,190)])
n=[N('im','Image x',70,250,'input'),N('enc','Image encoder',300,250),N('z','Latent z',530,250,'latent'),N('unet','Latent denoising U-Net',775,250,'attention',w=215),N('dec','Image decoder',1040,250),N('text','Text / condition',300,480,'input'),N('ce','Condition encoder',575,480),N('ca','Cross-attention',860,480,'attention')];add(4,'latent_diffusion','Latent diffusion with conditioning','编码到潜空间、条件注入与图像解码，适合条件生成总图。',n,[E('im','enc'),E('enc','z'),E('z','unet'),E('unet','dec'),E('text','ce'),E('ce','ca'),E('ca','unet','K,V')],[G('Latent-space generator',40,175,1220,190)])
n=[N('noise','Noise z',85,190,'latent'),N('gen','Generator G',390,190,'attention'),N('fake','Generated sample',710,190,'input'),N('real','Real sample',710,440,'input'),N('disc','Discriminator D',1030,320,'module'),N('loss','Adversarial objective',400,480,'loss',w=230)];add(4,'gan_adversarial','Adversarial generator-discriminator loop','真假样本合流及训练反馈放在下方，适合 GAN 与对抗机制。',n,[E('noise','gen'),E('gen','fake'),E('fake','disc'),E('real','disc'),E('disc','loss','training feedback','dashed',[(1190,580),(515,580)]),E('loss','gen','update G','dashed')])
n=[N('x','Input x',65,335,'input'),N('enc','Encoder q(z|x)',295,335),N('mu','Mean mu',545,210,'latent'),N('sd','Scale sigma',545,455,'latent'),N('s','Reparameterize\nz = mu + sigma * eps',790,335,'attention',w=225),N('dec','Decoder p(x|z)',1070,335,'input'),N('eps','eps ~ N(0, I)',790,520,'neutral')];add(4,'vae_latent','Variational latent reparameterization','概率变量与采样节点分开，清晰显示可微重参数化结构。',n,[E('x','enc'),E('enc','mu'),E('enc','sd'),E('mu','s'),E('sd','s'),E('eps','s'),E('s','dec')])
# 05 retrieval and knowledge mechanisms.
n=[N('docs','Documents',70,190,'input'),N('chunk','Chunk + embed',330,190),N('index','Vector index',620,190,'latent','database'),N('q','User query',70,465,'input'),N('ret','Retrieve top-k',620,465),N('ctx','Context assembly',890,465,'attention'),N('ans','LLM answer',1130,465,'input',w=150)];add(5,'rag_online_offline','RAG offline index and online answering','离线索引和在线问答分轨，便于论文方法总览。',n,[E('docs','chunk'),E('chunk','index'),E('q','ret','query embedding'),E('index','ret','nearest neighbors'),E('ret','ctx'),E('ctx','ans')],[G('Offline indexing',40,135,1225,165),G('Online inference',40,390,1225,185)])
n=[N('docs','Corpus',65,285,'input'),N('extract','Entity + relation\nextraction',315,285),N('kg','Knowledge graph',580,255,'latent','graph',w=210,h=130),N('q','Question',335,490,'input'),N('sub','Subgraph retrieval',850,285,'attention'),N('gen','Evidence-grounded\nanswer',1100,285,'input')];add(5,'graph_rag','Graph-based retrieval and evidence path','知识图谱、查询与子图证据分开展示，适合 GraphRAG 类结构。',n,[E('docs','extract'),E('extract','kg'),E('kg','sub'),E('q','sub'),E('sub','gen')])
n=[N('q','Query',65,320,'input'),N('router','Route?',330,315,'latent','diamond',150,90),N('dense','Dense retriever',650,190),N('sparse','Sparse retriever',650,450),N('rank','Merge + rerank',930,320,'attention'),N('out','Retrieved context',1130,320,'input',w=155)];add(5,'hybrid_retrieval','Hybrid retrieval and routing','决策节点、双检索分支与汇合，适合混合检索或自适应路径选择。',n,[E('q','router'),E('router','dense','semantic'),E('router','sparse','lexical'),E('dense','rank'),E('sparse','rank'),E('rank','out')])
# 06 multimodal mechanisms.
n=[N('im','Images',70,210,'input'),N('ie','Image encoder',350,210),N('iv','Image embeddings',655,210,'latent'),N('txt','Texts',70,465,'input'),N('te','Text encoder',350,465),N('tv','Text embeddings',655,465,'latent'),N('obj','Cross-modal alignment\ncontrastive objective',1005,335,'loss',w=245)];add(6,'dual_encoder','Dual encoder and cross-modal alignment','两种模态各自编码，右侧显示对齐目标；适合 CLIP 类机制。',n,[E('im','ie'),E('ie','iv'),E('txt','te'),E('te','tv'),E('iv','obj'),E('tv','obj')],[G('Visual branch',40,155,855,150),G('Language branch',40,405,855,150)])
n=[N('a','Modality A tokens',80,220,'input'),N('b','Modality B tokens',80,450,'input'),N('qa','Projection Q',370,220),N('kv','Projection K,V',370,450),N('cross','Cross-attention\nQ_A attends to K_B,V_B',700,320,'attention',w=260),N('out','Fused representation',1060,320,'input',w=210)];add(6,'cross_modal_fusion','Cross-modal attention fusion','明确 Q 与 K/V 来自不同模态，便于展示交互模块创新。',n,[E('a','qa'),E('b','kv'),E('qa','cross'),E('kv','cross'),E('cross','out')])
n=[N('v','Video frames',65,195,'input'),N('a','Audio waveform',65,435,'input'),N('ve','Visual encoder',345,195),N('ae','Audio encoder',345,435),N('align','Temporal alignment',665,315,'latent'),N('fuse','Fusion block',955,315,'attention'),N('out','Prediction',955,515,'input')];add(6,'audio_visual','Audio-visual temporal fusion','时间对齐作为独立模块，适合音视频识别和事件理解。',n,[E('v','ve'),E('a','ae'),E('ve','align'),E('ae','align'),E('align','fuse'),E('fuse','out')])
# 07 RL and agent loops.
n=[N('env','Environment',80,315,'input',w=215),N('obs','Observation encoder',420,210),N('actor','Actor pi(a|s)',730,210,'attention'),N('critic','Critic V(s) / Q(s,a)',730,465,'latent',w=215),N('buf','Replay / rollout',420,465,'neutral','database')];add(7,'actor_critic','Actor-critic interaction and learning','实线交互环与虚线训练支路分开，适合强化学习系统总览。',n,[E('env','obs','state / observation'),E('obs','actor'),E('actor','env','action','solid',[(815,145),(190,145)]),E('env','buf','transition'),E('buf','critic'),E('critic','actor','learning signal','dashed')])
n=[N('env','Shared environment',70,330,'input',w=220),N('a1','Agent 1\nLocal policy',450,160,'attention'),N('a2','Agent 2\nLocal policy',450,330,'attention'),N('a3','Agent N\nLocal policy',450,500,'attention'),N('central','Central critic / mixer\nTraining only',860,330,'latent',w=270),N('loss','Joint objective',890,560,'loss',w=215)];add(7,'multi_agent_ctde','Multi-agent centralized training','多智能体并行结构；集中模块是训练时使用的可选结构，按 CTDE 方法修改。',n,[E('env','a1'),E('env','a2'),E('env','a3'),E('a1','central','trajectory','dashed'),E('a2','central','trajectory','dashed'),E('a3','central','trajectory','dashed'),E('central','loss'),E('a1','env','action','solid',[(430,125),(50,125),(50,365)]),E('a3','env','action','solid',[(430,600),(50,600),(50,365)])])
n=[N('task','Task + context',75,310,'input'),N('plan','Planner',365,180,'attention'),N('act','Tool executor',705,180),N('tools','External tools',1040,180,'neutral','database'),N('obs','Observation',705,465,'input'),N('mem','Working memory',365,465,'latent','database'),N('answer','Final answer',1040,465,'input')];add(7,'tool_agent_loop','Tool-using agent loop','规划、执行、观测和记忆构成闭环，最后输出与工具交互分开。',n,[E('task','plan'),E('plan','act','tool call'),E('act','tools'),E('tools','obs','tool result'),E('obs','mem'),E('mem','plan','updated context'),E('plan','answer','finish','dashed',[(600,115),(1250,115),(1250,500)])])
n=[N('task','Problem',65,330,'input'),N('coord','Coordinator',340,330,'attention'),N('w1','Research agent',665,160),N('w2','Coding agent',665,330),N('w3','Verifier agent',665,500),N('merge','Synthesize + verify',1050,330,'latent',w=205)];add(7,'agent_orchestration','Coordinator and specialist agents','中心分派、多路协作与结果汇合，适合 LLM 多智能体方法图。',n,[E('task','coord'),E('coord','w1'),E('coord','w2'),E('coord','w3'),E('w1','merge'),E('w2','merge'),E('w3','merge')])
# 08 learning mechanisms, not numerical charts.
n=[N('x','Unlabeled sample',75,340,'input'),N('v1','Augmented view 1',360,200),N('v2','Augmented view 2',360,475),N('e1','Encoder + projector',685,200,'attention',w=210),N('e2','Encoder + projector',685,475,'attention',w=210),N('loss','Contrastive objective',1040,340,'loss',w=205)];add(8,'contrastive_views','Two-view contrastive learning','双视图增强、共享编码与对比目标，适合 SimCLR 类训练机制。',n,[E('x','v1'),E('x','v2'),E('v1','e1'),E('v2','e2'),E('e1','loss'),E('e2','loss'),E('e1','e2','shared weights','dashed')])
n=[N('x','Training sample',75,330,'input'),N('teacher','Teacher network\nFrozen / EMA',405,180,'neutral',w=210),N('student','Student network\nTrainable',405,450,'attention',w=210),N('t','Teacher features',745,180,'latent'),N('s','Student features',745,450,'latent'),N('loss','Distillation objective',1060,330,'loss',w=205)];add(8,'teacher_student','Teacher-student distillation','冻结与可训练参数用颜色区别，目标和特征路径分开。',n,[E('x','teacher'),E('x','student'),E('teacher','t'),E('student','s'),E('t','loss','stop gradient','dashed'),E('s','loss')])
n=[N('image','Image patches',70,310,'input'),N('mask','Mask sampling',330,310,'latent'),N('enc','Visible-token encoder',620,210,'attention',w=220),N('token','Mask tokens',620,460,'neutral'),N('dec','Reconstruction decoder',930,310,w=240),N('loss','Masked-patch objective',930,520,'loss',w=240)];add(8,'masked_autoencoder','Masked autoencoder mechanism','编码器仅处理可见 token，掩码 token 在解码端注入。',n,[E('image','mask'),E('mask','enc','visible'),E('enc','dec'),E('token','dec','insert mask tokens'),E('dec','loss')])
n=[N('train','Training data',70,195,'input'),N('model','Shared model',410,195,'attention'),N('loss','Objective + update',790,195,'loss'),N('test','New input',70,470,'input'),N('copy','Model parameters\nInference mode',410,470,'attention'),N('out','Prediction',790,470,'input')];add(8,'train_inference_lanes','Training and inference separation','上下泳道拆分训练更新与推理前向，适合整篇方法总览。',n,[E('train','model'),E('model','loss'),E('loss','model','gradient update','dashed',[(1000,130),(495,130)]),E('model','copy','parameters','dashed'),E('test','copy'),E('copy','out')],[G('Training',40,145,1210,165),G('Inference',40,405,1210,165)])
# 09 3D and neural graphics.
n=[N('ray','Camera ray',65,310,'input'),N('sample','Sample 3D positions\n(x,y,z), direction',330,310,w=215),N('enc','Position encoding',630,310,'latent'),N('mlp','Radiance field MLP\ncolor + density',895,310,'attention',w=225),N('render','Volume rendering\nPixel color',895,510,'input',w=225)];add(9,'nerf_rendering','Neural radiance field rendering','射线采样、位置编码与体渲染作为不同语义模块。',n,[E('ray','sample'),E('sample','enc'),E('enc','mlp'),E('mlp','render')])
n=[N('views','Multi-view images',65,215,'input'),N('init','SfM initialization',350,215),N('gauss','3D Gaussian primitives\nposition, covariance, color',655,215,'latent',w=250),N('rast','Differentiable\nsplat rasterization',1000,215,'attention',w=250),N('target','Target view',355,475,'input'),N('loss','Image objective',715,475,'loss'),N('adapt','Densify / prune\nOptimize parameters',1000,475,'module',w=250)];add(9,'gaussian_splatting','Gaussian splatting optimization loop','表示、可微渲染和密度控制分支，适合 3D Gaussian Splatting 类方法。',n,[E('views','init'),E('init','gauss'),E('gauss','rast'),E('rast','loss'),E('target','loss'),E('loss','adapt'),E('adapt','gauss','parameter update','dashed')])
n=row(['Point cloud\nN x 3','Shared point MLP\nN x C','Symmetric pooling\n1 x C','Global + local fuse\nN x 2C','Per-point prediction'],kinds=['input','module','latent','attention','input']);add(9,'point_cloud','Point-set encoder with global-local fusion','无序点集的共享变换、对称池化与局部特征回传。',n,seq(n)+[E('1','3','point features','dashed',[(360,215),(780,215)])])
# 10 computer systems / data flows.
n=[N('client','Clients',70,315,'input'),N('route','Request router',335,315),N('w1','Worker 1',650,155),N('w2','Worker 2',650,315),N('w3','Worker N',650,475),N('store','Shared storage',1035,315,'latent','database')];add(10,'distributed_workers','Distributed worker and storage architecture','分发、并行执行和共享存储，适合分布式计算系统架构。',n,[E('client','route'),E('route','w1'),E('route','w2'),E('route','w3'),E('w1','store'),E('w2','store'),E('w3','store')],[G('Compute cluster',580,110,310,465)])
n=row(['Event sources','Message broker','Stream operator\nWindow + state','Result sink','Serving layer'],kinds=['input','latent','attention','neutral','input']);n[1]['shape']='database';n[3]['shape']='database';add(10,'stream_processing','Stateful stream-processing flow','事件流与状态更新分开，适合流式系统和在线数据处理。',n,seq(n))
n=[N('q','Query',65,320,'input'),N('parse','Parse + logical plan',320,320,w=220),N('opt','Cost / neural optimizer',645,320,'attention',w=230),N('exec','Physical execution',1010,320,w=210),N('meta','Catalog + statistics\nMetadata input only',645,515,'latent','database',w=230),N('data','Data storage',1010,515,'neutral','database',w=210)];add(10,'query_optimizer','Query planning and execution architecture','查询编译、优化器和执行器是主要链路；元数据是模块输入，不绘制统计图。',n,[E('q','parse'),E('parse','opt'),E('opt','exec'),E('meta','opt'),E('data','exec')])
# 11 causal/scientific AI mechanisms.
n=[N('u','Confounder U',535,160,'neutral','ellipse',150,75),N('x','Treatment X',245,395,'input','ellipse',150,75),N('m','Mediator M',585,395,'latent','ellipse',150,75),N('y','Outcome Y',940,395,'attention','ellipse',150,75),N('do','Intervention do(X)',200,570,'loss',w=230)];add(11,'causal_dag','Causal mechanism and intervention DAG','因果方向、混杂与中介分开；干预边按实际假设修改。',n,[E('u','x'),E('u','y'),E('x','m'),E('m','y'),E('x','y','direct effect','solid',[(320,520),(1015,520)]),E('do','x','intervention','dashed')])
n=[N('stim','Stimulus / input',80,310,'input'),N('rnn','Recurrent circuit\nState h_t',440,310,'attention',w=225),N('read','Readout',810,310),N('task','Task behavior',810,510,'input'),N('constraint','Spatial / wiring\nconstraint',440,510,'latent',w=225)];add(11,'recurrent_circuit','Recurrent circuit with structural constraints','功能输入、循环状态与结构约束的机制示意。',n,[E('stim','rnn'),E('rnn','read'),E('read','task'),E('constraint','rnn','regularization','dashed'),E('rnn','rnn','recurrent state','solid',[(715,250),(715,175),(410,175),(410,340)])])
n=[N('seq','Sequence / entity inputs',70,190,'input',w=230),N('pair','Pairwise representation',70,450,'latent',w=230),N('trunk','Representation trunk\nInteraction updates',420,320,'attention',w=245),N('gen','Structure generation\nDenoising / refinement',780,320,'attention',w=245),N('struct','Predicted structure',1080,320,'input',w=205)];add(11,'ai_science_structure','Representation-to-structure mechanism','多类型表示到结构生成的通用 AI 科学框架；不是 AlphaFold 的精确复刻。',n,[E('seq','trunk'),E('pair','trunk'),E('trunk','gen'),E('gen','struct')])
# 12 composition and algorithm templates.
n=[N('input','(a) Input / problem',65,330,'input',w=220),N('base','Baseline processing',395,210,'neutral',w=220),N('novel','(b) Proposed module\nYour contribution',395,465,'attention',w=245),N('fuse','Feature integration',780,330,'latent',w=220),N('out','(c) Output',1080,330,'input',w=190)];add(12,'contribution_overview','Contribution-first method overview','中间突出创新模块，适合论文 Figure 1 / method overview。',n,[E('input','base'),E('input','novel'),E('base','fuse'),E('novel','fuse'),E('fuse','out')],[G('Method',340,145,720,455)])
n=[N('start','Start',100,200,'input','ellipse'),N('init','Initialize state',400,200),N('check','Converged?',750,195,'latent','diamond',165,90),N('end','Return output',1050,200,'input','ellipse'),N('update','Update / refine',750,480,'attention'),N('eval','Evaluate criterion',400,480)];add(12,'algorithm_iteration','Iterative algorithm with decision branch','终止条件、迭代更新与返回分支清楚标记，适合算法流程图。',n,[E('start','init'),E('init','check'),E('check','end','Yes'),E('check','update','No'),E('update','eval'),E('eval','check','next iteration','solid',[(355,590),(700,590),(700,240)])])
n=[N('big','System overview',70,285,'input',w=230),N('module','Highlighted module',440,285,'attention',w=235),N('output','System output',795,285,'input',w=210),N('step1','Internal step A',380,520),N('step2','Internal step B',635,520),N('step3','Internal step C',890,520)];add(12,'overview_zoom','Overview with module zoom-in','上方总图与下方模块细节形成两级叙事，适合方法模块解释。',n,[E('big','module'),E('module','output'),E('module','step1','zoom-in','dashed'),E('step1','step2'),E('step2','step3')],[G('Module detail',325,450,810,165)])

# Additional visual primitives: feature cubes, actual neurons, tokens and temporal graphs.
n=[N('im','Input image\nH x W x 3',65,300,'input','cube',155,155),N('f1','Feature map\nH/2 x W/2 x C',330,320,'module','cube',165,120),N('f2','Feature map\nH/4 x W/4 x 2C',605,340,'module','cube',165,90),N('f3','Feature map\nH/8 x W/8 x 4C',880,350,'attention','cube',155,70),N('out','Task head',1110,350,'input',w=155)];add(1,'feature_tensor_cubes','Feature tensors and convolution stages','可编辑立体特征图图元展示空间分辨率下降和通道变化，不要求读者只靠方框理解张量。',n,[E('im','f1','Conv / stride 2'),E('f1','f2','Conv / stride 2'),E('f2','f3','Conv / stride 2'),E('f3','out')])
n=[];edges=[];layers=[(150,3),(440,5),(750,5),(1090,2)]
for l,(x,count) in enumerate(layers):
 for j in range(count):n.append(N(f'l{l}_{j}',f'x{j+1}' if l==0 else (f'y{j+1}' if l==3 else ''),x,340+(j-(count-1)/2)*83,'input' if l in [0,3] else 'attention','ellipse',48,48))
for l in range(3):
 for a in range(layers[l][1]):
  for b in range(layers[l+1][1]):edges.append(E(f'l{l}_{a}',f'l{l+1}_{b}'))
add(1,'neuron_layers','Neural network as neuron-node layers','每个神经元与连接都可编辑，适合小型全连接网络、神经网络机制解释。',n,edges,[G('Input',105,160,150,420),G('Hidden layer 1',395,120,150,500),G('Hidden layer 2',705,120,150,500),G('Output',1045,160,150,420)])
for e in SPECS[-1]['edges']:e['straight']=True
n=[];edges=[]
for i in range(4):
 x=110+i*290;n.extend([N(f'x{i}',f'Input x_{i}',x,185,'input'),N(f'h{i}',f'Recurrent cell\nh_{i} = f(x_{i}, h_{i-1})',x,340,'attention',w=210),N(f'y{i}',f'Output y_{i}',x,500,'input')]);edges.extend([E(f'x{i}',f'h{i}'),E(f'h{i}',f'y{i}')])
 if i:edges.append(E(f'h{i-1}',f'h{i}','state'))
add(2,'rnn_unrolled','Recurrent computation unrolled in time','按时间步展开循环神经网络，同色模块表示参数共享，横向箭头表示状态传递。',n,edges)
n=[N('img','Image patches',65,280,'input','cube',165,155),N('enc','Transformer encoder',760,325,'attention',w=235),N('out','Prediction',1085,325,'input')];edges=[E('img','p0','patch embedding'),E('p0','enc'),E('enc','out')]
for i in range(8):n.append(N(f'p{i}',('C' if i==0 else str(i)),370+i*40,325,'latent' if i==0 else 'module','box',31,70))
add(2,'patch_token_strip','Patch image and editable token strip','每个 token 为独立图元，C 表示 CLS token；可替换为 mask、时间或模态 token。',n,edges,[G('Embedded token sequence',335,250,365,175)])
n=[];edges=[]
for i in range(3):
 x=140+i*390
 for j,(dx,dy) in enumerate([(0,0),(105,-75),(105,75),(210,0)]):n.append(N(f'g{i}_{j}',str(j+1),x+dx,340+dy,'attention' if j==0 else 'input','ellipse',48,48))
 for a,b in [(0,1),(0,2),(1,3),(2,3)]:edges.append(E(f'g{i}_{a}',f'g{i}_{b}'))
 if i:edges.append(E(f'g{i-1}_3',f'g{i}_0','t -> t+1','dashed'))
add(3,'temporal_graph','Temporal graph and node-state evolution','三个时间切片均为可编辑节点—边图，虚线连接表示跨时间状态变化。',n,edges,[G(f'Time step {i}',105+i*390,200,305,330) for i in range(3)])
n=[N('image','Visual tokens',65,220,'input','cube',175,110),N('text','Language tokens',65,460,'input'),N('ve','Visual backbone',370,220),N('te','Language backbone',370,460),N('merge','Shared fusion tokens',955,335,'attention',w=250)];edges=[E('image','ve'),E('text','te'),E('ve','v0'),E('te','t0'),E('v4','merge'),E('t4','merge')]
for i in range(5):n.extend([N(f'v{i}',str(i+1),650+i*38,220,'module','box',29,65),N(f't{i}',str(i+1),650+i*38,460,'latent','box',29,65)]);edges.append(E(f'v{i}',f't{i}','','dashed'))
add(6,'modality_token_alignment','Token-level cross-modal interactions','上下 token 对应边展示模态对齐和交互机制，可改为稀疏或全连接交互。',n,edges)

def paths(spec,e):
 nodes={n['id']:n for n in spec['nodes']};a,b=nodes[e['source']],nodes[e['target']]
 ac=(a['x']+a['w']/2,a['y']+a['h']/2);bc=(b['x']+b['w']/2,b['y']+b['h']/2)
 if e.get('straight'):
  dx,dy=bc[0]-ac[0],bc[1]-ac[1];length=math.hypot(dx,dy);ux,uy=dx/length,dy/length
  return [(ac[0]+ux*a['w']/2,ac[1]+uy*a['h']/2),(bc[0]-ux*b['w']/2,bc[1]-uy*b['h']/2)]
 if e['via']:
  def anchor(n,p):
   cx,cy=n['x']+n['w']/2,n['y']+n['h']/2;dx,dy=p[0]-cx,p[1]-cy
   if abs(dx)/n['w']>abs(dy)/n['h']:return (n['x']+(n['w'] if dx>0 else 0),cy)
   return (cx,n['y']+(n['h'] if dy>0 else 0))
  pts=[anchor(a,e['via'][0])]+[tuple(p) for p in e['via']]+[anchor(b,e['via'][-1])]
 elif abs(ac[0]-bc[0])<35:
  pts=[(ac[0],a['y']+(a['h'] if bc[1]>ac[1] else 0)),(bc[0],b['y']+(0 if bc[1]>ac[1] else b['h']))]
 elif abs(ac[1]-bc[1])<35:
  pts=[(a['x']+(a['w'] if bc[0]>ac[0] else 0),ac[1]),(b['x']+(0 if bc[0]>ac[0] else b['w']),bc[1])]
 else:
  start=(a['x']+(a['w'] if bc[0]>ac[0] else 0),ac[1]);end=(b['x']+(0 if bc[0]>ac[0] else b['w']),bc[1]);mid=(start[0]+end[0])/2
  pts=[start,(mid,start[1]),(mid,end[1]),end]
 return pts
def render_svg(spec):
 W,H=spec['width'],spec['height'];esc=html.escape
 s=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{esc(spec["title"])}">', '<defs><marker id="arrow" markerWidth="10" markerHeight="8" refX="9" refY="4" orient="auto" markerUnits="userSpaceOnUse"><path d="M0,0 L10,4 L0,8 Z" fill="#647284"/></marker></defs>',f'<rect width="{W}" height="{H}" fill="white"/>','<g font-family="Arial, Helvetica, sans-serif" fill="#243247">',f'<text x="48" y="52" font-size="27" font-weight="700">{spec["id"]} / {esc(spec["title"])}</text>','<text x="48" y="84" font-size="14" fill="#738093">EDITABLE MECHANISM BLUEPRINT / Generic structure; adapt to your method</text>']
 for g in spec['groups']:
  s += [f'<rect x="{g["x"]}" y="{g["y"]}" width="{g["w"]}" height="{g["h"]}" rx="12" fill="#FAFBFD" stroke="#CCD4DD" stroke-dasharray="5 4"/>',f'<text x="{g["x"]+16}" y="{g["y"]+25}" font-size="15" font-weight="700" fill="#68778A">{esc(g["title"])}</text>']
 for e in spec['edges']:
  p=paths(spec,e);d='M '+' L '.join(f'{x},{y}' for x,y in p);dash=' stroke-dasharray="6 4"' if e['style']=='dashed' else ''
  s.append(f'<path d="{d}" fill="none" stroke="#647284" stroke-width="1.7"{dash} marker-end="url(#arrow)"/>')
  if e['label']:
   lens=[math.hypot(p[i+1][0]-p[i][0],p[i+1][1]-p[i][1]) for i in range(len(p)-1)];idx=max(range(len(lens)),key=lambda i:lens[i]);x=(p[idx][0]+p[idx+1][0])/2;y=(p[idx][1]+p[idx+1][1])/2-7;label=e['label'];tw=len(label)*7+12
   s += [f'<rect x="{x-tw/2}" y="{y-14}" width="{tw}" height="19" rx="3" fill="white"/>',f'<text x="{x}" y="{y}" text-anchor="middle" font-size="12" fill="#516173">{esc(label)}</text>']
 for n in spec['nodes']:
  x,y,w,h=n['x'],n['y'],n['w'],n['h'];fill,stroke=COLORS[n['kind']];shape=n['shape']
  if shape=='ellipse':s.append(f'<ellipse cx="{x+w/2}" cy="{y+h/2}" rx="{w/2}" ry="{h/2}" fill="{fill}" stroke="{stroke}" stroke-width="1.6"/>')
  elif shape=='diamond':s.append(f'<polygon points="{x+w/2},{y} {x+w},{y+h/2} {x+w/2},{y+h} {x},{y+h/2}" fill="{fill}" stroke="{stroke}" stroke-width="1.6"/>')
  elif shape=='database':s += [f'<path d="M{x},{y+12} V{y+h-12} C{x},{y+h+4} {x+w},{y+h+4} {x+w},{y+h-12} V{y+12} Z" fill="{fill}" stroke="{stroke}" stroke-width="1.6"/>',f'<ellipse cx="{x+w/2}" cy="{y+12}" rx="{w/2}" ry="12" fill="{fill}" stroke="{stroke}" stroke-width="1.6"/>']
  elif shape=='cube':
   depth=17
   s += [f'<polygon points="{x},{y+depth} {x+depth},{y} {x+w},{y} {x+w-depth},{y+depth}" fill="{fill}" stroke="{stroke}"/>',f'<polygon points="{x+w-depth},{y+depth} {x+w},{y} {x+w},{y+h-depth} {x+w-depth},{y+h}" fill="{fill}" stroke="{stroke}" opacity="0.7"/>',f'<rect x="{x}" y="{y+depth}" width="{w-depth}" height="{h-depth}" fill="{fill}" stroke="{stroke}" stroke-width="1.6"/>']
  elif shape=='graph':
   s.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{fill}" stroke="{stroke}"/>')
   pts=[(x+45,y+35),(x+105,y+22),(x+165,y+44),(x+75,y+83),(x+145,y+87)]
   for a,b in [(0,1),(1,2),(0,3),(1,3),(1,4),(2,4),(3,4)]:s.append(f'<line x1="{pts[a][0]}" y1="{pts[a][1]}" x2="{pts[b][0]}" y2="{pts[b][1]}" stroke="{stroke}" stroke-width="1.5"/>')
   for px,py in pts:s.append(f'<circle cx="{px}" cy="{py}" r="8" fill="white" stroke="{stroke}" stroke-width="2"/>')
  else:s.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{fill}" stroke="{stroke}" stroke-width="1.6"/>')
  lines=n['label'].split('\n');cy=y+h/2 if shape!='graph' else y+h-24
  for j,line in enumerate(lines):s.append(f'<text x="{x+w/2}" y="{cy+(j-(len(lines)-1)/2)*20+5}" text-anchor="middle" font-size="{14 if len(line)>27 else 16}" font-weight="{600 if j==0 else 400}">{esc(line)}</text>')
 s += [f'<line x1="48" y1="{H-83}" x2="{W-48}" y2="{H-83}" stroke="#DCE2E9"/>',f'<text x="48" y="{H-53}" font-size="13" fill="#718095">Solid: forward / interaction flow     Dashed: auxiliary / training / skip path (see labels)</text>',f'<text x="48" y="{H-28}" font-size="12" fill="#8994A2">Original template. Source papers are topic references, not an exact algorithm specification.</text>','</g></svg>']
 return '\n'.join(s)
def render_drawio(spec):
 mx=ET.Element('mxfile',host='app.diagrams.net',version='26.0.0');d=ET.SubElement(mx,'diagram',name=spec['title'],id=spec['id']);model=ET.SubElement(d,'mxGraphModel',dx='1320',dy='800',grid='1',gridSize='10',guides='1',tooltips='1',connect='1',arrows='1',fold='1',page='1',pageScale='1',pageWidth=str(spec['width']),pageHeight=str(spec['height']),math='0',shadow='0');root=ET.SubElement(model,'root');ET.SubElement(root,'mxCell',id='0');ET.SubElement(root,'mxCell',id='1',parent='0')
 def cell(id,label,style,x,y,w,h,parent='1'):
  c=ET.SubElement(root,'mxCell',id=id,value=label,style=style,vertex='1',parent=parent);ET.SubElement(c,'mxGeometry',x=str(x),y=str(y),width=str(w),height=str(h),attrib={'as':'geometry'});return c
 cell('title',spec['id']+' / '+spec['title'],'text;html=1;align=left;verticalAlign=middle;whiteSpace=wrap;fontSize=26;fontStyle=1;fontColor=#243247;',48,25,1230,45)
 cell('subtitle','Generic editable structure - adapt modules and edges to your actual method.','text;html=1;align=left;fontSize=14;fontColor=#738093;',48,75,1200,25)
 for i,g in enumerate(spec['groups']):cell('g'+str(i),g['title'],'swimlane;html=1;startSize=35;rounded=1;container=1;pointerEvents=0;collapsible=0;fillColor=#FAFBFD;strokeColor=#CCD4DD;dashed=1;fontSize=15;fontColor=#68778A;',g['x'],g['y'],g['w'],g['h'])
 for n in spec['nodes']:
  parent='1';x,y=n['x'],n['y']
  for i,g in enumerate(spec['groups']):
   if x>=g['x'] and y>=g['y']+35 and x+n['w']<=g['x']+g['w'] and y+n['h']<=g['y']+g['h']:parent='g'+str(i);x-=g['x'];y-=g['y'];break
  fill,stroke=COLORS[n['kind']];shape={'box':'rounded=1;','ellipse':'ellipse;','diamond':'rhombus;','database':'shape=cylinder3;','graph':'rounded=1;','cube':'shape=cube;size=17;'}[n['shape']]
  label=n['label'].replace('\n','<br>')
  cell('n_'+n['id'],label,shape+f'whiteSpace=wrap;html=1;fillColor={fill};strokeColor={stroke};fontColor=#243247;fontFamily=Arial;fontSize=16;strokeWidth=1.6;spacing=8;',x,y,n['w'],n['h'],parent)
  if n['shape']=='graph':
   # Editable mini-graph primitives, grouped under a real container.
   graphcell=root.find(f"mxCell[@id='n_{n['id']}']");graphcell.set('value',n['label'].replace('\n',' / '));graphcell.set('style',graphcell.get('style')+'container=1;pointerEvents=0;verticalAlign=bottom;fontSize=12;spacingBottom=5;')
   pts=[(45,35),(105,22),(165,44),(75,83),(145,87)]
   for j,(px,py) in enumerate(pts):cell(f"mini_{n['id']}_{j}",'',f'ellipse;fillColor=#FFFFFF;strokeColor={stroke};html=1;',px-8,py-8,16,16,'n_'+n['id'])
   for j,(a,b) in enumerate([(0,1),(1,2),(0,3),(1,3),(1,4),(2,4),(3,4)]):
    ec=ET.SubElement(root,'mxCell',id=f"me_{n['id']}_{j}",style=f'endArrow=none;strokeColor={stroke};html=1;',edge='1',parent='n_'+n['id'],source=f"mini_{n['id']}_{a}",target=f"mini_{n['id']}_{b}");ET.SubElement(ec,'mxGeometry',relative='1',attrib={'as':'geometry'})
 for i,e in enumerate(spec['edges']):
  pts=paths(spec,e);ns={n['id']:n for n in spec['nodes']};a,b=ns[e['source']],ns[e['target']];start,end=pts[0],pts[-1]
  style=f'edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;endArrow=block;endFill=1;strokeColor=#647284;strokeWidth=1.7;fontSize=12;labelBackgroundColor=#FFFFFF;exitX={(start[0]-a["x"])/a["w"]};exitY={(start[1]-a["y"])/a["h"]};entryX={(end[0]-b["x"])/b["w"]};entryY={(end[1]-b["y"])/b["h"]};'
  if e['style']=='dashed':style+='dashed=1;'
  if e.get('straight'):style=style.replace('edgeStyle=orthogonalEdgeStyle;','edgeStyle=none;')
  c=ET.SubElement(root,'mxCell',id='e'+str(i),value=e['label'],style=style,edge='1',parent='1',source='n_'+e['source'],target='n_'+e['target']);geo=ET.SubElement(c,'mxGeometry',relative='1',attrib={'as':'geometry'})
  if len(pts)>2:
   arr=ET.SubElement(geo,'Array',attrib={'as':'points'})
   for x,y in pts[1:-1]:ET.SubElement(arr,'mxPoint',x=str(x),y=str(y))
 cell('legend','Solid: forward / interaction flow. Dashed: auxiliary / training / skip path; see arrow labels.','text;html=1;align=left;fontColor=#718095;fontSize=13;',48,spec['height']-64,1220,30)
 return ET.tostring(mx,encoding='unicode',xml_declaration=True)
def main():
 catalog=[]
 for sp in SPECS:
  for n in sp['nodes']:
   if n['shape'] not in ['ellipse','graph']:
    maxchars=max(18,int((n['w']-20)/7.3))
    n['label']='\n'.join(part for line in n['label'].split('\n') for part in textwrap.wrap(line,width=maxchars,break_long_words=False,break_on_hyphens=False))
  folder=ROOT/'templates'/sp['category'];folder.mkdir(parents=True,exist_ok=True);stem=sp['id']+'_'+sp['slug']
  (folder/(stem+'.drawio')).write_text(render_drawio(sp),encoding='utf8');(folder/(stem+'.svg')).write_text(render_svg(sp),encoding='utf8');(folder/(stem+'.json')).write_text(json.dumps(sp,ensure_ascii=False,indent=2),encoding='utf8')
  card={k:sp[k] for k in ['id','category','title','description','slug','tips']};card.update(drawio=(folder/(stem+'.drawio')).relative_to(ROOT).as_posix(),preview=(folder/(stem+'.svg')).relative_to(ROOT).as_posix(),spec=(folder/(stem+'.json')).relative_to(ROOT).as_posix(),editable_template=True,provenance='原创通用结构模板；主题相关论文提供布局参考，并非逐图复刻',preview_renderer='SVG generated from shared JSON geometry; not a draw.io native export')
  catalog.append(card)
 (ROOT/'metadata'/'templates.json').write_text(json.dumps(catalog,ensure_ascii=False,indent=2),encoding='utf8')
 print(json.dumps({'editable_templates':len(catalog),'categories':len(CATS)},ensure_ascii=False))
if __name__=='__main__':main()
