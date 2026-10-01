# Public documentation review — 2026-10-01

The repository README is hand-maintained and now describes offline browsing,
skill installation, retrieval/prompt commands, layout/visual taxonomy,
editable templates, dependencies, validation scope, contributions and licensing.

`LICENSE` covers original project materials only. `THIRD_PARTY_NOTICES.md` and
`metadata/rights_review.json` make the redistribution-review status explicit:
223 paper images remain unverified; no per-image clearance is claimed.

The current tracked documentation and archived test JSON use `${REPO_ROOT}`,
`${USER_SKILL_ROOT}` or `${USER_HOME}` in place of the previous local paths.
These are redacted historical records, not executable tool arguments. The
offline harness scripts locate this checkout using `__file__`; fresh runs may
write new machine-specific paths to their local evidence, which should be
reviewed before committing.

Past commits were not rewritten. They still contain the original image files
and historical paths. Changes in the current tree do not remove past content.
No remote was configured and no files were published during this documentation
update. A public distribution containing paper images still requires the
review described in the third-party notices.
