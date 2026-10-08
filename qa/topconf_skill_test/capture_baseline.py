import datetime
import hashlib
import json
import subprocess
import sys
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
SKILL = ROOT / 'agent-skill/cs-mechanism-imagegen'
UPSTREAM = ROOT / 'external-cache/topconf-paper-figure-gallery'
command = [sys.executable, str(SKILL / 'scripts/library.py'), 'search', '--query', 'HippoRAG']
search = subprocess.run(command, cwd=SKILL, capture_output=True, text=True, encoding='utf-8')
search_data = json.loads(search.stdout)
assert search.returncode == 0 and search_data['matches'] == 0 and search_data['results'] == []
commit = subprocess.run(['git', 'rev-parse', 'HEAD'], cwd=UPSTREAM, capture_output=True, text=True, encoding='utf-8', check=True).stdout.strip()
assert commit == '1f49dc03cfbfe12a1b8846815d25d3ec5a8253da'
figures_file = UPSTREAM / 'data/figures.json'
figures = json.loads(figures_file.read_text(encoding='utf-8'))
assert len(figures) == 3449
hipporag = [row for row in figures if 'hipporag' in json.dumps(row).lower()]
catalog = SKILL / 'references/catalog.json'
catalog_data = json.loads(catalog.read_text(encoding='utf-8'))

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

baseline = {
    'captured_at': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'scope': 'Read-only pre-integration baseline; all outputs under qa/topconf_skill_test; no imagegen call',
    'skill_root': str(SKILL),
    'current_catalog': {'path': str(catalog), 'records': len(catalog_data), 'sha256': digest(catalog)},
    'current_library_script': {'path': str(SKILL / 'scripts/library.py'), 'sha256': digest(SKILL / 'scripts/library.py')},
    'hipporag_search': {'command': command, 'exit_code': search.returncode, 'stdout': search.stdout, 'stderr': search.stderr, 'parsed': search_data, 'conclusion': 'HippoRAG upstream figure is not retrievable before integration'},
    'upstream': {'repository': 'https://github.com/qwdwqfwq/topconf-paper-figure-gallery', 'local_path': str(UPSTREAM), 'commit': commit, 'data_file': str(figures_file), 'data_sha256': digest(figures_file), 'actual_record_count': len(figures), 'readme_badge_count': 3452, 'count_note': 'Use actual figures.json count 3449; README badge 3452 is stale for this commit'},
    'upstream_hipporag': [{'original_record': row, 'absolute_image': str(UPSTREAM / row['image']), 'image_exists': (UPSTREAM / row['image']).is_file(), 'image_sha256': digest(UPSTREAM / row['image']) if (UPSTREAM / row['image']).is_file() else None} for row in hipporag],
    'integration_requirements': {
        'provenance': ['Preserve upstream figure ID and original image path', 'Preserve paper title and complete authors list', 'Preserve paper URL and PDF-source URL separately', 'Preserve venue, year and original pattern', 'Record upstream repository and exact commit', 'Record imported image hash and any conversion/cropping notes'],
        'review_status': ['New layout/visual/topic tags must be marked pending review unless manually inspected', 'Retain original upstream pattern=teaser without equating it to mechanism', 'Do not infer mechanism suitability solely from title, venue, source pattern or automatic keyword classification', 'Separate imported paper references from original blueprints'],
        'rights': ['Upstream code MIT does not cover paper images', 'Retain original author/publisher attribution and original source links', 'Keep per-paper rights verification status explicit; gallery presence is not redistribution permission'],
        'forward_test': ['After integration, repeat HippoRAG query through the user-facing skill CLI', 'Inspect returned local image before selecting it as a visual reference', 'Check authors, paper/PDF links, commit and pending-review tags in the returned metadata', 'Prepare a topology-grounded prompt without treating the teaser as the requested algorithm']
    },
    'actual_baseline_findings': ['Existing skill HippoRAG query returns zero results', 'Upstream figures.json contains 3449 records, not README badge count 3452', 'Upstream HippoRAG record is tagged teaser; mechanism suitability remains unverified until visual inspection']
}
(OUT / 'baseline.json').write_text(json.dumps(baseline, ensure_ascii=False, indent=2), encoding='utf-8')

md = '''# Topconf integration baseline

This baseline was captured before integration. Production files were read only; no imagegen call was made.

- Current `scripts/library.py search --query HippoRAG`: exit 0, `matches: 0`, `results: []`.
- Upstream commit: `''' + commit + '''`.
- Actual `data/figures.json` records: **3449**. README badge says 3452; use the actual data count.
- Upstream matching figure: `neurips2024-1022`, **HippoRAG: Neurobiologically Inspired Long-Term Memory for Large Language Models**, NeurIPS 2024.
- Authors: Bernal J. Gutiérrez; Yiheng Shu; Yu Gu; Michihiro Yasunaga; Yu Su.
- Original pattern: **teaser**. This is not evidence that the image is a mechanism diagram. No image-content judgment has been made in this baseline.

Integration must retain the upstream repository and exact commit, original figure ID/image path/hash, full author list, paper title, paper URL, PDF-source URL, venue/year, original pattern and image-conversion/cropping notes. Imported topic/layout/visual tags need an explicit pending-review status until visual inspection; teaser must not be silently promoted to mechanism.

The upstream MIT license covers code, not paper images. Retain attribution and source links, and mark per-paper rights verification explicitly.

After integration, the forward test should repeat the user-facing HippoRAG search, inspect the actual returned image, verify provenance and pending-review fields, and prepare a prompt whose topology comes from the supplied method brief. The parent agent will handle real image generation.

Full commands, raw output, source record and file hashes are saved in `baseline.json`.
'''
(OUT / 'baseline.md').write_text(md, encoding='utf-8')
print(json.dumps({'baseline': str(OUT / 'baseline.json'), 'search_matches': search_data['matches'], 'upstream_records': len(figures), 'hipporag_records': len(hipporag), 'commit': commit}, ensure_ascii=False, indent=2))
