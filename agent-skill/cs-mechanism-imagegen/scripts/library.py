"""Offline retrieval and validated imagegen prompt preparation. Standard library only."""
import argparse,json,sys,hashlib,struct
from pathlib import Path
from collections import Counter
ROOT=Path(__file__).resolve().parents[1]
TOPICS={'01':['vision','cnn','视觉','编码解码'],'02':['transformer','attention','mamba','注意力'],
        '03':['graph','gnn','图神经网络'],'04':['generation','diffusion','生成','扩散'],
        '05':['retrieval','rag','graphrag','检索'],'06':['multimodal','多模态'],
        '07':['rl','agent','reinforcement','强化学习','智能体'],'08':['training','ssl','自监督','训练'],
        '09':['3d','nerf','render','三维'],'10':['systems','system','数据库','系统'],
        '11':['causal','science','因果','科学'],'12':['general','framework','通用']}

def read(name):return json.loads((ROOT/'references'/name).read_text(encoding='utf8'))
def emit(data):print(json.dumps(data,ensure_ascii=False,indent=2))
def topic_id(value):
    if not value:return None
    value=str(value).casefold()
    for k,aliases in TOPICS.items():
        if value==k or value in aliases or value.startswith(k+'_'):return k
    raise ValueError('Unknown topic: '+value+'; use list to inspect topics')

def search(catalog,topic=None,layout=None,visual=None,query='',limit=6,kind=None):
    tid=topic_id(topic);words=query.casefold().split()
    matches=[]
    for x in catalog:
        if tid and x['topic']!=tid:continue
        if layout and x['layout_style']!=layout:continue
        if visual and x['visual_style']!=visual:continue
        if kind and x['kind']!=kind:continue
        hay=' '.join(str(x.get(k,'')) for k in ['id','title','description','category','caption','keywords']).casefold()
        if not all(w in hay for w in words):continue
        matches.append(x)
    # Editable structural blueprints are especially clear mechanism references.
    return sorted(matches,key=lambda x:(x['kind']!='original_blueprint',-int(x.get('year',0)),x['id']))[:limit]

def safe_image(record):
    p=(ROOT/record['image']).resolve()
    if not p.is_relative_to(ROOT.resolve()):raise ValueError('Image path escapes skill directory: '+record['id'])
    return p

def validate_brief(b):
    if not isinstance(b,dict):raise ValueError('Brief must be an object')
    nodes=b.get('nodes');edges=b.get('edges')
    if not isinstance(nodes,list) or not nodes:raise ValueError('nodes must be a nonempty list')
    if not isinstance(edges,list):raise ValueError('edges must be a list')
    ids=set()
    for n in nodes:
        if not isinstance(n,dict) or not isinstance(n.get('id'),str) or not n['id'].strip() or not isinstance(n.get('label'),str) or not n['label'].strip():raise ValueError('Each node needs nonempty string id/label')
        if n['id'] in ids:raise ValueError('Duplicate node ID: '+n['id'])
        ids.add(n['id'])
    seen=set()
    for e in edges:
        if not isinstance(e,dict) or e.get('source') not in ids or e.get('target') not in ids:raise ValueError('Unknown edge endpoint: '+str(e))
        key=(e['source'],e['target'],e.get('kind','data'))
        if key in seen:raise ValueError('Duplicate directed edge: '+str(key))
        seen.add(key)
        if e.get('line','solid') not in ['solid','dashed']:raise ValueError('line must be solid or dashed')
        if e.get('kind','data') not in ['data','control','loss','read','write']:raise ValueError('Unknown edge kind')
    non=b.get('non_edges',[])
    for pair in non:
        if not isinstance(pair,list) or len(pair)!=2 or pair[0] not in ids or pair[1] not in ids:raise ValueError('Invalid forbidden edge')
        if any(e['source']==pair[0] and e['target']==pair[1] for e in edges):raise ValueError('Allowed edge conflicts with non_edges: '+str(pair))
    groups=b.get('groups',[]);gids=set()
    for g in groups:
        if not isinstance(g,dict) or not isinstance(g.get('id'),str) or not g['id'] or not isinstance(g.get('label'),str) or not g['label']:raise ValueError('Groups need id/label')
        if g['id'] in gids:raise ValueError('Duplicate group ID')
        gids.add(g['id'])
        if not isinstance(g.get('members'),list) or any(m not in ids for m in g['members']):raise ValueError('Unknown group member')
        if len(g['members'])!=len(set(g['members'])):raise ValueError('Duplicate group member')
    for n in nodes:
        if n.get('group') and (n['group'] not in gids or n['id'] not in next(g['members'] for g in groups if g['id']==n['group'])):raise ValueError('Node group and group members disagree')
    for key in ['invariants','layout_notes','exact_labels','avoid']:
        if key in b and (not isinstance(b[key],list) or any(not isinstance(v,str) for v in b[key])):raise ValueError(key+' must be a list of strings')
    if b.get('background','white') not in ['white','transparent']:raise ValueError('background must be white or transparent')
    if b.get('topic'):topic_id(b['topic'])
    return b

def make_prompt(brief,refs,layout,visual):
    b=validate_brief(brief);tax=read('style-taxonomy.json')
    l=next((x for x in tax['layouts'] if x['id']==layout),None)
    v=next((x for x in tax['visuals'] if x['id']==visual),None)
    if l is None or v is None:raise ValueError('Unknown layout or visual style')
    lines=['Use case: infographic-diagram',
           'Asset type: research-paper mechanism / architecture figure, raster output',
           'Primary request: '+b.get('intent',b.get('title','Draw the supplied method')),
           'Canvas/backdrop: '+b.get('aspect_ratio',l['suggested_aspect_ratio'])+' landscape; '+b.get('background','white')+' background; generous whitespace; crisp readable labels.',
           'Layout: '+l['prompt_clause'],'Style/medium: '+v['prompt_clause'],
           'Color palette: '+str(b.get('palette') or v['suggested_palette']),
           'Input images:']
    if refs:
        for i,x in enumerate(refs,1):
            lines.append(f"Image {i}: style/layout reference ({x['id']}); borrow visual grammar only. Do not reproduce its algorithm, labels, title or footer.")
    else:lines.append('None. Generate a new diagram from the structure below.')
    lines.append(f"Scientific topology: EXACTLY {len(b['nodes'])} system nodes and {len(b['edges'])} directed system arrows. The following edge list is exhaustive.")
    lines.append('Nodes (IDs identify endpoints; do not render IDs unless part of the label):')
    for n in b['nodes']:
        lines.append(f"- {n['id']}: {json.dumps(n['label'],ensure_ascii=False)}; role={n.get('role','process')}"+(f"; group={n['group']}" if n.get('group') else '')+(f"; icon={n['icon']}" if n.get('icon') else '')+(f"; note={n['note']}" if n.get('note') else ''))
    lines.append('Directed system edges:')
    for i,e in enumerate(b['edges'],1):
        lines.append(f"{i}. {e['source']} -> {e['target']}; kind={e.get('kind','data')}; line={e.get('line','solid')}"+(f"; exact label={json.dumps(e['label'],ensure_ascii=False)}" if e.get('label') else '; no edge label'))
    lines.append('Group containers (boundaries represent membership, not data-flow links):')
    for g in b.get('groups',[]):lines.append(f"- {json.dumps(g['label'],ensure_ascii=False)}: "+', '.join(g['members']))
    lines.append('Forbidden system edges: '+('; '.join(f"{a} -> {z}" for a,z in b.get('non_edges',[])) or 'Any edge not in the exhaustive list.'))
    labels=[n['label'] for n in b['nodes']]+[g['label'] for g in b.get('groups',[])]+[e['label'] for e in b['edges'] if e.get('label')]+b.get('exact_labels',[])
    lines.append('Text (verbatim, no invented labels): '+json.dumps(list(dict.fromkeys(labels)),ensure_ascii=False))
    if b.get('show_title'):lines.append('Draw this title verbatim: '+json.dumps(b.get('title',''),ensure_ascii=False))
    else:lines.append('No main title, footer, template ID, watermark or source-paper name inside the diagram.')
    for key,label in [('invariants','Scientific invariants'),('layout_notes','Placement and routing'),('avoid','Avoid')]:
        if b.get(key):lines.append(label+': '+'; '.join(b[key]))
    lines.append('Constraints: Give each system arrow one clear arrowhead at the target. No additional system nodes or links; illustrative graph icons may contain small undirected edges distinct from the system arrows. Keep typography flat, aligned and legible at research-paper print size. No invented statistical results.')
    return '\n'.join(lines)+'\n'

def verify(catalog):
    errors=[];ids=set();tax=read('style-taxonomy.json');layouts={x['id'] for x in tax['layouts']};visuals={x['id'] for x in tax['visuals']}
    for x in catalog:
        if x['id'] in ids:errors.append('duplicate ID '+x['id'])
        ids.add(x['id'])
        if x['layout_style'] not in layouts or x['visual_style'] not in visuals:errors.append('unknown style '+x['id'])
        try:
            p=safe_image(x);data=p.read_bytes()
            if data[:8]!=b'\x89PNG\r\n\x1a\n':errors.append('not PNG '+x['id'])
            if hashlib.sha256(data).hexdigest()!=x['image_sha256']:errors.append('hash mismatch '+x['id'])
            w,h=struct.unpack('>II',data[16:24])
            if min(w,h)<30:errors.append('image too small '+x['id'])
        except (OSError,ValueError,struct.error) as e:errors.append(x['id']+': '+str(e))
    return {'images':len(catalog),'topics':len(set(x['topic'] for x in catalog)),'layout_styles':len(layouts),'visual_styles':len(visuals),'kinds':dict(Counter(x['kind'] for x in catalog)),'errors':errors}

def main():
    if hasattr(sys.stdout,'reconfigure'):sys.stdout.reconfigure(encoding='utf8')
    p=argparse.ArgumentParser(description=__doc__);sub=p.add_subparsers(dest='command',required=True)
    sub.add_parser('list');sub.add_parser('verify')
    q=sub.add_parser('search');q.add_argument('--topic');q.add_argument('--layout');q.add_argument('--visual');q.add_argument('--query',default='');q.add_argument('--limit',type=int,default=6);q.add_argument('--kind',choices=['paper_reference','original_blueprint'])
    a=sub.add_parser('prompt');a.add_argument('--brief',required=True,type=Path);a.add_argument('--refs',default='');a.add_argument('--layout',required=True);a.add_argument('--visual',required=True);a.add_argument('--out',required=True,type=Path);a.add_argument('--overwrite',action='store_true')
    args=p.parse_args()
    try:
        catalog=read('catalog.json')
        if args.command=='list':emit({'topics':[{'id':k,'aliases':v,'images':sum(x['topic']==k for x in catalog)} for k,v in TOPICS.items()],**read('style-taxonomy.json')})
        elif args.command=='verify':
            report=verify(catalog);emit(report)
            if report['errors']:sys.exit(1)
        elif args.command=='search':
            if args.limit<1:raise ValueError('limit must be positive')
            tax=read('style-taxonomy.json')
            if args.layout and args.layout not in {x['id'] for x in tax['layouts']}:raise ValueError('Unknown layout style')
            if args.visual and args.visual not in {x['id'] for x in tax['visuals']}:raise ValueError('Unknown visual style')
            rows=search(catalog,args.topic,args.layout,args.visual,args.query,args.limit,args.kind)
            emit({'matches':len(rows),'filter_policy':'strict; no silent fallback','results':[{**x,'absolute_image':str(safe_image(x))} for x in rows]})
        else:
            brief=validate_brief(json.loads(args.brief.read_text(encoding='utf-8-sig')));refs=[]
            for ident in filter(None,args.refs.split(',')):
                x=next((x for x in catalog if x['id']==ident),None)
                if x is None:raise ValueError('Unknown reference ID '+ident)
                if not safe_image(x).is_file():raise ValueError('Reference PNG missing '+ident)
                refs.append({**x,'absolute_image':str(safe_image(x))})
            prompt=make_prompt(brief,refs,args.layout,args.visual)
            files={'.prompt.txt':prompt,'.brief.json':json.dumps(brief,ensure_ascii=False,indent=2),'.references.json':json.dumps({'layout_style':args.layout,'visual_style':args.visual,'reference_images':refs,'transparent_background':brief.get('background')=='transparent'},ensure_ascii=False,indent=2)}
            paths={suffix:Path(str(args.out)+suffix) for suffix in files}
            if not args.overwrite and any(p.exists() for p in paths.values()):raise ValueError('Output exists; use a versioned name or --overwrite')
            args.out.parent.mkdir(parents=True,exist_ok=True)
            for suffix,data in files.items():paths[suffix].write_text(data,encoding='utf8')
            emit({'generated_prompt_files':[str(p.resolve()) for p in paths.values()],'nodes':len(brief['nodes']),'edges':len(brief['edges']),'reference_images':[str(safe_image(x)) for x in refs],'image_generation_called':False})
    except (ValueError,OSError,KeyError,TypeError) as e:
        emit({'error':str(e)});sys.exit(2)

if __name__=='__main__':main()
