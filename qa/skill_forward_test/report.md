# Offline forward-use test

Selected reference: **T17**, L08 stage swimlanes + V01 flat muted, original generic structural blueprint (MIT).

Reference PNG: `C:/Users/wengy/Documents/ChatGPT/论文阅读/绘图模板库/agent-skill/cs-mechanism-imagegen/assets/images/05/L08/T17.png`

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
