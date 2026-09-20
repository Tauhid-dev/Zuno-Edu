# Workflow optimisation verification

This change reuses the chunk registry/manifests, progress cache, reconciliation and
completion evidence, skill hierarchy, handoff archive and CI. No second planning or
state system was introduced. New routing metadata selects phases, contract entries,
checks, review depth and model recommendations; `next chunk` is the normal entry point.

## Preserved design

All 62 registry entries retain every pre-existing field, including ordering,
dependencies, scope and acceptance. Architecture files, API/frontend catalogs,
requirements and application directories are unchanged. SCOPE_LOCK's single review
policy clause now permits risk-appropriate review; product scope 1.0 and architecture
version 1 remain unchanged. No application implementation has begun.

## Scenario checks

| Scenario | Verified behavior |
| --- | --- |
| A: normal merge | Human merge plus immutable artifacts completes the chunk and releases its dependency. |
| B: open PR | PR_OPEN reserves work; dependent chunks cannot start; independent ready work remains eligible. |
| C: merge after previous session | Fresh remote proof supersedes local PR_OPEN/cache claims. |
| D: stale handoff/newer master | Current remote SHA and verified evidence win; caches cannot select work. |
| E: dirty working tree | Stop before selection; no destructive recovery. |
| F: low-risk isolated CRUD | Deterministic checks and lightweight review; Luna/low. |
| G: authorization/payment/child data | Enforced risk floor, independent deep review and Astra/high or xhigh. |
| H: unexpected context | Targeted expansion requires a named reason; no silent truncation or scope expansion. |

Closed unmerged claims block the affected chunk until human disposition; exact marker
parsing and the documented retry path are tested. Named frontend contracts and expanded
service method contracts remain accessible without loading full catalogs.

## Validation and independent review

- Workflow suite: 56/56 PASS, including existing remote merge/evidence regressions.
- Plan/bootstrap, graph, routing metadata and whitespace checks: PASS.
- Six edited workflow skills: bundled skill validator PASS.
- Independent reviewer: workflow_optimisation_review, final PASS; three material
  findings fixed and covered by regression tests; no Critical/High findings remain.
- Root AGENTS: 1,664 bytes versus 4,846 previously (66% reduction).
- First-chunk startup packet: approximately 4,500 tokens using UTF-8 bytes/4, including
  router, repository identity, cache/current handoff, manifest, routing output and
  execution instructions/skills. Contract/source reads count toward its 12,000-token
  cumulative budget. These are estimates, not measured tokenizer consumption.

## Approval provenance

Bootstrap PR #1 was human-merged at e6818689ce23526165c4fe99a8899e9d5641891e
before its actual PR number was recorded in scope-lock.json. Therefore existing
reconciliation correctly remains DRAFT. This workflow PR becomes the new reviewed
approval pointer with refreshed witnesses; PR #1 remains recorded as product baseline.
Record the actual workflow PR number before human merge. No fabricated approval,
self-reported LOCKED flag, product completion or direct master commit is used.
