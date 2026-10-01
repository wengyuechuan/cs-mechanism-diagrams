from collect_library import *
papers=json.loads((META/'papers.json').read_text(encoding='utf8'))
todo=[]
for p in papers:
 if p.get('download_status')=='ok':continue
 p.setdefault('category',category(p['title']))
 if p['venue']=='PVLDB':p['original_pdf_url']=p['pdf_url'];p['pdf_url']=p['pdf_url'].replace('www.vldb.org','vldb.org')
 todo.append(p)
with concurrent.futures.ThreadPoolExecutor(4) as ex:list(ex.map(download,todo))
save_json(META/'papers.json',papers);save_json(META/'retry_issues.json',FAIL)
print(json.dumps({'ok':sum(p.get('download_status')=='ok' for p in papers),'failed':[p['id'] for p in papers if p.get('download_status')!='ok']},ensure_ascii=False))
