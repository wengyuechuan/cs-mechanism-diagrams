"""Download public proceedings, identify mechanism figures, retain provenance.
Usage: python tools/collect_library.py [--extract-only]
No statistical figure is intentionally selected. Automatic selections remain labelled.
"""
import sys, re, json, csv, time, hashlib, concurrent.futures, argparse
from pathlib import Path
from urllib.parse import urljoin
sys.path.insert(0,str(Path(__file__).parent/'vendor'))
import requests, fitz
from bs4 import BeautifulSoup
ROOT=Path(__file__).resolve().parents[1]
CACHE=ROOT/'tools'/'cache'; CACHE.mkdir(exist_ok=True)
META=ROOT/'metadata'; META.mkdir(exist_ok=True)
FAIL=[]
def save_json(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2),encoding='utf8')
def get(url,binary=False):
 for attempt in range(2):
  try:
   r=requests.get(url,timeout=(15,55),headers={'User-Agent':'AcademicFigureReferenceLibrary/1.0 (personal research)'})
   r.raise_for_status()
   return r.content if binary else r.text
  except Exception:
   if attempt:raise
   time.sleep(1.5)
def soup(url,cache=None):
 p=CACHE/(cache or hashlib.sha1(url.encode()).hexdigest()+'.html')
 if p.exists():s=p.read_text(encoding='utf8')
 else:s=get(url);p.write_text(s,encoding='utf8')
 return BeautifulSoup(s,'html.parser')
TOPICS=[('transformer|attention|mamba|state.space','02_Transformer与注意力'),('graph|message.passing|relational|knowledge.graph','03_图神经网络与关系推理'),('diffusion|denois|generative|gan|variational','04_生成模型与扩散机制'),('retriev|rag|search.augment','05_检索增强与知识系统'),('multimodal|multi.modal|vision.language|visual.language|cross.modal|audio.visual','06_多模态与跨模态融合'),('agent|reinforcement|policy|robot|planning|embodied','07_强化学习与智能体'),('contrastive|self.supervis|masked|distill|pretrain','08_训练策略与自监督'),('3d|nerf|gaussian|render|point.cloud|mesh','09_三维视觉与神经渲染'),('database|query|storage|distributed|index|stream|transaction','10_计算机系统与数据流程'),('causal|neurosci|brain|biomolecular|protein','11_因果与AI科学机制'),('segment|detect|convol|encoder|decoder|u.net','01_视觉网络与编码解码')]
def category(text):
 for pattern,name in TOPICS:
  if re.search(pattern,text,re.I):return name
 return '12_通用方法与总体框架'
def select(items,n):
 items=list(dict((p['title'].lower(),p) for p in items).values())
 chosen=[]; seen=set()
 # Round-robin across subject areas avoids collecting only diffusion papers.
 for round_ in range(10):
  for pattern,_ in TOPICS:
   candidates=[p for p in items if p['title'] not in seen and re.search(pattern,p['title'],re.I)]
   if candidates:
    # Framework titles are more likely to provide usable architecture schematics.
    p=max(candidates,key=lambda q:sum(bool(re.search(k,q['title'],re.I)) for k in ['framework','architecture','network','learning','model','pipeline'])-0.2*bool(re.search('survey|position|theory|bound',q['title'],re.I)))
    chosen.append(p);seen.add(p['title'])
    if len(chosen)>=n:return chosen
 return chosen
def discover_one(spec):
 typ,venue,year,url,cache,count=spec
 try:
  s=soup(url,cache); items=[]
  if typ in ['cvf','eccv','neurips','acl']:
   for a in s.select('a[href]'):
    href=a['href'];title=a.get_text(' ',strip=True)
    if typ=='cvf' and re.search(r'/content/.+/html/.+_paper.html$',href):
     purl=urljoin(url,href);pdf=purl.replace('/html/','/papers/').replace('.html','.pdf')
    elif typ=='eccv' and f'eccv_{year}' in href and '/html/' in href:
     purl=urljoin(url,href);pdf=None
    elif typ=='neurips' and '/hash/' in href and 'Abstract-Conference.html' in href:
     purl=urljoin(url,href);pdf=purl.replace('/hash/','/file/').replace('Abstract-Conference.html','Paper-Conference.pdf')
    elif typ=='acl' and re.fullmatch(f'/{year}.acl-long.\\d+/',href):
     purl=urljoin(url,href);pdf=purl.rstrip('/')+'.pdf'
    else:continue
    if len(title)>8:items.append(dict(title=title,venue=venue,year=year,source_url=purl,pdf_url=pdf,source_kind='official_proceedings'))
  elif typ=='pmlr':
   for t in s.select('p.title'):
    links=t.find_next('p',class_='links')
    if not links:continue
    aa=[a for a in links.select('a[href]')]
    purl=next((urljoin(url,a['href']) for a in aa if a.get_text(strip=True)=='abs'),None)
    pdf=next((urljoin(url,a['href']) for a in aa if 'pdf' in a.get_text(strip=True).lower()),None)
    if purl and pdf:items.append(dict(title=t.get_text(' ',strip=True),venue=venue,year=year,source_url=purl,pdf_url=pdf,source_kind='official_proceedings'))
  elif typ=='jmlr':
   for dl in s.select('dl'):
    dt=dl.find('dt');a=dl.find('a',href=re.compile(r'\.pdf$'))
    if dt and a:
     title=dt.get_text(' ',strip=True)
     items.append(dict(title=title,venue=venue,year=year,source_url=urljoin(url,a['href']).replace('.pdf','.html'),pdf_url=urljoin(url,a['href']),source_kind='official_journal'))
  elif typ=='vldb':
   for a in s.select('a[href]'):
    if '.pdf' not in a['href'] or 'p' not in a['href']:continue
    parent=a.parent
    for _ in range(3):
     title=parent.find(['h3','h4','h5'])
     if title:break
     parent=parent.parent
    if title:items.append(dict(title=title.get_text(' ',strip=True),venue=venue,year=year,source_url=url,pdf_url=urljoin(url,a['href']),source_kind='official_journal'))
  chosen=select(items,count)
  print(json.dumps({'discovered':venue,'year':year,'available':len(items),'selected':len(chosen)},ensure_ascii=False),flush=True)
  return chosen
 except Exception as e:FAIL.append({'stage':'discovery','url':url,'error':str(e)});return []
def discover():
 specs=[('cvf','CVPR',2024,'https://openaccess.thecvf.com/CVPR2024?day=all','6.html',16),('cvf','ICCV',2023,'https://openaccess.thecvf.com/ICCV2023?day=all',None,12),('cvf','CVPR',2022,'https://openaccess.thecvf.com/CVPR2022?day=all',None,8),('eccv','ECCV',2024,'https://www.ecva.net/papers.php','4.html',10),('neurips','NeurIPS',2024,'https://proceedings.neurips.cc/paper_files/paper/2024','1.html',12),('pmlr','ICML',2024,'https://proceedings.mlr.press/v235/','0.html',12),('acl','ACL',2024,'https://aclanthology.org/events/acl-2024/','2.html',12),('jmlr','JMLR',2024,'https://jmlr.org/papers/v25/','3.html',8),('vldb','PVLDB',2024,'https://www.vldb.org/pvldb/vol17.html','5.html',6)]
 allp=[]
 with concurrent.futures.ThreadPoolExecutor(4) as ex:
  for part in ex.map(discover_one,specs):allp+=part
 classics=[
 ('Attention Is All You Need','NeurIPS',2017,'https://proceedings.neurips.cc/paper/2017/hash/3f5ee243547dee91fbd053c1c4a845aa-Abstract.html','https://proceedings.neurips.cc/paper/2017/file/3f5ee243547dee91fbd053c1c4a845aa-Paper.pdf'),
 ('Deep Residual Learning for Image Recognition','CVPR',2016,'https://openaccess.thecvf.com/content_cvpr_2016/html/He_Deep_Residual_Learning_CVPR_2016_paper.html','https://openaccess.thecvf.com/content_cvpr_2016/papers/He_Deep_Residual_Learning_CVPR_2016_paper.pdf'),
 ('Swin Transformer: Hierarchical Vision Transformer using Shifted Windows','ICCV',2021,'https://openaccess.thecvf.com/content/ICCV2021/html/Liu_Swin_Transformer_Hierarchical_Vision_Transformer_Using_Shifted_Windows_ICCV_2021_paper.html','https://openaccess.thecvf.com/content/ICCV2021/papers/Liu_Swin_Transformer_Hierarchical_Vision_Transformer_Using_Shifted_Windows_ICCV_2021_paper.pdf'),
 ('Masked Autoencoders Are Scalable Vision Learners','CVPR',2022,'https://openaccess.thecvf.com/content/CVPR2022/html/He_Masked_Autoencoders_Are_Scalable_Vision_Learners_CVPR_2022_paper.html','https://openaccess.thecvf.com/content/CVPR2022/papers/He_Masked_Autoencoders_Are_Scalable_Vision_Learners_CVPR_2022_paper.pdf'),
 ('Segment Anything','ICCV',2023,'https://openaccess.thecvf.com/content/ICCV2023/html/Kirillov_Segment_Anything_ICCV_2023_paper.html','https://openaccess.thecvf.com/content/ICCV2023/papers/Kirillov_Segment_Anything_ICCV_2023_paper.pdf'),
 ('Adding Conditional Control to Text-to-Image Diffusion Models','ICCV',2023,'https://openaccess.thecvf.com/content/ICCV2023/html/Zhang_Adding_Conditional_Control_to_Text-to-Image_Diffusion_Models_ICCV_2023_paper.html','https://openaccess.thecvf.com/content/ICCV2023/papers/Zhang_Adding_Conditional_Control_to_Text-to-Image_Diffusion_Models_ICCV_2023_paper.pdf'),
 ('High-Resolution Image Synthesis with Latent Diffusion Models','CVPR',2022,'https://openaccess.thecvf.com/content/CVPR2022/html/Rombach_High-Resolution_Image_Synthesis_With_Latent_Diffusion_Models_CVPR_2022_paper.html','https://openaccess.thecvf.com/content/CVPR2022/papers/Rombach_High-Resolution_Image_Synthesis_With_Latent_Diffusion_Models_CVPR_2022_paper.pdf'),
 ('An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale','ICLR',2021,'https://openreview.net/forum?id=YicbFdNTTy','https://openreview.net/pdf?id=YicbFdNTTy'),
 ('Graph Attention Networks','ICLR',2018,'https://openreview.net/forum?id=rJXMpikCZ','https://openreview.net/pdf?id=rJXMpikCZ'),
 ('Semi-Supervised Classification with Graph Convolutional Networks','ICLR',2017,'https://openreview.net/forum?id=SJU4ayYgl','https://openreview.net/pdf?id=SJU4ayYgl'),
 ('Denoising Diffusion Implicit Models','ICLR',2021,'https://openreview.net/forum?id=St1giarCHLP','https://openreview.net/pdf?id=St1giarCHLP'),
 ('Instant Neural Graphics Primitives with a Multiresolution Hash Encoding','ACM TOG / SIGGRAPH',2022,'https://nvlabs.github.io/instant-ngp/','https://nvlabs.github.io/instant-ngp/assets/mueller2022instant.pdf'),
 ('3D Gaussian Splatting for Real-Time Radiance Field Rendering','ACM TOG / SIGGRAPH',2023,'https://repo-sam.inria.fr/fungraph/3d-gaussian-splatting/','https://repo-sam.inria.fr/fungraph/3d-gaussian-splatting/3d_gaussian_splatting_low.pdf'),
 ]
 for t,v,y,u,p in classics:allp.append(dict(title=t,venue=v,year=y,source_url=u,pdf_url=p,source_kind='official_or_author_public_copy'))
 natures=[('s41586-024-07487-w','Nature','Accurate structure prediction of biomolecular interactions with AlphaFold 3',2024),('s41586-021-03819-2','Nature','Highly accurate protein structure prediction with AlphaFold',2021),('s42256-023-00748-9','Nature Machine Intelligence','Spatially embedded recurrent neural networks reveal widespread links between structural and functional neuroscience findings',2023),('s42256-024-00832-8','Nature Machine Intelligence','Augmenting large language models with chemistry tools',2024),('s42256-023-00744-z','Nature Machine Intelligence','Deep learning of causal structures in high dimensions under data limitations',2023),('s42256-024-00976-7','Nature Machine Intelligence','What large language models know and what people think they know',2025)]
 for slug,v,t,y in natures:
  allp.append(dict(title=t,venue=v,year=y,source_url='https://www.nature.com/articles/'+slug,pdf_url='https://www.nature.com/articles/'+slug+'.pdf',source_kind='official_open_access_journal'))
 allp=list(dict((p['title'].lower(),p) for p in allp).values())
 for i,p in enumerate(allp,1):p['id']=f'P{i:03}';p['category']=category(p['title'])
 save_json(META/'sources.json',allp);return allp
def download(p):
 try:
  folder=ROOT/'references'/p['category']/p['id'];folder.mkdir(parents=True,exist_ok=True)
  if p['pdf_url'] is None:
   s=soup(p['source_url'])
   a=next((a for a in s.select('a[href]') if '.pdf' in a['href'] and ('paper' in a.get_text().lower() or '/papers/' in a['href'])),None)
   if not a:raise ValueError('no public PDF link found')
   p['pdf_url']=urljoin(p['source_url'],a['href'])
  pdf=folder/'paper.pdf'
  if not pdf.exists():
   data=get(p['pdf_url'],True)
   if not data.startswith(b'%PDF'):raise ValueError('response is not a PDF')
   pdf.write_bytes(data)
  with fitz.open(pdf) as doc:
   if len(doc)==0:raise ValueError('empty PDF')
   first=doc[0].get_text();p['pages']=len(doc);p['pdf_first_page_excerpt']=first[:600]
  p['local_pdf']=pdf.relative_to(ROOT).as_posix();p['sha256']=hashlib.sha256(pdf.read_bytes()).hexdigest();p['bytes']=pdf.stat().st_size
  p['download_status']='ok';p['collected_date']='2026-10-01';p['license']='See original source; publicly accessible does not imply permission to republish.'
  save_json(folder/'source.json',p)
  print(json.dumps({'download':p['id'],'venue':p['venue'],'pages':p['pages']},ensure_ascii=False),flush=True)
 except Exception as e:
  p['download_status']='failed';p['error']=str(e);FAIL.append({'stage':'download','id':p['id'],'url':p['pdf_url'],'error':str(e)})
 return p
STRONG=r'architectur|framework|pipeline|schematic|overview|flowchart|workflow|computation.graph|message.passing|information.flow|mechanism|block.diagram'
MEDIUM=r'illustrat|encoder|decoder|attention.head|network.structure|network.model|graph.structure|aggregation|training.procedure|training.process|model.structure'
CHART=r'accuracy|performance|convergence|learning.curve|ablation|scatter|histogram|bar.chart|box.plot|roc.curve|precision.recall|t.sne|error.rate|benchmark.result'
def fig_type(caption):
 t=caption.lower()
 if 'message' in t or 'graph' in t:return '图结构与消息传递'
 if 'attention' in t:return '注意力与信息交互'
 if 'training' in t or 'distill' in t:return '训练机制与学习流程'
 if 'pipeline' in t or 'workflow' in t or 'flowchart' in t:return '方法流程图'
 if 'architecture' in t or 'encoder' in t or 'decoder' in t or 'network' in t:return '网络架构图'
 return '机制示意与总体框架'
def crop_for_caption(page,cap,allcaps):
 # Preserve vector drawings, labels and images; determine the visual band preceding the caption.
 W,H=page.rect.width,page.rect.height;x0,y0,x1,y1=cap['bbox']
 # A short centered caption can belong to a full-width diagram. Treating it
 # as a two-column caption cuts off half of classic Transformer/ECCV figures.
 full=x1-x0>W*.62 or abs((x0+x1)/2-W/2)<W*.12
 if full: left,right=22,W-22
 elif (x0+x1)/2<W/2:left,right=22,W/2+3
 else:left,right=W/2-3,W-22
 visuals=[]
 for d in page.get_drawings():
  r=fitz.Rect(d['rect'])
  if r.width>W*.94 and r.height<3:continue
  if r.y1<=y0+2 and r.y0>=28 and r.x1>=left and r.x0<=right:
   if r.width>1 or r.height>1:visuals.append(r)
 for im in page.get_image_info():
  r=fitz.Rect(im['bbox'])
  if r.y1<=y0+2 and r.y0>=28 and r.x1>=left and r.x0<=right:visuals.append(r)
 if not visuals:return None
 visuals.sort(key=lambda r:r.y0)
 bands=[]
 for r in visuals:
  if bands and r.y0<=bands[-1][1]+13:bands[-1][1]=max(bands[-1][1],r.y1);bands[-1][2].append(r)
  else:bands.append([r.y0,r.y1,[r]])
 band=bands[-1]
 if y0-band[1]>90:return None
 # If the bottom band consists only of isolated labels/lines, merge a nearby band.
 if band[1]-band[0]<35 and len(bands)>1 and band[0]-bands[-2][1]<40:
  band=[bands[-2][0],band[1],bands[-2][2]+band[2]]
 if band[1]-band[0]<22:return None
 # Ensure full-width schematic bounds are not cut at the column boundary.
 r=fitz.Rect(band[2][0])
 for v in band[2][1:]:r|=v
 if r.width>W*.58:left,right=22,W-22
 top=max(25,band[0]-12)
 for prev in allcaps:
  if prev['bbox'][3]<y0 and prev['bbox'][3]>top and abs(prev['bbox'][0]-x0)<W*.35:
   top=max(top,prev['bbox'][3]+5)
 rect=fitz.Rect(left,top,right,min(H-20,y1+5))
 return rect if rect.height>45 else None
def extract(p):
 if p.get('download_status')!='ok':return []
 out=[]
 folder=(ROOT/p['local_pdf']).parent;figdir=folder/'figures';figdir.mkdir(exist_ok=True)
 with fitz.open(ROOT/p['local_pdf']) as doc:
  for pn in range(min(len(doc),18)):
   page=doc[pn];blocks=page.get_text('dict')['blocks'];caps=[]
   for b in blocks:
    if b.get('type')!=0:continue
    t=' '.join(''.join(span['text'] for span in line['spans']) for line in b['lines']).strip()
    m=re.match(r'^(?:Figure|Fig\.)\s*(\d+)[\s:.(]',t,re.I)
    if m:caps.append({'text':t,'number':m.group(1),'bbox':b['bbox']})
   for cap in caps:
    t=cap['text'];strong=bool(re.search(STRONG,t,re.I));medium=bool(re.search(MEDIUM,t,re.I));chart=bool(re.search(CHART,t[:150],re.I))
    if not (strong or medium) or (chart and not strong):continue
    rect=crop_for_caption(page,cap,caps)
    if rect is None:continue
    fid=f"{p['id']}_F{cap['number']}_p{pn+1:02}"
    png=figdir/(fid+'.png');svg=figdir/(fid+'.svg')
    page.get_pixmap(matrix=fitz.Matrix(2,2),clip=rect,alpha=False).save(png)
    with fitz.open() as cropped:
     cp=cropped.new_page(width=rect.width,height=rect.height)
     cp.show_pdf_page(cp.rect,doc,pn,clip=rect)
     svg.write_text(cp.get_svg_image(text_as_path=True),encoding='utf8')
    pagepng=figdir/f'page_{pn+1:02}.png'
    if not pagepng.exists():page.get_pixmap(matrix=fitz.Matrix(1.2,1.2),alpha=False).save(pagepng)
    f=dict(id=fid,paper_id=p['id'],title=p['title'],venue=p['venue'],year=p['year'],category=category(p['title']+' '+t[:120]),diagram_type=fig_type(t),figure_number=cap['number'],pdf_page=pn+1,caption=t,source_url=p['source_url'],pdf_url=p['pdf_url'],local_pdf=p['local_pdf'],preview=png.relative_to(ROOT).as_posix(),vector_reference=svg.relative_to(ROOT).as_posix(),page_preview=pagepng.relative_to(ROOT).as_posix(),crop_bbox=list(rect),selection='caption keyword + vector geometry',review_status='自动筛选待逐图复核',has_possible_statistical_panels=bool(re.search(CHART,t,re.I)),editable_template=False)
    save_json(figdir/(fid+'.json'),f);out.append(f)
 print(json.dumps({'extracted':p['id'],'mechanism_candidates':len(out)},ensure_ascii=False),flush=True)
 return out
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--extract-only',action='store_true');args=ap.parse_args()
 if args.extract_only:papers=json.loads((META/'papers.json').read_text(encoding='utf8'))
 else:
  papers=discover()
  with concurrent.futures.ThreadPoolExecutor(5) as ex:papers=list(ex.map(download,papers))
  save_json(META/'papers.json',papers);save_json(META/'download_failures.json',FAIL)
 figures=[]
 # PyMuPDF is not thread safe; extraction is intentionally sequential.
 for p in papers:
  try:figures+=extract(p)
  except Exception as e:FAIL.append({'stage':'extraction','id':p['id'],'error':str(e)})
 save_json(META/'figures.json',figures);save_json(META/'issues.json',FAIL)
 with (META/'figure_index.csv').open('w',encoding='utf-8-sig',newline='') as file:
  fields=['id','paper_id','title','venue','year','category','diagram_type','figure_number','pdf_page','review_status','has_possible_statistical_panels','preview','vector_reference','source_url']
  w=csv.DictWriter(file,fieldnames=fields,extrasaction='ignore');w.writeheader();w.writerows(figures)
 print(json.dumps({'papers_ok':sum(p.get('download_status')=='ok' for p in papers),'figures':len(figures),'issues':len(FAIL)},ensure_ascii=False),flush=True)
if __name__=='__main__':main()
