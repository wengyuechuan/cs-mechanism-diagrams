import sys, concurrent.futures, json
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent/'vendor'))
import requests
from bs4 import BeautifulSoup
urls=['https://proceedings.mlr.press/v235/','https://proceedings.neurips.cc/paper_files/paper/2024','https://aclanthology.org/events/acl-2024/','https://jmlr.org/papers/v25/','https://www.ecva.net/papers.php','https://www.vldb.org/pvldb/vol17.html','https://openaccess.thecvf.com/CVPR2024?day=all']
def fetch(item):
 i,u=item
 try:
  r=requests.get(u,timeout=45);r.raise_for_status()
  p=Path(__file__).parent/'cache';p.mkdir(exist_ok=True)
  (p/f'{i}.html').write_text(r.text,encoding='utf8')
  s=BeautifulSoup(r.text,'html.parser')
  links=[(a.get_text(' ',strip=True),a.get('href')) for a in s.select('a[href]') if len(a.get_text(strip=True))>30]
  return {'url':u,'length':len(r.text),'links':links[:7]}
 except Exception as e:return {'url':u,'error':str(e)}
with concurrent.futures.ThreadPoolExecutor(6) as ex:
 for r in ex.map(fetch,enumerate(urls)):print(json.dumps(r,ensure_ascii=False),flush=True)
