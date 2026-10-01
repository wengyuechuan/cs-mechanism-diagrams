"""Validate deliverable files, provenance, XML structure and link targets."""
import sys,json,hashlib,re,xml.etree.ElementTree as ET
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent/'vendor'))
from PIL import Image
import pymupdf
ROOT=Path(__file__).resolve().parents[1];errors=[];warnings=[]
def load(n):return json.loads((ROOT/'metadata'/n).read_text(encoding='utf8'))
ps,fs,ts=load('papers.json'),load('figures.json'),load('templates.json')
for collection in [ps,fs,ts]:
 ids=[x['id'] for x in collection]
 if len(ids)!=len(set(ids)):errors.append('duplicate IDs')
for p in ps:
 if p.get('download_status')!='ok':errors.append('paper not downloaded: '+p['id']);continue
 file=ROOT/p['local_pdf']
 if not file.exists():errors.append('missing PDF: '+p['id']);continue
 if hashlib.sha256(file.read_bytes()).hexdigest()!=p['sha256']:errors.append('hash mismatch: '+p['id'])
 with pymupdf.open(file) as d:
  if len(d)!=p['pages']:errors.append('page count mismatch: '+p['id'])
for f in fs:
 if f['paper_id'] not in {p['id'] for p in ps}:errors.append('orphan figure '+f['id'])
 for key in ['preview','vector_reference','local_pdf','page_preview']:
  if not (ROOT/f[key]).exists():errors.append('missing '+key+' '+f['id'])
 with Image.open(ROOT/f['preview']) as im:
  im.verify()
 ET.parse(ROOT/f['vector_reference'])
 if '缩略图' not in f.get('review_status',''):errors.append('unreviewed '+f['id'])
for t in ts:
 for key in ['drawio','preview','spec']:
  if not (ROOT/t[key]).exists():errors.append('missing '+key+' '+t['id'])
 root=ET.parse(ROOT/t['drawio']).getroot();cells=root.findall('.//mxCell');byid={c.get('id'):c for c in cells}
 if not {'0','1'}.issubset(byid):errors.append('missing root cells '+t['id'])
 if len(cells)!=len(byid):errors.append('duplicate XML IDs '+t['id'])
 for c in cells:
  if c.get('parent') and c.get('parent') not in byid:errors.append('unknown parent '+t['id'])
  if c.get('edge')=='1':
   if c.get('source') not in byid or c.get('target') not in byid:errors.append('dangling edge '+t['id'])
   if c.find('mxGeometry') is None:errors.append('edge without geometry '+t['id'])
 ET.parse(ROOT/t['preview'])
 sp=json.loads((ROOT/t['spec']).read_text(encoding='utf8'))
 for n in sp['nodes']:
  if n['x']<0 or n['y']<0 or n['x']+n['w']>sp['width'] or n['y']+n['h']>sp['height']:errors.append('off-canvas '+t['id'])
  # Text width is a conservative approximation, reported as a review warning.
  if n['shape'] not in ['ellipse','graph'] and any(len(line)*7.3>n['w']-12 for line in n['label'].split('\n')):warnings.append('long label '+t['id']+'/'+n['id'])
 for i,a in enumerate(sp['nodes']):
  for b in sp['nodes'][i+1:]:
   if min(a['x']+a['w'],b['x']+b['w'])>max(a['x'],b['x']) and min(a['y']+a['h'],b['y']+b['h'])>max(a['y'],b['y']):errors.append('overlapping nodes '+t['id']+'/'+a['id']+'/'+b['id'])
 if not t.get('edit_url','').startswith('https://app.diagrams.net/#R'):errors.append('missing editor URL '+t['id'])
payload=(ROOT/'index.html').read_text(encoding='utf8')
if str(len(fs)) not in payload:errors.append('gallery count absent')
report={'source_papers':len(ps),'mechanism_references':len(fs),'editable_templates':len(ts),'categories':len(set(t['category'] for t in ts)),'errors':errors,'warnings':warnings,'validation':'file integrity, PDF pages/hashes, image decodability, SVG/XML parsing, editable cells/edges, geometry bounds and duplicate IDs','native_drawio_export_verified':False}
(ROOT/'qa'/'validation_report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(report,ensure_ascii=False,indent=2))
if errors:raise SystemExit(1)
