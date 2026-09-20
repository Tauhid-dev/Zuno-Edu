---
name: state-reconciliation
description: Recompute effective Zuno Edu scope and chunk status from fresh remote master; use before selection, not to trust a cached handoff.
---

# Evidence exception handling

Normal startup runs next_chunk.py without loading this skill. Load it and only the relevant STATE_RECONCILIATION section when synchronization/evidence is inconsistent or when changing the workflow.

Fresh remote master, live official GitHub PR evidence and immutable witnesses outrank caches/handoffs. Preserve before/after remote-tip checks, exact origin, clean master and dependency proofs. Network/access/rate errors stop selection. Closed-unmerged PRs require resolution; stale handoffs never reserve or complete work. Persist safe metadata corrections only on the selected feature branch. Never repair via reset/discard/force push or offline approval bypass. Test changes using isolated Git repositories.
