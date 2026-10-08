"""Create a relocatable skill ZIP and the local delivery guide."""
import json,zipfile
from pathlib import Path
from collections import Counter
ROOT=Path(__file__).resolve().parents[1]
SKILL=ROOT/'agent-skill/cs-mechanism-imagegen'

def main():
    counts=json.loads((ROOT/'metadata/style_summary.json').read_text(encoding='utf8'))
    cat=json.loads((SKILL/'references/catalog.json').read_text(encoding='utf8'))
    zip_path=ROOT/f'cs-mechanism-imagegen_{len(cat)}图.zip'
    with zipfile.ZipFile(zip_path,'w',compression=zipfile.ZIP_DEFLATED) as z:
        for p in sorted(SKILL.rglob('*')):
            if p.is_file() and '__pycache__' not in p.parts and p.suffix!='.pyc':
                z.write(p,Path(SKILL.name)/p.relative_to(SKILL))
    with zipfile.ZipFile(zip_path) as z:
        assert z.testzip() is None
        image_count=sum(n.startswith((SKILL.name+'/assets/images/',SKILL.name+'/assets/imported/')) and n.lower().endswith(('.png','.jpg','.jpeg')) for n in z.namelist())
        assert image_count==len(cat)
    table='| 主题 | 本库论文图 | 上游参考 | 原创蓝图 | 合计 |\n|---|---:|---:|---:|---:|\n'
    for topic in sorted(set(x['category'] for x in cat)):
        subset=[x for x in cat if x['category']==topic];a=sum(x['kind']=='paper_reference' for x in subset)
        u=sum(x['kind']=='upstream_reference' for x in subset);b=sum(x['kind']=='original_blueprint' for x in subset)
        table+=f'| {topic} | {a} | {u} | {b} | {len(subset)} |\n'
    text='''# 扩充图库与 AI 绘图 skill：交付说明

本次已新增 52 篇正式会议公开论文：ICCV 2025 24 篇、ICML 2025 16 篇、ACL 2025 12 篇；从 83 张候选图中筛选保留 61 张机制参考。旧库排除 2 张数据/统计混合参考，最终为 **223 张论文机制图 + 48 张原创结构蓝图 = 271 张真实、哈希各不相同的 PNG**。另保留 184 篇原 PDF，不用 PDF 页数或索引条数充当图片数量。

## 从这里开始

- [离线风格图库](风格图库.html)：双击打开即可，无需服务器或联网；可组合主题、布局、视觉风格、来源类型与关键词。
- [主题内风格索引](主题内风格索引.md)：每个主题内的风格数量与代表图 ID。
- [风格分类指南](风格分类指南.md)：11 类布局、6 类视觉表达、适用场景、避免事项与提示片段。
- [Skill 入口](agent-skill/cs-mechanism-imagegen/SKILL.md)：agent 的完整操作流程。
- [可迁移 Skill 压缩包](cs-mechanism-imagegen_271图.zip)：完整 skill、271 张 PNG、相对路径索引及真实生成例子，不包含 184 篇完整 PDF。
- [原可编辑模板](可编辑机制图模板_48套.zip)：48 套 drawio、SVG、PNG 和结构 JSON。

## 分类方式

每张图都记录一个主题、一个主要布局和一个主要视觉表达。主题按来源论文主要方法归类，跨领域方法也可用标题与图注关键词搜索；布局描述信息结构，视觉表达描述图元与质感。二者可独立组合，例如检索方法采用“分阶段泳道 + 扁平柔和色块”，同一主题的另一张图采用“节点关系 + 彩色节点”。不是全部主题都有全部 66 种风格组合，零结果会如实显示。

布局包括线性流水线、多分支汇合、层级编码解码、模块总览与局部放大、节点消息传递、token 矩阵算子、迭代反馈、阶段泳道、多面板机制对照、概念场景、树状层级。视觉表达包括柔和色块、单色细线、张量轻透视、图标场景混合、彩色节点、高对比模块。

这些是本库的人工表达方式标签，配色是绘制建议；不是会议或期刊官方风格规范。源图经过缩略图类型与风格复核，未做每篇算法的专家审查。原 PDF、来源网址、图号、PDF 页码和裁剪记录便于进一步核对。旧下载目录名称保留历史位置，当前分类以 style_catalog 和风格图库为准。

'''+table+'''
## Agent 如何使用

把完整 skill 目录复制到个人技能目录，例如 `~/.codex/skills/cs-mechanism-imagegen/`。新任务中可直接输入：

```text
使用 $cs-mechanism-imagegen 和 $imagegen，先在图库中选择适合的机制图风格，再绘制我的方法。
主题：图神经网络；布局：节点消息传递；视觉：彩色节点。
我的模块、节点、边、分组与准确标签如下：……
```

Agent 的流程是检索真实 PNG → 看图 → 写方法 brief → 校验节点/边/分组 → 组合提示词 → 调用内置 imagegen → 查看成图核对 → 保存成图、brief、实际 prompt、参考与审核记录。不能因参考图有某个模块就添加到新方法，也不能把位图改扩展名声称是可编辑矢量图。检索/提示词脚本仅需 Python 标准库，不依赖网络或第三方包；生成使用运行环境已有的 imagegen 工具。

在 skill 目录下也可手工检索：

```powershell
python scripts/library.py list
python scripts/library.py search --topic retrieval --layout L08 --visual V01 --limit 4
python scripts/library.py prompt --brief assets/briefs/graph-rag.json --refs T17,T18 --layout L08 --visual V01 --out output/graph-rag
python scripts/library.py verify
```

## 已完成的实际验证

- 文件完整性：184 篇 PDF 的 SHA-256/页数、223 张机制 PNG 解码、SVG/XML 解析、48 套可编辑模板节点/边/几何检查通过。
- 可迁移图库：271 张 PNG 路径、哈希、主题和风格 ID 通过检查；271 个图片哈希各不相同。
- 7 项脚本测试通过，包含重复/缺失端点、分组、禁止边、严格筛选与拓扑提示词。
- 独立 agent 实际检索并生成提示词，测试了零结果与禁止 Answer → Graph index 回写的拒绝行为；其离线测试未调用 imagegen。
- 主 agent 另外真实调用了内置 imagegen，得到 [GraphRAG 成图](examples/imagegen/graph-rag-v01.png)。人工核对 9 个节点、8 条单向系统箭头、两阶段分组和标签通过；[实际最终提示词](examples/imagegen/graph-rag-v01.final.prompt.txt) 与 [核对记录](examples/imagegen/graph-rag-v01.review.json) 一并保存。该例未验证特定期刊的投稿版面/分辨率。
- 浏览器实测主题内的布局与视觉组合、详情提示片段、空结果提示；[实际界面截图](qa/风格图库预览.png) 可查看。

原论文图保留原作者与出版商权利，skill 中明确区分论文参考和原创蓝图；原创 skill 文本、脚本、分类体系和蓝图提供 MIT 许可。
'''
    text=text.replace('cs-mechanism-imagegen_271图.zip',zip_path.name).replace('完整 skill、271 张 PNG','完整 skill、'+str(len(cat))+' 张 PNG/JPEG').replace('检索真实 PNG','检索真实 PNG/JPEG')
    text=text.replace('# 扩充图库与 AI 绘图 skill：交付说明','# 扩充图库与 AI 绘图 skill：交付说明\n\n2026-10-08：新增 '+str(counts.get('upstream_references',0))+' 张 Top-Conf 参考，图库共 '+str(len(cat))+' 张。下述 271 张为原始精选库，导入批次见 [外部图库整合说明](外部图库整合说明.md)。')
    (ROOT/'扩充与Skill使用说明.md').write_text(text,encoding='utf8')
    report={**counts,'distinct_image_hashes':len(set(x['image_sha256'] for x in cat)),
            'zip_image_count':image_count,'zip_megabytes':round(zip_path.stat().st_size/1048576,2),
            'zip_integrity':'pass','imagegen_real_example':'examples/imagegen/graph-rag-v01.png',
            'imagegen_upstream_example':'examples/imagegen/topconf-graph-rag-v02.png',
            'upstream_import_report':'metadata/topconf_import_report.json',
            'browser_checks':['combined topic/layout/visual','reference detail','empty result'],
            'manual_review_scope':'thumbnail diagram type/style; example nodes, edges, labels; not full-paper algorithm review'}
    (ROOT/'qa/style_delivery_report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
    print(json.dumps(report,ensure_ascii=False))

if __name__=='__main__':main()
