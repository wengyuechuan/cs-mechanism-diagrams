"""Add public 2025 papers without replacing the reviewed v1 figures."""
from collect_library import *

def main():
    papers=json.loads((META/'papers.json').read_text(encoding='utf8'))
    specs=[('cvf','ICCV',2025,'https://openaccess.thecvf.com/ICCV2025?day=all',None,24),
           ('pmlr','ICML',2025,'https://proceedings.mlr.press/v267/',None,16),
           ('acl','ACL',2025,'https://aclanthology.org/events/acl-2025/',None,12)]
    new=[]
    with concurrent.futures.ThreadPoolExecutor(3) as pool:
        for part in pool.map(discover_one,specs):new.extend(part)
    seen={p['title'].lower() for p in papers}
    todo=[]
    for p in new:
        if p['title'].lower() in seen:continue
        seen.add(p['title'].lower());p['id']=f'P{len(papers)+1:03}'
        p['category']=category(p['title']);p['copy_note']='官方会议公开论文版本';p['batch']='v2-2025-expansion'
        papers.append(p);todo.append(p)
    with concurrent.futures.ThreadPoolExecutor(5) as pool:list(pool.map(download,todo))
    save_json(META/'papers.json',papers)
    candidates=[]
    for p in todo:
        try:candidates.extend(extract(p))
        except Exception as e:FAIL.append({'stage':'extraction','id':p['id'],'error':str(e)})
    save_json(META/'v2_candidates.json',candidates)
    save_json(META/'v2_download_issues.json',FAIL)
    print(json.dumps({'new_papers':len(todo),'downloaded':sum(p.get('download_status')=='ok' for p in todo),'candidate_figures':len(candidates)},ensure_ascii=False),flush=True)

if __name__=='__main__':main()
