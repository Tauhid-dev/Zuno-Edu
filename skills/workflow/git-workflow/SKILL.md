---
name: git-workflow
description: Perform Zuno Edu branch, commit and PR workflow for a bounded chunk; not general repository repair or permission to merge.
---

# Git Workflow

## Required context

Read AGENTS.md, memory/repository.json, selected execution metadata and STATE_RECONCILIATION.md.

## Rules

Confirm configured origin and clean worktree; fetch origin, checkout master, pull --ff-only origin master. Stop on failure or divergence without destructive repair. Reconcile master read-only before branching.

## Implementation standards

Create feature/<chunk-id-lowercase>-<slug> from synchronized master. Use feat/fix/test/docs(CHUNK-ID) subjects. Never commit working changes directly on master, rebase others' work, or force-push by assumption.

## Verification

Verify final diff, required checks, independent review and correct master target. Push feature branch, create PR, record actual PR number with a follow-up feature commit, and ensure final review covers it.

## Common failures

Failure signals: missing origin, invented repository identity, dirty master, accidental default-branch edits, PR aimed at another branch, automatic merge.

See [the repository constitution](../../../AGENTS.md) and [state protocol](../../../docs/planning/STATE_RECONCILIATION.md) for shared authority. Do not load unrelated skills.
