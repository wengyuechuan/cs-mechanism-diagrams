# Topconf integration baseline

This baseline was captured before integration. Production files were read only; no imagegen call was made.

- Current `scripts/library.py search --query HippoRAG`: exit 0, `matches: 0`, `results: []`.
- Upstream commit: `1f49dc03cfbfe12a1b8846815d25d3ec5a8253da`.
- Actual `data/figures.json` records: **3449**. README badge says 3452; use the actual data count.
- Upstream matching figure: `neurips2024-1022`, **HippoRAG: Neurobiologically Inspired Long-Term Memory for Large Language Models**, NeurIPS 2024.
- Authors: Bernal J. Gutiérrez; Yiheng Shu; Yu Gu; Michihiro Yasunaga; Yu Su.
- Original pattern: **teaser**. This is not evidence that the image is a mechanism diagram. No image-content judgment has been made in this baseline.

Integration must retain the upstream repository and exact commit, original figure ID/image path/hash, full author list, paper title, paper URL, PDF-source URL, venue/year, original pattern and image-conversion/cropping notes. Imported topic/layout/visual tags need an explicit pending-review status until visual inspection; teaser must not be silently promoted to mechanism.

The upstream MIT license covers code, not paper images. Retain attribution and source links, and mark per-paper rights verification explicitly.

After integration, the forward test should repeat the user-facing HippoRAG search, inspect the actual returned image, verify provenance and pending-review fields, and prepare a prompt whose topology comes from the supplied method brief. The parent agent will handle real image generation.

Full commands, raw output, source record and file hashes are saved in `baseline.json`.
