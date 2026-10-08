# Top-Conf skill forward test

Result: PASS (behavior tests); documentation reference exists at report time: True.

Only `qa/topconf_skill_test/forward.md` and `qa/topconf_skill_test/forward.json` were written. No imagegen call. All reported filesystem paths are repository-relative.

Catalog: 3710 records = 3439 Top-Conf + 271 local references.

## Test evidence

| Case | Exit | Returned / total | Pass |
|---|---:|---:|---|
| HippoRAG reviewed-only | 0 | 1 / 1 | True |
| source topconf | 0 | 2 / 3439 | True |
| source local | 0 | 2 / 9 | True |
| combined pattern venue year | 0 | 4 / 4 | True |
| reviewed-only topconf | 0 | 20 / 20 | True |
| combined reviewed filters | 0 | 1 / 1 | True |
| zero unknown query | 0 | 0 / 0 | True |
| zero incompatible venue | 0 | 0 / 0 | True |
| zero historical year | 0 | 0 / 0 | True |
| search unreviewed marker allowed | 0 | 1 / 2309 | True |
| catalog verify JPEG/PNG | 0 | - / - | True |
| reject preset L00/V01 | 2 | - / - | True |
| reject preset L08/V00 | 2 | - / - | True |
| reject preset L00/V00 | 2 | - / - | True |

## HippoRAG provenance and local review

ID: `TCF_neurips2024-1022`. Image: `agent-skill/cs-mechanism-imagegen/assets/imported/topconf/neurips2024-1022.jpg`.

Authors: Bernal J. Gutiérrez, Yiheng Shu, Yu Gu, Michihiro Yasunaga, Yu Su.
Venue/year: NeurIPS 2024. Source: https://proceedings.neurips.cc/paper_files/paper/2024/hash/6ddc001d07ca4f319af96a3024f6dbd1-Abstract-Conference.html.
Upstream: https://github.com/qwdwqfwq/topconf-paper-figure-gallery; commit `1f49dc03cfbfe12a1b8846815d25d3ec5a8253da`; ID `neurips2024-1022`; raw pattern `teaser`.

Authors, paper/PDF URLs, upstream teaser label, commit and exact JPEG bytes match the pinned local checkout. Local override `metadata/topconf_review_overrides.json` preserves teaser and assigns reviewed L09/V04. The review text explicitly limits review to layout/visual expression rather than a complete algorithm audit.

Side-by-side conceptual comparison of current RAG, human memory and HippoRAG, mixing brain illustrations, entity icons and arrows; L09 and V04 are defensible local expression tags. Upstream teaser is not architecture classification. This image is conceptual overview, not a substitute for complete algorithm topology. Some left-edge labels are clipped in the imported crop.

## JPEG and presets

CLI verify: 3710 images, 0 errors. Independent Pillow verify: 3439 imported JPEGs, 0 errors.

Each of L00/V01, L08/V00 and L00/V00 is rejected with exit 2 before output files are created. L00/V00 search remains allowed so candidates can be inspected. A reviewed L09/V04 prompt was built only in memory.

Pillow verify is independent structural verification; library verify checks file hash and parsed PNG/JPEG header dimensions, not a full pixel-decoding proof.

## Documentation and limits

The skill linked `references/topconf-import.md`, missing on initial read; existence at report time: True. Parent was notified; the document was created and then independently read. The initial missing link is resolved. Its snapshot commit, imported count and 20/3419 review split match the data.

Publication attribution was checked against pinned upstream data, not against a fetched publisher page or full PDF. The test inspected the actual HippoRAG JPEG via view_image. It does not conclude that all 3439 candidates are locally reviewed or suitable method references.

Independent full pixel decode: 3439 JPEGs, 0 errors (`Image.open` + `Image.load`).

Documentation observation: `references/topconf-import.md` says complete JPEG decoding occurs at import, but `tools/import_topconf.py` uses `Image.verify` without `Image.load`. This wording/implementation mismatch was reported to parent; production files were not changed by this test. No corrupt image was found.

Final resolution: parent changed the importer to `Image.load` and reimported all 3439 JPEGs successfully. See [resolved findings](resolved_findings.md).
