"""Apply documented thumbnail review decisions and recrop mechanism-only regions."""
from collect_library import *
import copy
figures=json.loads((META/'figures.json').read_text(encoding='utf8'))
# Explicit visual exclusions from the contact-sheet review, not uninspected AI labels.
excluded={
 'P006_F3_p08':'正文引用被误识别为图注',
 'P015_F1_p01':'纯输入样例，不是机制图',
 'P021_F4_p05':'任务与评价矩阵，不是网络机制',
 'P026_F5_p09':'结果可视化样例',
 'P032_F1_p01':'数据域样例',
 'P038_F4_p12':'定性配准结果',
 'P040_F3_p08':'图像数据生成示例，机制表达不足',
 'P042_F1_p01':'生成结果对比',
 'P042_F2_p02':'图像分布示意与结果样例',
 'P042_F4_p07':'生成结果比较',
 'P050_F2_p02':'坐标数值曲线',
 'P050_F3_p08':'训练性能曲线',
 'P053_F3_p09':'定性注意力结果',
 'P070_F2_p02':'注意力统计热图',
 'P071_F5_p08':'统计柱状图',
 'P071_F7_p15':'统计柱状图',
 'P072_F4_p13':'正文引用被误识别为图注',
 'P080_F5_p05':'统计热图',
 'P080_F7_p07':'注意力结果热图',
 'P080_F8_p07':'注意力结果热图',
 'P080_F11_p14':'统计热图',
 'P080_F13_p17':'统计热图',
 'P080_F14_p18':'统计热图',
 'P082_F1_p05':'散点图与统计分布',
 'P096_F8_p07':'消融结果与生成样例',
 'P097_F2_p02':'统计曲线与结果示例',
 'P098_F5_p07':'性能散点图',
 'P103_F10_p11':'渲染结果对比',
 'P106_F3_p04':'机制与统计结果混排，本批不收',
 'P106_F6_p08':'参数数值结果',
 'P108_F3_p04':'统计结果曲线',
 'P108_F6_p07':'ROC曲线与柱状图',
 'P112_F3_p07':'统计热图与散点结果',
 'P119_F2_p04':'论文时间线，不是机制图',
 'P119_F6_p09':'检测结果样例',
 'P119_F7_p10':'论文时间线',
 'P119_F10_p16':'论文时间线',
 'P120_F3_p02':'统计性能曲线',
 'P120_F4_p03':'论文时间线',
 'P122_F6_p08':'生成结果对比',
 'P125_F1_p01':'问答样例与统计曲线混排',
 'P127_F2_p03':'问答输出样例',
 'P127_F4_p05':'嵌入散点图',
 'P127_F6_p08':'检测结果示例',
 'P129_F3_p04':'数据集样例',
 'P129_F4_p04':'数据集样例',
}
wide={'P031_F2_p05','P037_F2_p06','P037_F3_p07','P038_F2_p05','P040_F2_p04','P041_F2_p06','P043_F1_p02','P043_F2_p05','P044_F2_p05','P044_F3_p07','P045_F2_p04','P060_F2_p03','P063_F3_p04','P063_F5_p06','P065_F6_p16','P066_F7_p13','P089_F3_p08','P091_F1_p03','P105_F3_p04','P107_F1_p02','P109_F1_p02','P115_F3_p04'}
# Mixed originals retain only explicitly reviewed mechanism subpanels.
# Fractions are relative to the complete figure graphics region (caption excluded).
subregions={'P013_F1_p02':[(.52,0,1,1,'右侧方法结构，剔除左侧词频柱图')],
 'P034_F4_p06':[(0,0,.60,1,'左侧策略网络结构，剔除右侧实验表格')],
 'P100_F1_p04':[(0,0,.57,1,'左侧 GCN 结构，剔除右侧嵌入结果')],
 'P104_F2_p03':[(0,0,.49,.53,'子图 a：表征网络机制'),(0,.53,1,1,'子图 c：扩散结构机制，剔除子图 b 训练曲线')],
 'P106_F1_p02':[(0,0,.55,1,'左侧空间网络约束机制，剔除右侧统计热图')]}
records=[];review=[];seen=set()
for f in figures:
 if f['id'] in seen:review.append({'id':f['id'],'decision':'deduplicate'});continue
 seen.add(f['id'])
 if f['id'] in excluded:review.append({'id':f['id'],'decision':'exclude','reason':excluded[f['id']]});continue
 with fitz.open(ROOT/f['local_pdf']) as doc:
  pn=f['pdf_page']-1;page=doc[pn];rect=fitz.Rect(f['crop_bbox'])
  # Keep graph graphics only; captions and prose remain in metadata and the original page.
  for b in page.get_text('dict')['blocks']:
   if b.get('type')!=0:continue
   t=' '.join(''.join(s['text'] for s in line['spans']) for line in b['lines']).strip()
   if t==f['caption']:
    rect.y1=min(rect.y1,b['bbox'][1]-2);break
  if f['id'] in wide:rect.x0=22;rect.x1=page.rect.width-22
  # A centered graphic may cross columns even when a caption does not.
  if f['venue']=='ECCV':rect.x0=115;rect.x1=page.rect.width-115
  if rect.height<20:review.append({'id':f['id'],'decision':'exclude','reason':'未发现完整图形区域'});continue
  regions=subregions.get(f['id'],[(0,0,1,1,'仅裁出机制图形；图注见索引')])
  for idx,(a,b,c,d,note) in enumerate(regions):
   out=copy.deepcopy(f)
   if len(regions)>1:out['id']=f['id']+chr(97+idx);out['figure_number']=f['figure_number']+chr(97+idx)
   region=fitz.Rect(rect.x0+a*rect.width,rect.y0+b*rect.height,rect.x0+c*rect.width,rect.y0+d*rect.height)
   png=(ROOT/f['preview']).parent/(out['id']+'.png');svg=png.with_suffix('.svg')
   page.get_pixmap(matrix=fitz.Matrix(2,2),clip=region,alpha=False).save(png)
   with fitz.open() as cropped:
    cp=cropped.new_page(width=region.width,height=region.height);cp.show_pdf_page(cp.rect,doc,pn,clip=region);svg.write_text(cp.get_svg_image(text_as_path=True),encoding='utf8')
   out.update(preview=png.relative_to(ROOT).as_posix(),vector_reference=svg.relative_to(ROOT).as_posix(),crop_bbox=list(region),crop_note=note,review_status='已完成缩略图类型检查；结构细节请核对原PDF',review_level='thumbnail diagram-type review',has_possible_statistical_panels=False)
   save_json(png.with_suffix('.json'),out);records.append(out)
  review.append({'id':f['id'],'decision':'include','cropped_subpanels':f['id'] in subregions,'full_width_fix':f['id'] in wide})
save_json(META/'figures_candidates.json',figures);save_json(META/'figures.json',records);save_json(ROOT/'qa'/'curation_decisions.json',review)
# Delete only collector-generated candidate previews that are not in the curated set.
active={p for f in records for p in [f['preview'],f['vector_reference'],str(Path(f['preview']).with_suffix('.json')).replace('\\','/')]}
for f in figures:
 for suffix in ['.png','.svg','.json']:
  p=(ROOT/f['preview']).with_suffix(suffix)
  if p.relative_to(ROOT).as_posix() not in active and p.exists():
   assert p.resolve().is_relative_to((ROOT/'references').resolve()) and p.parent.name=='figures'
   p.unlink()
print(json.dumps({'candidates':len(figures),'curated_mechanisms':len(records),'excluded':sum(r['decision']=='exclude' for r in review),'deduplicated':sum(r['decision']=='deduplicate' for r in review)},ensure_ascii=False))
