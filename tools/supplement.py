from collect_library import *
papers=json.loads((META/'papers.json').read_text(encoding='utf8'))
figures=json.loads((META/'figures.json').read_text(encoding='utf8'))
fallback={'P098':'2010.11929','P099':'1710.10903','P100':'1609.02907','P101':'2010.02502'}
todo=[]
for p in papers:
 if p['id'] in fallback and p.get('download_status')!='ok':
  p['original_pdf_url']=p['pdf_url'];p['pdf_url']='https://arxiv.org/pdf/'+fallback[p['id']];p['source_kind']='author_preprint_of_verified_conference_paper';p['copy_note']='OpenReview returned HTTP 403; downloaded the publicly available arXiv author version.';todo.append(p)
more=[]
def add(t,v,y,u,pdf,kind='official_or_author_public_copy'):
 more.append(dict(title=t,venue=v,year=y,source_url=u,pdf_url=pdf,source_kind=kind,category=category(t)))
s=BeautifulSoup((CACHE/'5.html').read_text(encoding='utf8'),'html.parser');data=json.loads(s.select_one('script#__NEXT_DATA__').text)['props']['pageProps']['groupedIssues']
vldb=[dict(title=p['title'],venue='PVLDB',year=2024,source_url=p['pdf'],pdf_url=p['pdf'],source_kind='official_journal') for ps in data.values() for p in ps if p['title']!='Front Matter']
for keyword in ['nsDB:','DecLog:','FedGTA:','GastCoCo:','ELEET:','TenGraph:']:
 p=next((p for p in vldb if keyword in p['title']),None)
 if p:p['category']=category(p['title']);more.append(p)
for slug,t in [('21-1127','Tianshou: A Highly Modularized Deep Reinforcement Learning Library'),('15-239','Domain-Adversarial Training of Neural Networks'),('16-272','Neural Autoregressive Distribution Estimation')]:
 vol={'21-1127':23,'15-239':17,'16-272':17}[slug];y=2022 if vol==23 else 2016
 add(t,'JMLR',y,f'https://jmlr.org/papers/v{vol}/{slug}.html',f'https://jmlr.org/papers/volume{vol}/{slug}/{slug}.pdf','official_journal')
add('Deep Learning for 3D Point Clouds: A Survey','IEEE TPAMI',2021,'https://doi.org/10.1109/TPAMI.2020.3005434','https://arxiv.org/pdf/1912.12033','author_preprint_of_verified_journal_paper')
add('Deep Learning for Generic Object Detection: A Survey','IJCV',2020,'https://doi.org/10.1007/s11263-019-01247-4','https://arxiv.org/pdf/1809.02165','author_preprint_of_verified_journal_paper')
more+=discover_one(('cvf','CVPR',2025,'https://openaccess.thecvf.com/CVPR2025?day=all',None,12))
more+=discover_one(('neurips','NeurIPS',2025,'https://proceedings.neurips.cc/paper_files/paper/2025',None,8))
seen={p['title'].lower() for p in papers}
for p in more:
 if p['title'].lower() in seen:continue
 seen.add(p['title'].lower());p['id']=f'P{len(papers)+1:03}';papers.append(p);todo.append(p)
with concurrent.futures.ThreadPoolExecutor(5) as ex:list(ex.map(download,todo))
save_json(META/'papers.json',papers)
for p in todo:
 try:figures+=extract(p)
 except Exception as e:FAIL.append({'stage':'extraction','id':p['id'],'error':str(e)})
save_json(META/'figures.json',figures);save_json(META/'supplement_issues.json',FAIL)
print(json.dumps({'papers_ok':sum(p.get('download_status')=='ok' for p in papers),'figures':len(figures),'remaining_failures':[p['id'] for p in papers if p.get('download_status')!='ok']},ensure_ascii=False),flush=True)
