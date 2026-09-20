---
name: git-workflow
description: Perform Zuno Edu branch, commit and PR workflow for a bounded chunk; not general repository repair or permission to merge.
---

# Repository workflow

Use configured origin/master and AGENTS startup. Clean worktree, fetch, checkout integration branch, fast-forward pull, then fresh reconciliation. Stop on dirt/divergence/failure without destructive repair.

One feature branch from verified master; no unmerged dependency base or direct master commits. Use the selected chunk's ID in commit subjects. Run required checks and risk-based review, push and create/update the PR targeting master. Record actual PR number, verify final changes and STOP. Human merge only; an obsolete local feature branch never outranks remote evidence.
