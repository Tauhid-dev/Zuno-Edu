# Zuno Edu — next chunk

One chunk per context; human PR merge only. No product work during DRAFT.
Preserve approved scope, architecture, contracts and permissions.

1. Inspect `git status --porcelain=v1` and `memory/repository.json`. Stop for
   uncommitted work, missing identity, wrong origin or failed/diverged sync.
   Never reset, stash, discard or rebase another person's work.
2. Fetch origin, check out the configured integration branch (`master`), and pull
   with `--ff-only`. Use actual configured names; do not assume main or branch
   from an unmerged PR.
3. Run `python3 scripts/next_chunk.py` on synchronized master. Only READY plus
   `execution_authorized: true` permits implementation; previews/handoffs do not.
4. Read the returned manifest and relevant `memory/CURRENT_HANDOFF.md`. Load only
   the packet's execution instructions, selected skills, targeted contract entries
   and source paths. Use its context reader; never open entire catalogs by default.
5. Create `feature/<chunk-id-lowercase>-<slug>` from the verified master SHA.
   Implement one chunk, run its checks, apply its review depth, then load its
   handoff instructions. Record PR_OPEN and a conditional next model recommendation;
   push/open the PR and STOP. Only the human merges.

Router: `docs/planning/workflow-routing.json`. Compact state:
`memory/progress.json` (cache only; verified remote merges win). Detailed policies:
sections of `docs/planning/AGENT_WORKFLOW.md`, loaded by phase. Evidence protocol:
`docs/planning/STATE_RECONCILIATION.md`, needed for reconciliation issues/handoff.
Historical `memory/handoffs/` is audit-only, never normal startup context.
