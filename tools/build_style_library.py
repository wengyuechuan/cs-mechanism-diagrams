"""Build the three-axis library and portable imagegen skill assets."""
import sys,json,hashlib,shutil,csv,html
from pathlib import Path
from collections import Counter
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools/vendor'))
import resvg_py
from style_taxonomy import taxonomy,TEMPLATE_STYLES
SKILL=ROOT/'agent-skill/cs-mechanism-imagegen'

TOPIC_NOTES={
'01':'视觉网络先确定尺度与跳连关系；层级编码解码适合 U-Net/FPN，总图与核心模块分开展示适合复杂分割方法。',
'02':'注意力图先写明 Q、K、V 的来源与操作；token/矩阵展开适合局部算子，模块总览适合 Transformer/Mamba 整体架构。',
'03':'GNN 先区分图中实体边与系统流程箭头；局部消息传递用节点关系图，完整网络用总览加邻域放大。',
'04':'生成模型明确前向/逆向方向、条件注入与采样次数；迭代布局适合扩散过程，分支布局适合条件与潜变量。',
'05':'检索类优先区分离线构建与在线查询；GraphRAG 可组合泳道 L08 与节点图 V05。参考模板中的向量索引不能自动搬到图谱方法。',
'06':'多模态要明确各模态输入、单独编码与融合位置；交互注意力的方向由用户方法定义，不能因为对称布局就画成双向。',
'07':'强化学习分别表达环境交互与参数学习；智能体工具循环只能画确实存在的反馈。具身场景使用图标辅助说明，不能取代模块定义。',
'08':'训练机制明确冻结与可训练分支、梯度路径、损失与数据流；教师学生、自监督通常适合平行分支或训练推理泳道。',
'09':'三维方法可用张量层叠 V03 表达特征、轻场景 V04 表达射线和几何；图示的视角/坐标关系不能随风格改动。',
'10':'系统图先确定职责边界、存储组件、读写方向与执行阶段；泳道和层级模块适合数据库、分布式训练和查询执行。',
'11':'因果与科学 AI 区分因果DAG、模型计算图与概念示意；只有用户提供的因果边才标因果，生物/物理机制图必须核对实体语义。',
'12':'通用框架根据数据流选择线性、模块放大或多面板；不要仅用统一方框装饰替代真正的方法结构。'}

def dump(p,x):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,ensure_ascii=False,indent=2),encoding='utf8')
def raster_svg(svg,png):
    png.write_bytes(resvg_py.svg_to_bytes(svg_path=str(svg),zoom=1.6,background='white',font_dirs=['C:/Windows/Fonts']))

def main():
    figures=json.loads((ROOT/'metadata/figures.json').read_text(encoding='utf8'))
    papers=json.loads((ROOT/'metadata/papers.json').read_text(encoding='utf8'))
    bypaper={p['id']:p for p in papers}
    templates=json.loads((ROOT/'metadata/templates.json').read_text(encoding='utf8'))
    tax=taxonomy();dump(ROOT/'metadata/style_taxonomy.json',tax);dump(SKILL/'references/style-taxonomy.json',tax)
    for t in templates:
        t['layout_style'],t['visual_style']=TEMPLATE_STYLES[t['id']]
        png=(ROOT/t['preview']).with_suffix('.png');raster_svg(ROOT/t['preview'],png)
        t['preview_png']=png.relative_to(ROOT).as_posix()
    dump(ROOT/'metadata/templates.json',templates)
    catalog=[]
    for f in figures:
        dump((ROOT/f['preview']).with_suffix('.json'),f)
        p=bypaper[f['paper_id']]
        x={k:f.get(k) for k in ['id','title','category','layout_style','visual_style','source_url','pdf_url','figure_number','pdf_page','caption','crop_note','style_review','batch']}
        x.update(topic=f['category'][:2],kind='paper_reference',year=f['year'],venue=f['venue'],image=f['preview'],description=f['diagram_type'],source_kind=p['source_kind'],copy_note=p.get('copy_note','公开论文版本'),rights='Original authors/publisher; check source license')
        catalog.append(x)
    for t in templates:
        x={k:t[k] for k in ['id','title','category','layout_style','visual_style','description']}
        x.update(topic=t['category'][:2],kind='original_blueprint',year=2026,venue='原创结构蓝图',image=t['preview_png'],rights='MIT; original generic structure, not an exact paper reproduction',source_url=None,keywords=' '.join(t.get('tips',[])))
        catalog.append(x)
    portable=[]
    expected_images=set()
    for x in catalog:
        path=Path('assets/images')/x['topic']/x['layout_style']/(x['id']+'.png')
        dest=SKILL/path;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(ROOT/x['image'],dest)
        expected_images.add(dest.resolve())
        x['image_sha256']=hashlib.sha256(dest.read_bytes()).hexdigest()
        portable.append({**x,'image':path.as_posix()})
    # Prune only generated PNG copies from this builder's dedicated asset tree.
    image_root=(SKILL/'assets/images').resolve()
    for stale in image_root.rglob('*.png'):
        resolved=stale.resolve()
        if not resolved.is_relative_to(image_root):raise ValueError('Unsafe generated asset path')
        if resolved not in expected_images:stale.unlink()
    expected_groups={(ROOT/'styles'/x['category']/x['layout_style']/'index.json').resolve() for x in catalog}
    style_root=(ROOT/'styles').resolve()
    for stale in style_root.rglob('index.json'):
        resolved=stale.resolve()
        if not resolved.is_relative_to(style_root):raise ValueError('Unsafe generated style path')
        if resolved not in expected_groups:stale.unlink()
    dump(ROOT/'metadata/style_catalog.json',catalog);dump(SKILL/'references/catalog.json',portable)
    counts={'source_papers':len(papers),'paper_references':len(figures),'original_blueprints':len(templates),'portable_png_images':len(portable),'topic_categories':12,'layout_styles':len(tax['layouts']),'visual_styles':len(tax['visuals']),'new_papers':sum(p.get('batch')=='v2-2025-expansion' for p in papers),'new_paper_references':sum(f.get('batch')=='v2-2025-expansion' for f in figures)}
    dump(ROOT/'metadata/style_summary.json',counts)
    with (ROOT/'metadata/style_index.csv').open('w',encoding='utf-8-sig',newline='') as o:
        keys=['id','kind','topic','category','layout_style','visual_style','title','venue','year','image','source_url','figure_number','pdf_page']
        w=csv.DictWriter(o,fieldnames=keys,extrasaction='ignore');w.writeheader();w.writerows(catalog)
    layout_by={x['id']:x for x in tax['layouts']};visual_by={x['id']:x for x in tax['visuals']}
    guide='# 风格分类：主题 × 布局 × 视觉表达\n\n'+tax['classification_note']+'\n\n'
    for kind,title in [('layouts','布局风格'),('visuals','视觉表达')]:
        guide+='## '+title+'\n\n'
        for x in tax[kind]:
            guide+=f"### {x['id']} {x['name']}\n\n{x['definition']}\n\n"
            if kind=='layouts':guide+=f"适合：{x['use_when']}\n\n不适合：{x['avoid_when']}\n\n"
            else:guide+=f"建议配色：{x['suggested_palette']}\n\n"
            guide+='Prompt 片段：\n\n```text\n'+x['prompt_clause']+'\n```\n\n'
    (SKILL/'references/style-taxonomy.md').write_text(guide,encoding='utf8');(ROOT/'风格分类指南.md').write_text(guide,encoding='utf8')
    topics='# 主题内选风格\n\n分类字段均可组合，不把论文会场作为绘图风格。下面的图 ID 可用 `library.py search` 检索。\n\n'
    for c in sorted(set(x['category'] for x in catalog)):
        subset=[x for x in catalog if x['category']==c];tid=c[:2]
        text=f"## {c}\n\n{TOPIC_NOTES[tid]}\n\n"
        text+='| 布局 | 图例数 | 代表 ID |\n|---|---:|---|\n'
        for lid in sorted(set(x['layout_style'] for x in subset)):
            chosen=[x for x in subset if x['layout_style']==lid]
            chosen.sort(key=lambda x:(x['kind']!='original_blueprint',-x['year'],x['id']))
            text+=f"| {lid} {layout_by[lid]['name']} | {len(chosen)} | "+', '.join(x['id'] for x in chosen[:3])+' |\n'
            groupdir=ROOT/'styles'/c/lid
            dump(groupdir/'index.json',chosen)
        text+='\n视觉表达：'+', '.join(f"{vid} {visual_by[vid]['name']}（{sum(x['visual_style']==vid for x in subset)}）" for vid in sorted(set(x['visual_style'] for x in subset)))+'。\n\n'
        topics+=text
        path=ROOT/'styles'/c;path.mkdir(parents=True,exist_ok=True);(path/'README.md').write_text(text+'[打开风格图库](../../风格图库.html)\n',encoding='utf8')
    (SKILL/'references/topics.md').write_text(topics,encoding='utf8')
    (ROOT/'主题内风格索引.md').write_text(topics,encoding='utf8')
    (ROOT/'风格图库.html').write_text(page(catalog,tax,counts,False),encoding='utf8')
    (SKILL/'gallery.html').write_text(page(portable,tax,counts,True),encoding='utf8')
    (SKILL/'LICENSE.txt').write_text('MIT License applies to the original skill text, scripts, taxonomy and original_blueprint images. Copyright (c) 2026. Permission to use, copy, modify and distribute these original materials with this notice; provided AS IS without warranty. Third-party paper_reference images are excluded and retain original authors/publisher rights. See references/rights.md and per-image source metadata.\n',encoding='utf8')
    example=ROOT/'examples/imagegen';target=SKILL/'assets/examples';target.mkdir(exist_ok=True)
    for suffix in ['.png','.brief.json','.final.prompt.txt','.review.json']:
        src=example/('graph-rag-v01'+suffix)
        if src.exists():shutil.copy2(src,target/src.name)
    dump(target/'graph-rag-v01.references.json',{'layout_style':'L08','visual_style':'V01','reference_images':[x for x in portable if x['id'] in ['T17','T18']],'tool':'built-in imagegen'})
    print(json.dumps(counts,ensure_ascii=False))

def page(catalog,tax,counts,portable):
    payload=json.dumps({'catalog':catalog,'taxonomy':tax,'counts':counts},ensure_ascii=False).replace('</',r'<\/')
    home='<a href="index.html">原模板库</a>' if not portable else '<a href="SKILL.md">Skill 入口</a>'
    return PAGE.replace('__DATA__',payload).replace('__HOME__',home)

PAGE=r'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>机制图风格图库 · 主题 × 布局 × 视觉</title><style>
*{box-sizing:border-box}body{margin:0;font:15px/1.65 system-ui,"Microsoft YaHei",sans-serif;color:#243247;background:#f3f5f8}header{background:#172d45;color:white;padding:32px 5%}h1{font-size:30px;margin:6px 0}header p{color:#bad0df;margin:7px 0}.counts{display:flex;gap:12px;flex-wrap:wrap}.counts b{font-size:24px}.counts span{background:#28425b;padding:7px 16px;border-radius:6px}main{max-width:1540px;padding:24px;margin:auto}.filters{padding:16px;background:white;border:1px solid #dce3eb;border-radius:9px;display:flex;gap:10px;flex-wrap:wrap;position:sticky;top:0;z-index:3}input,select,button,a.button{font:inherit;border:1px solid #ccd5e0;border-radius:6px;background:white;padding:8px 12px;color:#243247}input{flex:1;min-width:200px}a{color:#2457ad}header a{color:#d5e5f1}#summary{color:#627489;margin:17px 0}.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(290px,1fr));gap:16px}.card{background:white;border:1px solid #dce3eb;border-radius:9px;overflow:hidden}.thumb{height:210px;display:flex;align-items:center;justify-content:center;padding:9px;cursor:zoom-in}.thumb img{width:100%;height:100%;object-fit:contain}.body{padding:15px;border-top:1px solid #e5eaf0}.body h3{font-size:15px;line-height:1.45;margin:8px 0}.tags{display:flex;gap:5px;flex-wrap:wrap}.tag{background:#edf3f8;color:#3e6485;padding:3px 7px;font-size:12px;border-radius:4px}.meta{color:#627489;font-size:12px}.actions{display:flex;gap:9px;flex-wrap:wrap;margin-top:9px}.actions a,.actions button{font-size:12px}.pagination{text-align:center;margin:24px}.pagination button{margin:0 12px}dialog{border:1px solid #ccd5e0;border-radius:10px;width:min(1200px,96vw);max-height:95vh;overflow:auto;padding:24px}dialog::backdrop{background:#132c40bf}dialog img{width:100%;max-height:580px;object-fit:contain}textarea{width:100%;height:180px;font:13px/1.5 monospace;border:1px solid #ccd5e0;padding:12px}#close{float:right}footer{color:#627489;font-size:12px;margin:25px 0}@media(max-width:650px){.filters{position:static}h1{font-size:24px}}
</style></head><body><header><div>CS MECHANISM DIAGRAM / STYLE LIBRARY</div><h1>按主题选图，按风格绘制</h1><p>主题定义内容，布局定义阅读路径，视觉表达定义图元与质感。每个主题内都可继续筛选两种风格。</p><div class="counts" id="counts"></div><p>__HOME__ · 原图出处、裁剪说明和可用提示片段均在详情中。</p></header><main><div class="filters"><input id="q" aria-label="搜索图例" placeholder="搜索图 ID、方法名称或关键词"><select id="topic" aria-label="主题"></select><select id="layout" aria-label="布局风格"></select><select id="visual" aria-label="视觉风格"></select><select id="kind" aria-label="来源类型"><option value="">全部来源</option><option value="paper_reference">论文机制图</option><option value="original_blueprint">原创结构蓝图</option></select></div><p id="summary"></p><div class="grid" id="grid"></div><div class="pagination"><button id="prev">上一页</button><span id="page"></span><button id="next">下一页</button></div><footer>分类为人工缩略图表达方式整理；不是会议官方标准或算法正确性审核。原论文参考保留原作者及出版商权利，原创蓝图为通用结构。</footer></main><dialog id="detail"><button id="close">关闭</button><div id="detailbody"></div></dialog><script>
const DATA=__DATA__, $=id=>document.getElementById(id),esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));let page=0;const size=24,L=Object.fromEntries(DATA.taxonomy.layouts.map(x=>[x.id,x])),V=Object.fromEntries(DATA.taxonomy.visuals.map(x=>[x.id,x]));
$('counts').innerHTML=[[DATA.counts.portable_png_images,'实际 PNG'],[12,'主题'],[11,'布局风格'],[6,'视觉风格']].map(([n,s])=>`<span><b>${n}</b> ${s}</span>`).join('');
function opts(id,label,items){$(id).innerHTML=`<option value="">${label}</option>`+items.map(([k,v])=>`<option value="${esc(k)}">${esc(v)}</option>`).join('')}
opts('topic','全部主题',[...new Set(DATA.catalog.map(x=>x.category))].sort().map(x=>[x.slice(0,2),x.slice(3)]));opts('layout','全部布局风格',DATA.taxonomy.layouts.map(x=>[x.id,x.id+' '+x.name]));opts('visual','全部视觉风格',DATA.taxonomy.visuals.map(x=>[x.id,x.id+' '+x.name]));
function current(){const q=$('q').value.trim().toLowerCase();return DATA.catalog.filter(x=>(!$('topic').value||x.topic===$('topic').value)&&(!$('layout').value||x.layout_style===$('layout').value)&&(!$('visual').value||x.visual_style===$('visual').value)&&(!$('kind').value||x.kind===$('kind').value)&&(!q||[x.id,x.title,x.category,x.caption,x.description,x.venue].join(' ').toLowerCase().includes(q)))}
function tags(x){return `<span class="tag">${esc(L[x.layout_style].name)}</span><span class="tag">${esc(V[x.visual_style].name)}</span>`}
function render(){const rows=current(),total=Math.max(1,Math.ceil(rows.length/size));page=Math.min(page,total-1);$('summary').textContent=`当前 ${rows.length} 张 · 可组合主题、布局、视觉与来源类型筛选。`;$('page').textContent=`${page+1} / ${total}`;$('prev').disabled=page===0;$('next').disabled=page===total-1;$('grid').innerHTML=rows.slice(page*size,(page+1)*size).map(x=>`<article class="card"><div class="thumb" data-id="${esc(x.id)}"><img src="${encodeURI(x.image)}" alt="${esc(x.id+' '+x.title)}" loading="lazy"></div><div class="body"><div class="meta">${esc(x.id)} · ${esc(x.category.slice(3))}</div><h3>${esc(x.title)}</h3><div class="tags">${tags(x)}</div><div class="meta">${x.kind==='original_blueprint'?'原创通用结构 · MIT':esc(x.venue+' '+x.year+' · Figure '+x.figure_number+' · PDF 第 '+x.pdf_page+' 页')}</div><div class="actions"><button data-id="${esc(x.id)}">风格详情</button><a href="${encodeURI(x.image)}" download>PNG</a></div></div></article>`).join('')||'<p>没有匹配项，请放宽一个风格条件。</p>';$('grid').querySelectorAll('[data-id]').forEach(el=>el.onclick=()=>detail(el.dataset.id))}
function detail(id){const x=DATA.catalog.find(x=>x.id===id),l=L[x.layout_style],v=V[x.visual_style];if(!x)return;const prompt='Layout: '+l.prompt_clause+'\nStyle/medium: '+v.prompt_clause+'\nSuggested palette: '+v.suggested_palette+'\nReference role: visual grammar only; replace all algorithm modules and edges with your own verified method.';$('detailbody').innerHTML=`<h2>${esc(x.id+' · '+x.title)}</h2><div class="tags">${tags(x)}</div><img src="${encodeURI(x.image)}" alt="${esc(x.id)}"><p>${esc(l.definition)}<br>${esc(v.definition)}</p><p>适合：${esc(l.use_when)}<br>避免：${esc(l.avoid_when)}</p><p class="meta">${x.kind==='original_blueprint'?esc(x.rights):esc(x.venue+' '+x.year+' · 图 '+x.figure_number+' · PDF 第 '+x.pdf_page+' 页 · '+x.copy_note)}</p>${x.source_url?`<a href="${esc(x.source_url)}" target="_blank" rel="noopener">正式论文出处</a>`:''}<p>${esc(x.crop_note||x.description)}</p><h3>可组合的提示片段</h3><textarea readonly aria-label="风格提示片段">${esc(prompt)}</textarea><p>这是风格片段；完整提示词还应包含真实节点、箭头、分组和精确文字。</p><p class="meta">${esc(x.caption||'原创结构蓝图；不是论文算法的精确复刻。')}</p>`;if(!$('detail').open)$('detail').showModal()}
['q','topic','layout','visual','kind'].forEach(id=>$(id).oninput=()=>{page=0;render()});$('prev').onclick=()=>{page--;render()};$('next').onclick=()=>{page++;render()};$('close').onclick=()=>$('detail').close();$('detail').onclick=e=>{if(e.target===$('detail'))$('detail').close()};render();
</script></body></html>'''

if __name__=='__main__':main()
