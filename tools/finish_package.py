import json,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];meta=ROOT/'metadata';qa=ROOT/'qa'
papers=json.loads((meta/'papers.json').read_text(encoding='utf8'))
history=[]
for p in meta.glob('*issues.json'):
 history.append({'file':p.name,'historical_records':json.loads(p.read_text(encoding='utf8'))})
history.append({'file':'download_failures.json','historical_records':json.loads((meta/'download_failures.json').read_text(encoding='utf8'))})
(qa/'download_attempt_history.json').write_text(json.dumps(history,ensure_ascii=False,indent=2),encoding='utf8')
for p in papers:
 if p.get('download_status')=='ok':
  p.pop('error',None);p['copy_note']=p.get('copy_note','原论文集/出版商公开版本' if 'preprint' not in p['source_kind'] else '作者公开预印本；期刊身份由 DOI / 正式书目信息确认')
  folder=(ROOT/p['local_pdf']).parent;(folder/'source.json').write_text(json.dumps(p,ensure_ascii=False,indent=2),encoding='utf8')
(meta/'papers.json').write_text(json.dumps(papers,ensure_ascii=False,indent=2),encoding='utf8')
(meta/'sources.json').write_text(json.dumps([{k:p.get(k) for k in ['id','title','venue','year','category','source_url','pdf_url','source_kind','copy_note','download_status']} for p in papers],ensure_ascii=False,indent=2),encoding='utf8')
(meta/'download_failures.json').write_text(json.dumps([p for p in papers if p.get('download_status')!='ok'],ensure_ascii=False,indent=2),encoding='utf8')
with zipfile.ZipFile(ROOT/'可编辑机制图模板_48套.zip','w',compression=zipfile.ZIP_DEFLATED) as z:
 for p in (ROOT/'templates').rglob('*'):
  if p.is_file():z.write(p,p.relative_to(ROOT).as_posix())
 for name in ['方法图绘制指南.md','LICENSE_TEMPLATES.txt']:z.write(ROOT/name,name)
 z.writestr('先读我.txt','48 套原创可编辑机制图模板，按 12 类整理。\n.drawio 用 diagrams.net 或 draw.io 桌面版编辑；.svg 是预览。\n原论文与原图参考请在完整资料库的 index.html 查看，此压缩包只打包可编辑模板。\n')
counts={}
for name in ['references','templates','metadata','tools','qa']:
 counts[name]=round(sum(p.stat().st_size for p in (ROOT/name).rglob('*') if p.is_file())/1048576,2)
print(json.dumps({'folder_megabytes':counts,'templates_zip_megabytes':round((ROOT/'可编辑机制图模板_48套.zip').stat().st_size/1048576,2)},ensure_ascii=False))
