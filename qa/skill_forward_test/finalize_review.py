import json
from pathlib import Path

OUT = Path(__file__).resolve().parent
REF = 'C:/Users/wengy/Documents/ChatGPT/论文阅读/绘图模板库/agent-skill/cs-mechanism-imagegen/assets/images/05/L08/T17.png'

review = {
    'scope': 'Offline forward-use evaluation: retrieval, visual inspection, brief and prompt preparation, rejection tests. No imagegen call.',
    'selected_reference': {'id': 'T17', 'absolute_png': REF, 'kind': 'original_blueprint', 'layout': 'L08', 'visual': 'V01', 'source': 'Original generic structural blueprint; MIT', 'viewed_with': 'tools.view_image', 'observation': 'Two dashed swimlane containers, low-saturation rectangular process blocks, thin slate arrows, white background. Vector-index RAG labels differ from the requested graph RAG; use only its layout and style.'},
    'checks': {
        'brief_content': {'status': 'pass', 'observation': 'Nine requested nodes and exact labels; four offline and five online.'},
        'brief_topology': {'status': 'pass', 'observation': 'Eight exhaustive directed edges; G -> R is the sole cross-lane read edge; no A -> G edge.'},
        'prompt_topology': {'status': 'pass', 'observation': 'Prompt lists all eight edges, forbids A -> G, and specifies a single target arrowhead at Subgraph retrieval.'},
        'prompt_style_layout': {'status': 'pass', 'observation': 'L08 labelled stage swimlanes, V01 flat muted palette, white background, no shadows or gradients; lane membership and gutter routing supplied.'},
        'reference_visual_fit': {'status': 'pass', 'observation': 'T17 has the requested swimlane and low-saturation visual grammar. Prompt explicitly excludes its original algorithm, title and footer.'},
        'required_zero_result_test': {'status': 'pass', 'evidence': '03-search-empty-combination.evidence.json', 'observation': 'Known valid taxonomy IDs retrieval/L03/V03 returned matches=0 and results=[].'},
        'required_forbidden_edge_test': {'status': 'pass', 'evidence': '05-prompt-forbidden-edge.evidence.json', 'observation': 'A -> G write edge conflicts with non_edges; exit code 2; no rejected output files created.'},
        'generated_image_content_topology_text': {'status': 'unverified', 'observation': 'No image was generated under the offline test restriction.'},
        'generated_image_layout_style_print_readability': {'status': 'unverified', 'observation': 'No generated image exists; reference inspection does not validate the eventual output.'},
        'files': {'status': 'pass', 'observation': 'Brief, prompt, references, evidence and tool-call plan saved. Final diagram PNG intentionally absent.'}
    },
    'actual_defects_encountered': [],
    'limits': ['No critical skill defect encountered in this requested workflow and the two specified negative tests.', 'Reference T17 contains seven vector-RAG nodes and a title/footer; it is not the requested mechanism. The generated prompt correctly instructs replacing its method and suppressing these decorations.', 'Imagegen rendering fidelity, arrow direction, exact text and final print quality remain unverified.'],
    'harness_note': 'Initial outer test runner stdout used Windows console encoding and displayed Chinese paths incorrectly in the command output. Evidence files contain correct UTF-8 paths; runner now explicitly sets UTF-8 stdout. This was a test-harness issue, not a skill error.'
}
(OUT / 'review.json').write_text(json.dumps(review, ensure_ascii=False, indent=2), encoding='utf-8')

plan = {
    'status': 'planned_only_not_executed',
    'tool': 'tools.image_gen__imagegen',
    'arguments': {'prompt': (OUT / 'graph-rag.prompt.txt').read_text(encoding='utf-8'), 'referenced_image_paths': [REF], 'transparent_background': False},
    'precondition': 'T17 already inspected via view_image; image generation was explicitly excluded from this evaluation.',
    'invocation': '// @exec: {"yield_time_ms": 120000, "max_output_tokens": 1000}\nconst result = await tools.image_gen__imagegen(argumentsFromThisJson);\ngeneratedImage(result);',
    'post_generation': ['Use the real returned output path; copy a versioned PNG into the user project.', 'View the output and compare nine nodes, eight arrows, all labels, two swimlanes and G -> R direction against the brief.', 'If needed, edit one observed defect at a time, preserve topology and exact labels; retain original version.', 'Mark rendered-image checks unverified until actual image inspection.']
}
(OUT / 'imagegen-call-plan.json').write_text(json.dumps(plan, ensure_ascii=False, indent=2), encoding='utf-8')

report = '''# Offline forward-use test

Selected reference: **T17**, L08 stage swimlanes + V01 flat muted, original generic structural blueprint (MIT).

Reference PNG: `''' + REF + '''`

The requested mechanism has been prepared as **9 nodes / 8 arrows**. It has not been generated as an image.

- Actual normalized brief: `graph-rag.brief.json`
- Actual imagegen prompt: `graph-rag.prompt.txt`
- Reference metadata: `graph-rag.references.json`
- Review: `review.json`
- Exact planned tool arguments: `imagegen-call-plan.json` (not executed)

Negative tests passed:

1. `search --topic retrieval --layout L03 --visual V03 --limit 4` returned exit 0, matches 0 and an empty results array. Evidence: `03-search-empty-combination.evidence.json`.
2. Injecting `A -> G` as a write edge returned exit 2 with `Allowed edge conflicts with non_edges: ['A', 'G']`. No rejected prompt outputs were created. Evidence: `05-prompt-forbidden-edge.evidence.json`; injected input: `graph-rag.injected-forbidden.brief.json`.

No critical skill defect was encountered in this workflow. The T17 reference shows vector-index RAG, seven nodes, a title and footer; these are reference content rather than the target algorithm. The prompt explicitly excludes copying them. Final rendering fidelity, print readability and actual image topology remain unverified because imagegen was not called.

The initial test runner console display mis-decoded Chinese paths, while UTF-8 evidence files retained correct paths. The runner now explicitly selects UTF-8 stdout; this is a harness issue rather than a skill defect.
'''
(OUT / 'report.md').write_text(report, encoding='utf-8')

checks = ['graph-rag.brief.json', 'graph-rag.prompt.txt', 'graph-rag.references.json', '03-search-empty-combination.evidence.json', '05-prompt-forbidden-edge.evidence.json', 'review.json', 'imagegen-call-plan.json']
for name in checks:
    p = OUT / name
    assert p.is_file() and p.stat().st_size > 0
    if p.suffix == '.json':
        json.loads(p.read_text(encoding='utf-8'))
print('Verified all required local evidence and deliverable files.')
