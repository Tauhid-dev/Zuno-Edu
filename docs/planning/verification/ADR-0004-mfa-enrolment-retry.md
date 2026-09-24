# ADR 0004 planning verification

Date: 2026-09-24. Planning-only proposal; no application implementation is
authorized by this branch.

The original C01 contract conflict was independently identified: the enrolment
request promised same-result replay for seven days, while the response contains a
provisioning URI that security requires to be returned once. The proposed ADR
chooses a secret-free `409 MFA_REPLAY` after commit, explicit user restart after a
lost response, and no replayable secret cache.

The independent security review also found that preserving an active factor while
replacing pending setup state requires account-scoped repository operations. ADR
0004 therefore adds `get_pending_factor_for_update(account_id, setup_token_hash,
browser_hash, scope)` and `invalidate_pending_setup(account_id, scope)` to `MfaRepository`.
Both are row-locking, scoped, and forbidden from returning or changing active
factor material. The existing active-factor lookup is explicitly active-only.

Validated on the proposal worktree:

- `scripts/update_scope_witnesses.py`: PASS, 114 witnesses, DRAFT only.
- `scripts/validate_plan.py`: PASS, 219 requirements, 62 chunks.
- `scripts/next_chunk.py --validate`: PASS.
- `scripts/reconcile_state.py --validate-plan`: PASS, execution unauthorized
  while scope is DRAFT.
- `git diff --check`: PASS.

The initial Windows workflow run failed 13 tests and errored once because fixture
files were hashed with CRLF but Git committed LF. A fresh run uses process-local
GIT_CONFIG_COUNT=1, GIT_CONFIG_KEY_0=core.autocrlf, GIT_CONFIG_VALUE_0=false so
fixture byte witnesses and committed bytes agree; no global Git setting or test
assertion is changed. The rerun PASSED all 61 tests in 315.156 seconds.
The catalog renderers now write explicit UTF-8/LF and obtain version labels from
the proposed lock, making their output reproducible across Windows and Linux.
Final independent critical-risk deep review by /root/contract_review approved
the planning correction with no remaining High/Medium findings. See the review
record in memory/handoffs/ADR-0004-review.md.
No product tests, completion evidence, implementation PR or merge claim is made.

All 114 witnesses were separately checked against actual staged Git blob bytes
before commit, with zero mismatches. The planning commit was pushed successfully.
PR creation through the GitHub connector returned HTTP 403 (Resource not accessible
by integration). Automatic approval review rejected opening GitHub's browser UI
as an alternate publishing route. No PR was created and no CI run is claimed.
The planning_pr remains null until an authorized PR is created; recording its real
number and checking the final committed witnesses remain required before handoff
for merge. Branch: feature/mfa-enrolment-retry-contract, base
f1f18fbd0e77bd305cd71d1ca6aa2d17d773bad3.
