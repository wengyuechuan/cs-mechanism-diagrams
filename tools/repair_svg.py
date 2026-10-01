from pathlib import Path
import re,json,xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1];repairs=[]
def valid(n):return n in [9,10,13] or 32<=n<=0xD7FF or 0xE000<=n<=0xFFFD or 0x10000<=n<=0x10FFFF
for file in (ROOT/'references').rglob('*.svg'):
 try:ET.parse(file)
 except ET.ParseError:
  text=file.read_text(encoding='utf8')
  def replace(m):
   v=m.group(1);n=int(v[1:],16) if v.lower().startswith('x') else int(v)
   return m.group(0) if valid(n) else ''
  fixed=re.sub(r'&#(x[0-9a-fA-F]+|[0-9]+);',replace,text)
  fixed=''.join(c for c in fixed if valid(ord(c)))
  ET.fromstring(fixed);file.write_text(fixed,encoding='utf8');repairs.append(file.relative_to(ROOT).as_posix())
(ROOT/'qa'/'svg_repairs.json').write_text(json.dumps({'removed_invalid_pdf_text_control_references_from':repairs,'original_pdf_and_png_unchanged':True},ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps({'repaired_svg':len(repairs)}))
