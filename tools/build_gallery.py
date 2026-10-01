import json,html,csv,zlib,base64
from pathlib import Path
from urllib.parse import quote
from collections import Counter
ROOT=Path(__file__).resolve().parents[1]
def load(n):return json.loads((ROOT/'metadata'/n).read_text(encoding='utf8'))
def save(p,data):p.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf8')
def main():
 figures=load('figures.json');papers=load('papers.json');templates=load('templates.json')
 for t in templates:
  related=[f for f in figures if f['category']==t['category']]
  related.sort(key=lambda f:(f.get('layout_style')!=t.get('layout_style'),f.get('visual_style')!=t.get('visual_style'),-f['year']))
  t['related_figures']=[f['id'] for f in related[:6]]
  xml=(ROOT/t['drawio']).read_text(encoding='utf8');compress=zlib.compress(quote(xml,safe='').encode())[2:-4]
  t['edit_url']='https://app.diagrams.net/#R'+base64.b64encode(compress).decode()
 save(ROOT/'metadata'/'templates.json',templates)
 with (ROOT/'metadata'/'figure_index.csv').open('w',encoding='utf-8-sig',newline='') as o:
  keys=['id','paper_id','title','venue','year','category','layout_style','visual_style','diagram_type','figure_number','pdf_page','review_status','preview','vector_reference','source_url']
  writer=csv.DictWriter(o,fieldnames=keys,extrasaction='ignore');writer.writeheader();writer.writerows(figures)
 ok=[p for p in papers if p.get('download_status')=='ok'];stats={'collected_date':'2026-10-01','source_papers':len(ok),'papers_with_mechanism_examples':len(set(f['paper_id'] for f in figures)),'mechanism_examples':len(figures),'editable_templates':len(templates),'categories':len(set(t['category'] for t in templates)),'venues':dict(Counter(p['venue'] for p in ok)),'figure_categories':dict(Counter(f['category'] for f in figures)),'pending_downloads':sum(p.get('download_status')!='ok' for p in papers)}
 save(ROOT/'metadata'/'summary.json',stats)
 payload=json.dumps({'figures':figures,'papers':ok,'templates':templates,'stats':stats},ensure_ascii=False).replace('</',r'<\/')
 html_text=PAGE.replace('__PAYLOAD__',payload)
 (ROOT/'index.html').write_text(html_text,encoding='utf8')
 readme=f'''# 计算机论文机制图与网络图模板库

收集日期：2026-10-01。范围：机制图、模型架构图、节点关系图、流程图、训练策略图。统计图不在模板范围内。

## 直接开始

双击 **index.html**，无需联网即可浏览本地图片与分类。首页默认显示可编辑模板；可切换到论文原图和论文清单。

双击 **[风格图库.html](风格图库.html)** 按“主题 × 布局 × 视觉表达”筛选实际 PNG；同一主题内均有多种风格。风格分类、主题内索引与可携带 imagegen skill 见下方。

- **{stats['source_papers']} 篇原论文 PDF**，其中 {stats['papers_with_mechanism_examples']} 篇提供了入库机制图。
- **{stats['mechanism_examples']} 张入库机制图参考**：PNG 预览、从 PDF 裁出的 SVG、原 PDF 页码、原图号和出处。
- **{stats['editable_templates']} 份原创可编辑 draw.io 模板**：配套 SVG 预览、JSON 几何定义与中文使用建议。
- **{stats['categories']} 个主题分类**，覆盖经典方法与 2024–2025 年样例。v2 新增 ICCV / ICML / ACL 2025 的 52 篇论文，筛出 61 张新机制图。

## AI 绘图 skill 与风格分类

- [风格图库](风格图库.html)：223 张论文机制参考 + 48 张原创结构蓝图，共 271 张 PNG。
- [风格分类指南](风格分类指南.md)：11 类布局、6 类视觉表达，可组合使用，不是会议官方风格标准。
- [主题内风格索引](主题内风格索引.md)：12 个主题下的子风格、图数和代表 ID。
- [Skill 入口](agent-skill/cs-mechanism-imagegen/SKILL.md)：选图、方法 brief、提示词脚本、内置 imagegen 调用与成图验收。
- [AI 成图示例](examples/imagegen/graph-rag-v01.png)：实际内置 imagegen 生成；同目录保留 brief、最终 prompt、参考清单与检查记录。

skill 完整副本在 `agent-skill/cs-mechanism-imagegen/`；个人技能目录安装副本为 `~/.codex/skills/cs-mechanism-imagegen/`。调用示例：`使用 $cs-mechanism-imagegen 选择合适风格，并用 imagegen 绘制我的方法图。`

图库按主题与主布局分组；实际 skill PNG 放在 `assets/images/<主题编号>/<布局ID>/`，视觉表达记录在索引中。搜索脚本不依赖 Python 第三方包、网络或原工作区路径。完整原 PDF 保留在本资料库，skill 包只携带图例和必要元数据。

## 怎样编辑

1. 在首页选中模板，查看大图与修改建议。
2. 点击“在线编辑”在 diagrams.net 中打开；或下载 `.drawio` 后使用 draw.io 桌面版。
3. 更改模块、张量维度、层数、分支和箭头。模板是通用结构，不保证等同于某篇论文的精确算法。
4. 在编辑器导出 SVG / PDF 后插入论文。SVG 预览是由同一份 JSON 生成，并非 draw.io 桌面端导出。

## 分类

'''+'\n'.join('- '+c for c in sorted(set(t['category'] for t in templates)))+'''

## 目录

- `templates/`：按类别保存的 `.drawio`、`.svg` 和 `.json`。
- `references/`：按主题、论文编号保存原 PDF、来源元数据及机制图。
- `metadata/figure_index.csv`：可用 Excel 打开的图例清单。
- `metadata/papers.json`：每篇论文的来源、实际下载地址、版本备注、SHA-256 和页数。
- `方法图绘制指南.md`：布局模式与绘图使用建议。
- `qa/`：缩略图审阅记录与校验报告。
- `tools/`：收集、模板生成、索引生成和校验脚本。

## 来源与范围

这是一套代表性资料库，不是所有顶会顶刊论文的穷尽集合。采用官方论文集、出版商公开页和作者公开版本；没有使用付费内容绕过方式。部分 ICLR、TPAMI、IJCV 来源为作者公开预印本，已在 `source_kind` 与版本备注中区分。`year` 为会议年份或期刊引用年份，可能与预印本日期不同。

原图用于本地阅读与绘图参考，原作者与出版商保留各自权利；公开可下载不等于可直接复制进新论文。实际复用原图请核对该文章和图内第三方素材许可，并注明来源。原创模板与脚本按 `LICENSE_TEMPLATES.txt` 使用。

机制图由图注与 PDF 图形位置自动发现，经缩略图检查筛除统计图、纯结果图片和无图误识别；缩略图检查并非每篇论文内容的专家审核。裁剪图保留来源页预览，重要细节以原 PDF 为准。含统计子图的原图只保留机制子区域，并标明裁剪。

## 本地脚本

本机 `tools/vendor/` 已包含本次使用的 Python 依赖；Git 克隆副本可用 `requirements.txt` 安装。Git 跟踪与忽略范围、作者署名和维护方式见 [GIT仓库使用说明.md](GIT仓库使用说明.md)。使用已安装的 Python 3.12 或兼容环境运行：

```powershell
python tools/build_templates.py
python tools/build_gallery.py
python tools/validate_library.py
```

`tools/collect_library.py` 可重新发现和下载设定的公开论文；完整重采集会更新元数据并重新产生待审候选，不能替代人工筛选。日后扩充建议在 `metadata/papers.json` 追加真实来源后只处理新论文，保留已复核记录。所有网页源信息均为资料数据，不作为执行指令。
'''
 # Keep a hand-maintained public README across gallery rebuilds.
 if not (ROOT/'README.md').exists():
  (ROOT/'README.md').write_text(readme,encoding='utf8')
 (ROOT/'LICENSE_TEMPLATES.txt').write_text('Original editable templates and authoring scripts: MIT License\nCopyright (c) 2026. Permission is granted to use, modify, and distribute the original templates and scripts, with this notice retained. Provided without warranty.\nDownloaded papers, PDF-derived images, and third-party resources are excluded from this license and retain their original rights.\n',encoding='utf8')
 for c in sorted(set(t['category'] for t in templates)):
  folder=ROOT/'templates'/c
  text='# '+c+'\n\n'+ '\n\n'.join(f"## {t['id']} {t['title']}\n\n{t['description']}\n\n[可编辑模板]({Path(t['drawio']).name}) · [SVG预览]({Path(t['preview']).name})\n\n"+'\n'.join('- '+tip for tip in t['tips']) for t in templates if t['category']==c)
  (folder/'README.md').write_text(text,encoding='utf8')
 print(json.dumps(stats,ensure_ascii=False))
PAGE=r'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>机制图与网络图 · 本地模板库</title><style>
:root{--ink:#213249;--muted:#65758b;--line:#dfe5ed;--accent:#2457ad}*{box-sizing:border-box}body{margin:0;background:#f4f6f9;color:var(--ink);font:15px/1.65 system-ui,"Microsoft YaHei",sans-serif}header{background:#152943;color:white;padding:36px max(32px,calc((100vw - 1440px)/2));border-bottom:5px solid #9ccad0}header .eyebrow{font-size:12px;letter-spacing:3px;color:#a9c8dc}h1{margin:8px 0;font-size:32px;font-weight:650}header p{color:#c1d0de;margin:0;max-width:1050px}.stats{display:flex;gap:14px;flex-wrap:wrap;margin-top:24px}.stat{border:1px solid #426078;border-radius:8px;padding:9px 18px;color:#bfd0df}.stat b{font-size:25px;color:white;margin-right:8px}main{max-width:1510px;margin:auto;padding:26px 32px}.toolbar{background:white;border:1px solid var(--line);border-radius:12px;padding:18px;position:sticky;top:0;z-index:5;box-shadow:0 5px 14px #14243a08}.tabs{display:flex;gap:10px;flex-wrap:wrap;margin-bottom:14px}button,.button{font:inherit;cursor:pointer;border:1px solid #ccd6e2;color:var(--ink);background:white;padding:7px 14px;border-radius:7px;text-decoration:none}.tabs button.active{background:#2457ad;color:white;border-color:#2457ad}.filters{display:flex;gap:10px;flex-wrap:wrap}input,select{font:inherit;padding:9px 12px;border:1px solid #ccd6e2;border-radius:7px;color:var(--ink);background:white}input{flex:1;min-width:230px}select{max-width:300px}.summary{margin:20px 2px;color:var(--muted)}.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:20px}.card{background:white;border:1px solid var(--line);border-radius:10px;overflow:hidden;box-shadow:0 3px 10px #15294306}.thumb{height:220px;background:#fff;border-bottom:1px solid var(--line);cursor:zoom-in;display:flex;align-items:center;justify-content:center;padding:8px}.thumb img{height:100%;width:100%;object-fit:contain}.cardbody{padding:17px}.meta{font-size:12px;color:#587088;margin-bottom:7px}.card h3{font-size:16px;line-height:1.5;margin:0 0 9px}.desc{color:var(--muted);font-size:13px}.actions{display:flex;gap:7px;flex-wrap:wrap;margin-top:13px}.actions a,.actions button{font-size:12px;padding:5px 9px}.badge{display:inline-block;font-size:11px;background:#edf4fa;padding:2px 7px;border-radius:4px;color:#386789}.paper{padding:22px}.paper p{font-size:13px}.empty{padding:60px;text-align:center;color:var(--muted);background:white;border-radius:10px}.pagination{display:flex;justify-content:center;align-items:center;gap:18px;margin:28px}footer{color:var(--muted);font-size:12px;margin-top:28px}dialog{width:min(1250px,95vw);max-height:94vh;border:1px solid #ccd6e2;border-radius:12px;padding:22px;overflow:auto}dialog::backdrop{background:#172534ba}dialog .close{float:right}dialog img{width:100%;max-height:650px;object-fit:contain;background:white}dialog h2{font-size:20px;padding-right:75px}dialog .caption{font-size:13px;white-space:pre-wrap;background:#f4f6f9;padding:16px;border-radius:8px}dialog a{color:#2457ad}.related{display:flex;gap:10px;flex-wrap:wrap}.related img{width:160px;height:115px;object-fit:contain;border:1px solid var(--line);cursor:pointer}.notice{background:#eaf0f7;color:#516981;border-radius:6px;padding:10px 13px;font-size:12px;margin-top:13px}@media(max-width:700px){header{padding:25px}main{padding:18px}h1{font-size:26px}.toolbar{position:static}.grid{grid-template-columns:1fr}}
</style></head><body><header><div class="eyebrow">COMPUTER SCIENCE / MECHANISM & ARCHITECTURE</div><h1>机制图、网络图与流程图模板库</h1><p>从公开论文中收集结构与表达方式。选择一个模板，查看同类论文原图，再把模块和连接换成自己的方法。</p><div class="stats" id="stats"></div></header><main><div class="toolbar"><div class="tabs"><button data-mode="templates" class="active">可编辑模板</button><button data-mode="figures">论文机制图</button><button data-mode="papers">原论文 PDF</button><a class="button" href="风格图库.html">按风格选图</a><a class="button" href="agent-skill/cs-mechanism-imagegen/SKILL.md">AI 绘图 Skill</a><a class="button" href="README.md">使用说明</a><a class="button" href="方法图绘制指南.md">绘制指南</a><a class="button" href="metadata/figure_index.csv" download>下载图例清单</a></div><div class="filters"><input id="query" placeholder="搜索：Transformer、消息传递、检索、智能体、作者方法…" aria-label="搜索"><select id="category" aria-label="主题分类"></select><select id="venue" aria-label="会议期刊"></select><select id="type" aria-label="图型"></select></div></div><div class="summary" id="summary"></div><div class="grid" id="grid"></div><div class="pagination"><button id="prev">上一页</button><span id="page"></span><button id="next">下一页</button></div><footer>收集日期 2026-10-01 · 原图保留作者及出版商权利；原创模板可编辑使用。部分来源是已注明的作者版本。<br>这是代表性集合；统计图、纯结果展示与误识别候选已从图例索引排除。PDF 保留完整论文内容。</footer></main><dialog id="detail"><button class="close" id="close">关闭</button><div id="detailbody"></div></dialog><script>
const DATA=__PAYLOAD__;let mode='templates',page=0;const size=24;const $=id=>document.getElementById(id);const escape=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));const url=p=>encodeURI(p);const shortcat=c=>c?.replace(/^\d+_/,'')||'';
$('stats').innerHTML=[['原论文',DATA.stats.source_papers],['机制图例',DATA.stats.mechanism_examples],['可编辑模板',DATA.stats.editable_templates],['主题分类',DATA.stats.categories]].map(([label,n])=>`<div class="stat"><b>${n}</b>${label}</div>`).join('');
function options(id,label,arr){$(id).innerHTML=`<option value="">${label}</option>`+[...new Set(arr.filter(Boolean))].sort().map(x=>`<option value="${escape(x)}">${escape(id==='category'?shortcat(x):x)}</option>`).join('')}
options('category','全部主题',[...DATA.templates,...DATA.figures].map(x=>x.category));options('venue','全部会议 / 期刊',DATA.papers.map(x=>x.venue));options('type','全部图型',DATA.figures.map(x=>x.diagram_type));
function current(){const q=$('query').value.trim().toLowerCase(),cat=$('category').value,venue=$('venue').value,type=$('type').value;return DATA[mode].filter(x=>(!cat||x.category===cat)&&(!venue||mode==='templates'||x.venue===venue)&&(!type||mode!=='figures'||x.diagram_type===type)&&(!q||[x.id,x.title,x.description,x.caption,x.category,x.diagram_type,x.venue,x.year].filter(Boolean).join(' ').toLowerCase().includes(q)))}
function actions(x){if(mode==='templates')return `<a class="button" href="${url(x.drawio)}" download>下载 .drawio</a><a class="button" href="${x.edit_url}" target="_blank" rel="noopener">在线编辑</a>`;if(mode==='figures')return `<a class="button" href="${url(x.local_pdf)}#page=${x.pdf_page}" target="_blank">原 PDF 第 ${x.pdf_page} 页</a><a class="button" href="${url(x.vector_reference)}" download>参考 SVG</a>`;return `<a class="button" href="${url(x.local_pdf)}" target="_blank">打开 PDF</a><a class="button" href="${x.source_url}" target="_blank" rel="noopener">来源页</a>`}
function render(){const all=current(),total=Math.max(1,Math.ceil(all.length/size));page=Math.min(page,total-1);$('summary').textContent=`当前 ${all.length} 项 · ${mode==='templates'?'原创通用结构，可编辑模块、箭头和文字。参考图按主题关联，并非论文算法的精确复刻。':mode==='figures'?'论文机制图参考，含原图号、页码与裁剪说明。点击图片放大。':'官方或作者公开版本；完整论文可能含实验结果图。'}`;$('page').textContent=`${page+1} / ${total}`;$('prev').disabled=page===0;$('next').disabled=page===total-1;
 $('grid').innerHTML=all.slice(page*size,(page+1)*size).map(x=>mode==='papers'?`<article class="card paper"><div class="meta">${escape(x.id)} · ${escape(x.venue)} ${x.year}</div><h3>${escape(x.title)}</h3><p>${escape(shortcat(x.category))} · ${x.pages} 页</p><span class="badge">${x.source_kind.includes('preprint')?'作者公开预印本':'公开来源 PDF'}</span><div class="actions">${actions(x)}</div></article>`:`<article class="card"><div class="thumb" data-id="${escape(x.id)}"><img src="${url(x.preview)}" alt="${escape(x.title)}" loading="lazy"></div><div class="cardbody"><div class="meta">${escape(x.id)} · ${escape(shortcat(x.category))}</div><h3>${escape(x.title)}</h3><div class="desc">${escape(mode==='templates'?x.description:`${x.venue} ${x.year} · ${x.diagram_type} · Figure ${x.figure_number} · PDF 第 ${x.pdf_page} 页`)}</div><div class="actions">${actions(x)}<button data-id="${escape(x.id)}">详情</button></div></div></article>`).join('')||'<div class="empty">没有匹配项目，请减少筛选条件。</div>';$('grid').querySelectorAll('[data-id]').forEach(el=>el.onclick=()=>detail(el.dataset.id));}
function detail(id){const x=[...DATA.templates,...DATA.figures].find(x=>x.id===id);if(!x)return;const isTemplate=x.editable_template,related=isTemplate?DATA.figures.filter(f=>x.related_figures.includes(f.id)):DATA.templates.filter(t=>t.category===x.category).slice(0,4);$('detailbody').innerHTML=`<h2>${escape(x.id)} · ${escape(x.title)}</h2><p>${escape(shortcat(x.category))}${isTemplate?'':` · ${escape(x.venue)} ${x.year} · Figure ${x.figure_number} · PDF 第 ${x.pdf_page} 页`}</p><img src="${url(x.preview)}" alt="${escape(x.title)}"><div class="actions">${isTemplate?`<a class="button" href="${url(x.drawio)}" download>下载可编辑 draw.io</a><a class="button" href="${x.edit_url}" target="_blank" rel="noopener">在 diagrams.net 编辑</a><a class="button" href="${url(x.preview)}" download>下载 SVG 预览</a>`:`<a class="button" href="${url(x.local_pdf)}#page=${x.pdf_page}" target="_blank">查看原 PDF</a><a class="button" href="${url(x.page_preview)}" target="_blank">完整来源页预览</a><a class="button" href="${url(x.vector_reference)}" download>下载参考 SVG</a><a class="button" href="${x.source_url}" target="_blank" rel="noopener">论文出处</a>`}</div>${isTemplate?`<p>${escape(x.description)}</p><ul>${x.tips.map(t=>`<li>${escape(t)}</li>`).join('')}</ul><div class="notice">${escape(x.provenance)}。SVG 由共享几何定义生成；具体算法语义请按你的论文修订。</div>`:`<p class="caption">${escape(x.caption)}</p><p>${escape(x.review_status)}${x.crop_note?' · '+escape(x.crop_note):''}</p>`}<h3>${isTemplate?'同主题论文原图':'同主题可编辑模板'}</h3><div class="related">${related.map(r=>`<img src="${url(r.preview)}" alt="${escape(r.id)}" title="${escape(r.id+' '+r.title)}" data-related="${escape(r.id)}">`).join('')||'暂无同主题图例'}</div>`;$('detailbody').querySelectorAll('[data-related]').forEach(el=>el.onclick=()=>detail(el.dataset.related));if(!$('detail').open)$('detail').showModal();}
$('close').onclick=()=>$('detail').close();$('detail').onclick=e=>{if(e.target===$('detail'))$('detail').close()};document.querySelectorAll('[data-mode]').forEach(b=>b.onclick=()=>{mode=b.dataset.mode;page=0;document.querySelectorAll('[data-mode]').forEach(v=>v.classList.toggle('active',v===b));$('venue').disabled=mode==='templates';$('type').disabled=mode!=='figures';render()});['query','category','venue','type'].forEach(id=>$(id).oninput=()=>{page=0;render()});$('prev').onclick=()=>{page--;render()};$('next').onclick=()=>{page++;render()};$('venue').disabled=true;$('type').disabled=true;render();
</script></body></html>'''
if __name__=='__main__':main()
