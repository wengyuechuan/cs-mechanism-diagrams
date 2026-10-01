"""Reproducible decisions from visual inspection of the v1/v2 contact sheets."""
from collect_library import *
import copy

# One layout / one visual-treatment label for each numbered thumbnail.
# X marks a candidate excluded from the mechanism library.
V1='''
04/01 06/02 06/02 06/02 06/02 06/02 01/04 04/01 09/04 01/04 09/04 09/04 09/01 04/03 04/01 05/05
03/03 04/02 02/03 09/04 04/04 02/05 06/03 09/04 04/04 02/04 07/01 04/04 04/03 09/04 05/04 09/01
09/03 06/01 04/01 09/02 09/03 09/06 06/03 02/03 02/03 01/01 05/01 07/02 02/03 08/03 09/03 04/04
04/01 09/01 02/03 09/03 04/03 09/01 01/03 07/01 09/05 02/03 07/03 09/03 09/01 02/02 02/03 09/01
09/01 12/02 04/04 09/05 04/01 09/01 02/01 05/05 07/04 02/05 11/02 04/03 03/03 02/03 02/01 09/01
04/01 02/04 04/01 05/02 07/04 07/01 02/04 06/01 02/01 11/04 01/04 04/01 09/01 04/05 09/02 01/02
02/02 03/02 04/01 09/01 06/04 09/02 06/01 01/04 02/04 09/01 04/01 04/02 05/05 05/05 01/03 04/01
07/01 04/01 05/05 07/04 09/04 07/05 09/04 04/02 04/01 01/04 06/01 02/03 04/01 01/01 04/01 12/01
09/02 09/05 04/01 07/01 02/03 01/02 01/02 01/02 02/01 09/03 05/05 09/03 09/03 09/03 08/04 09/03
02/04 09/01 06/04 09/04 04/03 04/03 09/04 09/01 12/04 07/05 01/04 09/04 01/03 09/03 08/01 X X 04/01 03/01 04/01
'''.split()
V2='''
04/03 04/01 09/04 02/04 04/04 06/01 X 02/04 09/01 04/04 09/04 03/04 05/02 02/01 09/05 X
09/05 11/04 04/04 04/03 X X 01/03 07/01 01/04 X 04/01 08/04 09/01 07/04 04/03 04/01
09/04 04/04 02/04 02/01 09/01 X X 02/03 09/04 04/03 05/05 X 02/01 09/01 X X
01/04 X X 04/01 01/03 04/04 02/01 01/04 06/04 X X 04/05 X X 09/04 01/04
05/01 04/04 04/03 X X 09/01 01/05 09/04 07/04 X 02/05 X X 07/04 02/03 X 02/01 06/01 04/05
'''.split()

def annotate(f,label):
    layout,visual=label.split('/')
    layout={'11':'10','12':'11'}.get(layout,layout)
    f.update(layout_style='L'+layout,visual_style='V'+visual,
             style_review='人工按缩略图检查主布局与视觉表达；不是会议官方风格标准',
             style_review_level='thumbnail visual classification',
             review_status='已完成机制类型与风格缩略图检查；细节请核对原PDF',
             review_level='thumbnail diagram-type and style review')
    return f

def redraw(f,rect,note):
    with fitz.open(ROOT/f['local_pdf']) as doc:
        page=doc[f['pdf_page']-1]
        page.get_pixmap(matrix=fitz.Matrix(2,2),clip=rect,alpha=False).save(ROOT/f['preview'])
        with fitz.open() as cropped:
            cp=cropped.new_page(width=rect.width,height=rect.height)
            cp.show_pdf_page(cp.rect,doc,f['pdf_page']-1,clip=rect)
            (ROOT/f['vector_reference']).write_text(cp.get_svg_image(text_as_path=True),encoding='utf8')
    f.update(crop_bbox=list(rect),crop_note=note,has_possible_statistical_panels=False)

def main():
    backup=META/'figures_v1_before_styles.json'
    if not backup.exists():backup.write_bytes((META/'figures.json').read_bytes())
    old=json.loads(backup.read_text(encoding='utf8'))
    new=json.loads((META/'v2_candidates.json').read_text(encoding='utf8'))
    assert len(old)==len(V1),(len(old),len(V1))
    assert len(new)==len(V2),(len(new),len(V2))
    records=[];decisions=[]
    repairs={'P034_F4_p06':(22,60.24,348,191.27),'P039_F2_p03':(30,25,384,153.15),
             'P041_F3_p07':(307,278.71,485,381.58),'P042_F3_p05':(306,230,484,341.20),
             'P060_F2_p03':(45,348.60,294,507.31)}
    for i,(f,label) in enumerate(zip(old,V1),1):
        if label=='X':
            decisions.append({'id':f['id'],'batch':'v1','decision':'exclude','reason':'数据样例或含数值结果的混合原图，本次风格库不纳入'})
            continue
        f=copy.deepcopy(f)
        if f['id'] in repairs:redraw(f,fitz.Rect(repairs[f['id']]),'二次复核裁剪：修复跨栏截断或移除旁边正文')
        records.append(annotate(f,label))
        decisions.append({'id':f['id'],'batch':'v1','decision':'include','layout_style':f['layout_style'],'visual_style':f['visual_style']})
    for i,(f,label) in enumerate(zip(new,V2),1):
        if label=='X':
            decisions.append({'id':f['id'],'batch':'v2','decision':'exclude','reason':'统计结果、纯结果/数据展示、正文提示文本或混合图不作为机制风格参考'})
            continue
        f=copy.deepcopy(f)
        with fitz.open(ROOT/f['local_pdf']) as doc:
            page=doc[f['pdf_page']-1];rect=fitz.Rect(f['crop_bbox'])
            for b in page.get_text('dict')['blocks']:
                if b.get('type')!=0:continue
                text=' '.join(''.join(s['text'] for s in ln['spans']) for ln in b['lines']).strip()
                if text==f['caption']:rect.y1=min(rect.y1,b['bbox'][1]-2);break
            if i==64:rect.x0=72;rect.x1=302;rect.y0=80
            if i==5:rect.x1=rect.x0+rect.width*.54
            if i==55:rect.x1=rect.x0+rect.width*.45
            if i==35:rect.x1=rect.x0+rect.width*.89
        if rect.height<20:raise ValueError(f['id']+' crop too short')
        redraw(f,rect,'机制图形裁剪；图注见元数据'+('；仅保留机制子区域，排除统计/正文区域' if i in [5,35,55] else ''))
        f['batch']='v2-2025-expansion';records.append(annotate(f,label))
        decisions.append({'id':f['id'],'batch':'v2','decision':'include','layout_style':f['layout_style'],'visual_style':f['visual_style']})
    assert len([f for f in records if f.get('batch')=='v2-2025-expansion'])>=50
    papers={p['id']:p for p in json.loads((META/'papers.json').read_text(encoding='utf8'))}
    for f in records:
        f['category']=papers[f['paper_id']]['category']
        f['topic_review_note']='按来源论文主要方法主题归类；布局与视觉风格另行标注'
    save_json(META/'figures.json',records)
    for f in records:save_json((ROOT/f['preview']).with_suffix('.json'),f)
    save_json(ROOT/'qa/style_classification_decisions.json',decisions)
    print(json.dumps({'total_figures':len(records),'v2_new_figures':sum(f.get('batch')=='v2-2025-expansion' for f in records),'layout_labels':len(set(f['layout_style'] for f in records)),'visual_labels':len(set(f['visual_style'] for f in records))},ensure_ascii=False))

if __name__=='__main__':main()
