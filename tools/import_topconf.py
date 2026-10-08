"""Import a pinned Top-Conf gallery snapshot without executing upstream code."""
import argparse,json,hashlib,shutil,subprocess,re,sys
from pathlib import Path
from collections import Counter
ROOT=Path(__file__).resolve().parents[1]
UPSTREAM_URL='https://github.com/qwdwqfwq/topconf-paper-figure-gallery'
LAYOUT_MAP={'pipeline':'L01','framework':'L04','conceptual':'L10','comparison':'L09'}
TOPICS=['01_视觉网络与编码解码','02_Transformer与注意力','03_图神经网络与关系推理','04_生成模型与扩散机制','05_检索增强与知识系统','06_多模态与跨模态融合','07_强化学习与智能体','08_训练策略与自监督','09_三维视觉与神经渲染','10_计算机系统与数据流程','11_因果与AI科学机制','12_通用方法与总体框架']

def dump(p,x):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,ensure_ascii=False,indent=2),encoding='utf8')

def source_image(root,value):
    p=(root/value).resolve()
    if not p.is_relative_to(root.resolve()):raise ValueError('Upstream image path escapes checkout')
    return p

def topic(title):
    rules=[('11',r'protein|molecular|molecule|biomolec|causal|causality|drug |gene |genomic|chemistry'),
           ('05',r'\brag\b|hipporag|retriev|knowledge.?augment|long.term memory'),
           ('06',r'multimodal|multi.modal|cross.modal|vision.language|visual.language|audio.visual'),
           ('03',r'\bgraph\b|\bgnn\b|hypergraph|knowledge graph'),
           ('07',r'reinforcement|\bagent\b|multi.agent|robot|embodied|policy optim|navigation|\brl\b'),
           ('09',r'\b3d\b|nerf|gaussian splat|radiance|point cloud|reconstruction|depth estim'),
           ('04',r'diffusion|generative|text.to.image|image generation|video generation|\bgan\b'),
           ('02',r'transformer|attention|mamba|state.space|language model|\bllm\b'),
           ('08',r'contrastive|self.supervised|distill|pre.?train|fine.tun|continual|unlearn|preference optim'),
           ('10',r'distributed|database|federat|query execut|serving|parallel|compiler|cache'),
           ('01',r'segment|detect|image|vision|visual|video|recognition|deblur')]
    for tid,pattern in rules:
        if re.search(pattern,title,re.I):return tid
    return '12'

def normalize(row,commit):
    ident=row['id']
    if not re.fullmatch(r'[A-Za-z0-9_.-]+',ident):raise ValueError('Unsupported upstream ID')
    tid=topic(row['title']);pattern=row.get('pattern','unknown')
    return {'id':'TCF_'+ident,'title':row['title'],'authors':row.get('authors',[]),'venue':row['venue'].upper() if row['venue']!='neurips' else 'NeurIPS','year':row['year'],
        'topic':tid,'category':TOPICS[int(tid)-1],'kind':'upstream_reference','source_collection':'topconf',
        'source_url':row['paper'],'pdf_url':row.get('pdf_source'),'figure_number':'1 / teaser','pdf_page':None,
        'layout_style':LAYOUT_MAP.get(pattern,'L00'),'visual_style':'V00','upstream_pattern':pattern,
        'description':'上游 Figure 1 / teaser 参考；本库机制与风格待复核','keywords':' '.join(row.get('authors',[]))+' '+pattern,
        'upstream_id':ident,'upstream_repository':UPSTREAM_URL,'upstream_commit':commit,'upstream_image':row.get('image'),
        'upstream_score':row.get('score'),'upstream_tier':row.get('tier',row.get('acceptance_tier')),
        'topic_review':'title-keyword suggestion; inspect figure before use','style_review_status':'pending',
        'style_review':'上游 pattern 仅映射候选布局；视觉风格及机制范围尚未在本库看图复核',
        'crop_note':'原样复制上游图像；未重新裁剪或重编码','rights':'Original paper authors/publisher; upstream MIT covers code only',
        'redistribution_status':'unverified','copy_note':'Top-Conf Figure Gallery snapshot; source version provided by upstream'}

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--checkout',type=Path,default=ROOT/'external-cache/topconf-paper-figure-gallery');args=p.parse_args()
    checkout=args.checkout.resolve();commit=subprocess.check_output(['git','-C',str(checkout),'rev-parse','HEAD'],text=True).strip()
    rows=json.loads((checkout/'data/figures.json').read_text(encoding='utf8'))
    sys.path.insert(0,str(ROOT/'tools/vendor'));from PIL import Image
    records=[];skipped=[];byhash={};seen=set();output=ROOT/'agent-skill/cs-mechanism-imagegen/assets/imported/topconf'
    output.mkdir(parents=True,exist_ok=True)
    overrides_path=ROOT/'metadata/topconf_review_overrides.json';overrides=json.loads(overrides_path.read_text(encoding='utf8')) if overrides_path.exists() else {}
    for row in rows:
        if row['id'] in seen:raise ValueError('Duplicate upstream ID: '+row['id'])
        seen.add(row['id'])
        if row.get('pattern')=='results':skipped.append({'id':row['id'],'reason':'pure results pattern excluded from mechanism references'});continue
        if overrides.get(row['id'],{}).get('exclude'):
            skipped.append({'id':row['id'],'reason':overrides[row['id']]['review_note']});continue
        src=source_image(checkout,row['image']);data=src.read_bytes();sha=hashlib.sha256(data).hexdigest()
        with Image.open(src) as im:w,h=im.size;im.load()
        if min(w,h)<30:raise ValueError('Image too small: '+row['id'])
        if sha in byhash:
            byhash[sha].setdefault('upstream_aliases',[]).append(row);skipped.append({'id':row['id'],'reason':'exact image duplicate','canonical_id':byhash[sha]['id']});continue
        x=normalize(row,commit);x.update(width=w,height=h,image_sha256=sha)
        if row['id'] in overrides:x.update(overrides[row['id']])
        dest=output/(row['id']+src.suffix.lower());shutil.copy2(src,dest)
        x['image']=dest.relative_to(ROOT).as_posix();x['skill_image']=dest.relative_to(ROOT/'agent-skill/cs-mechanism-imagegen').as_posix()
        records.append(x);byhash[sha]=x
    expected={(ROOT/x['image']).resolve() for x in records}
    for stale in output.glob('*.jpg'):
        resolved=stale.resolve()
        if not resolved.is_relative_to(output.resolve()):raise ValueError('Unsafe generated image path')
        if resolved not in expected:stale.unlink()
    # Keep original upstream notices with the adapted data; no upstream .git is copied.
    notice_dir=ROOT/'third_party/topconf-paper-figure-gallery'
    for name in ['LICENSE','NOTICE.md','IMAGES_POLICY.md']:
        notice_dir.mkdir(parents=True,exist_ok=True);shutil.copy2(checkout/name,notice_dir/name)
    dump(ROOT/'metadata/external_figures.json',records)
    report={'repository':UPSTREAM_URL,'commit':commit,'import_date':'2026-10-08','upstream_index_records':len(rows),'imported_distinct_images':len(records),'skipped_records':skipped,
            'patterns':dict(Counter(x['upstream_pattern'] for x in records)),'venues':dict(Counter(x['venue'] for x in records)),
            'manually_reviewed_in_this_library':sum(x.get('style_review_status')=='reviewed' for x in records),'total_bytes':sum((ROOT/x['image']).stat().st_size for x in records),
            'review_scope':'Bulk records retain upstream curation; local topics inferred, layout suggestions mapped, visual styles pending unless explicit manual override.'}
    dump(ROOT/'metadata/topconf_import_report.json',report)
    dump(ROOT/'metadata/topconf_rights_review.json',{'repository':UPSTREAM_URL,'commit':commit,'cleared_for_public_distribution':False,'records':[{'id':x['id'],'authors':x['authors'],'title':x['title'],'source_url':x['source_url'],'image':x['image'],'status':'unverified'} for x in records]})
    print(json.dumps({k:v for k,v in report.items() if k!='skipped_records'},ensure_ascii=False))

if __name__=='__main__':main()
