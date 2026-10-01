import json
import subprocess
import sys
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parents[2] / 'agent-skill/cs-mechanism-imagegen'
OUT = Path(__file__).resolve().parent
LIBRARY = ROOT / 'scripts/library.py'

def run(name, args):
    command = [sys.executable, str(LIBRARY), *args]
    p = subprocess.run(command, capture_output=True, text=True, encoding='utf-8')
    evidence = {'command': command, 'exit_code': p.returncode, 'stdout': p.stdout, 'stderr': p.stderr}
    (OUT / (name + '.evidence.json')).write_text(json.dumps(evidence, ensure_ascii=False, indent=2), encoding='utf-8')
    print(name + ': exit=' + str(p.returncode))
    return p

run('01-list', ['list'])
selected = run('02-search-selected', ['search', '--topic', 'retrieval', '--layout', 'L08', '--visual', 'V01', '--limit', '4'])
empty = run('03-search-empty-combination', ['search', '--topic', 'retrieval', '--layout', 'L03', '--visual', 'V03', '--limit', '4'])
assert empty.returncode == 0
empty_data = json.loads(empty.stdout)
assert empty_data['matches'] == 0 and empty_data['results'] == []

brief = json.loads((ROOT / 'assets/briefs/graph-rag.json').read_text(encoding='utf-8'))
brief['intent'] = 'Draw a graph-structured RAG mechanism diagram with two labelled swimlanes, offline graph indexing and online answering, in a flat muted academic style.'
brief['layout_notes'] += ['Give the top lane four balanced nodes and the bottom lane five balanced nodes. Use sufficient width for Entity-relation extraction; do not abbreviate it.', 'Graph index to Subgraph retrieval has exactly one arrowhead at Subgraph retrieval. Align or route this connection through the inter-lane gutter.']
brief['avoid'] += ['answer writeback', 'reverse graph-read arrow', 'gradients, shadows, glossy 3D blocks']
brief_path = OUT / 'graph-rag.request.brief.json'
brief_path.write_text(json.dumps(brief, ensure_ascii=False, indent=2), encoding='utf-8')
good = run('04-prompt-valid', ['prompt', '--brief', str(brief_path), '--refs', 'T17', '--layout', 'L08', '--visual', 'V01', '--out', str(OUT / 'graph-rag')])
assert good.returncode == 0

injected = json.loads(json.dumps(brief))
injected['edges'].append({'source': 'A', 'target': 'G', 'kind': 'write', 'label': 'answer writeback'})
injected_path = OUT / 'graph-rag.injected-forbidden.brief.json'
injected_path.write_text(json.dumps(injected, ensure_ascii=False, indent=2), encoding='utf-8')
bad = run('05-prompt-forbidden-edge', ['prompt', '--brief', str(injected_path), '--refs', 'T17', '--layout', 'L08', '--visual', 'V01', '--out', str(OUT / 'rejected')])
bad_data = json.loads(bad.stdout)
assert bad.returncode == 2 and 'conflicts with non_edges' in bad_data['error']
assert not any(OUT.glob('rejected.*'))

summary = {'empty_combination': {'status': 'pass', 'query': {'topic': 'retrieval', 'layout': 'L03', 'visual': 'V03'}, 'matches': empty_data['matches']}, 'forbidden_answer_writeback': {'status': 'pass', 'exit_code': bad.returncode, 'error': bad_data['error'], 'output_written': False}, 'valid_prompt': {'status': 'pass', **json.loads(good.stdout)}, 'image_generation': {'status': 'not_run', 'reason': 'Explicit offline evaluation constraint'}}
(OUT / 'test-summary.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps(summary, ensure_ascii=False, indent=2))
