import json,sys,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools/vendor'))
from PIL import Image,ImageDraw,ImageFont

def main():
    mode=sys.argv[1] if len(sys.argv)>1 else 'v1'
    records=json.loads((ROOT/'metadata'/('v2_candidates.json' if mode=='v2' else 'templates.json' if mode=='templates' else 'figures.json')).read_text(encoding='utf8'))
    if mode=='templates':records=[{**t,'preview':t['preview_png'],'venue':'Original','year':2026} for t in records]
    out=ROOT/'qa'/('v2_review' if mode=='v2' else 'templates_style_review' if mode=='templates' else 'style_review');out.mkdir(exist_ok=True)
    font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',16)
    for start in range(0,len(records),16):
        subset=records[start:start+16];sheet=Image.new('RGB',(1600,1200),'#e8edf3');d=ImageDraw.Draw(sheet)
        for i,f in enumerate(subset):
            x=(i%4)*400;y=(i//4)*300
            im=Image.open(ROOT/f['preview']).convert('RGB');im.thumbnail((386,242))
            sheet.paste(im,(x+7+(386-im.width)//2,y+36+(242-im.height)//2))
            d.text((x+9,y+6),f"{start+i+1:03} {f['id']}",font=font,fill='#152943')
            d.text((x+9,y+281),f"{f['venue']} {f['year']} | {f['title'][:29]}",font=font,fill='#334155')
        sheet.save(out/f'sheet_{start//16+1:02}.jpg',quality=93)
    (out/'ordered_records.json').write_text(json.dumps([{'number':i+1,'id':f['id'],'title':f['title']} for i,f in enumerate(records)],ensure_ascii=False,indent=2),encoding='utf8')
    print(str(out),len(records))

if __name__=='__main__':main()
