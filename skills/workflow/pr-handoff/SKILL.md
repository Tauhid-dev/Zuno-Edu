---
name: pr-handoff
description: Prepare the final Zuno Edu chunk PR and bounded human handoff after implementation/review; not start a new chunk or merge.
---

# Pr Handoff

## Required context

Read active chunk, completion-evidence protocol, final diff/checks, independent review and .github/pull_request_template.md.

## Rules

Include exact requirement IDs, objective, implemented/not-changed scope, authorization/architecture impact, checks, acceptance proof, review findings, PR_OPEN state, base master SHA and human action.

## Implementation standards

Create hashed implementation/test/review witnesses and canonical completion manifest. Push feature branch and open PR against master with exact full-line ZUNO_EDU_CHUNK:<ID>. Add actual PR number in a final feature commit when necessary.

## Verification

Confirm all required checks and independent review cover the final diff and no Critical/High remains. Human action is: Review and merge into master if approved. Report blockers honestly, including absent credentials/remote.

## Common failures

Failure signals: declaring COMPLETE, missing PR identifier, hash self-reference, unverified final changes, hiding missing checks, automatic merge or beginning another chunk.

See [the repository constitution](../../../AGENTS.md) and [state protocol](../../../docs/planning/STATE_RECONCILIATION.md) for shared authority. Do not load unrelated skills.
