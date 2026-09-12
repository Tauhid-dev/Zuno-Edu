# Independent state/workflow review

Reviewer: product_inventory, independent of workflow_system author. Initial review found 3 High and 2 Medium issues; 0 Critical. Author corrections are underway; independent recheck remains required.

| Finding | Severity | Evidence and correction |
|---|---|---|
| SW-01 | High | Normal unmerged feature-only PR metadata is absent from master. Reconciler reselects the same PLANNED chunk. Discover fresh open PRs by exact chunk marker/base/repository and head branch, without master writes; test true feature-only handoff. |
| SW-02 | High | Omitting LAUNCH_SCOPE from witnesses allowed later scope edits while reporting LOCKED. Enforce complete mandatory witness inventory in generation, validation and reconciliation; include normalized chunk manifest bodies. |
| SW-03 | High | Bot-merged implementation PR counted COMPLETE. Require human merged_by for normal implementation completion as well as planning approval. |
| SW-04 | Medium | Docs required authenticated-only gh despite supported public/token HTTPS fallback. Align documentation and fail-closed network/rate-limit semantics. |
| SW-05 | Medium | Validation hardcoded scope1.0/architecture1, blocking authorized future version changes. Validate version format and coherent approved authority instead. |

Scratch Git reproductions verified SW-01/02/03. Existing 17 workflow tests passed but did not cover these cases; the new regressions must prove corrections and master remains unchanged.
