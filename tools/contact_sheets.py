import sys,json,math
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent/'vendor'))
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[1];qa=ROOT/'qa';qa.mkdir(exist_ok=True)
items=json.loads((ROOT/'metadata'/'figures.json').read_text(encoding='utf8'))
font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',15)
for b in range(math.ceil(len(items)/16)):
 sheet=Image.new('RGB',(1600,1360),'#dde2e8');d=ImageDraw.Draw(sheet)
 for j,it in enumerate(items[b*16:(b+1)*16]):
  x=(j%4)*400;y=(j//4)*340;im=Image.open(ROOT/it['preview']).convert('RGB');im.thumbnail((384,280));sheet.paste(im,(x+(400-im.width)//2,y+26+(280-im.height)//2));d.text((x+8,y+5),it['id']+' | '+it['venue'],fill='#172334',font=font);d.text((x+8,y+310),it['caption'][:46].encode('ascii','replace').decode(),fill='#172334',font=font)
 sheet.save(qa/f'references_{b+1:02}.jpg',quality=92)
print(json.dumps({'figures':len(items),'sheets':math.ceil(len(items)/16)}))
