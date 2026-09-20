---
name: memory-maintenance
description: Maintain compact Zuno Edu operational memory during chunk work and handoff; not duplicate authoritative design documents.
---

# Compact current state

Load AGENT_WORKFLOW.md#Handoff, the fresh reconciliation result and current chunk. Update the existing progress.json cache on the feature branch only; retain confirmed remote completions, master SHA, active PR and blockers. Never complete unmerged work or trust stale handoff/state over remote evidence.

Replace CURRENT_HANDOFF.md in ≤250 words with required fields and exact next references/model/reasoning. Keep PROJECT_STATE compact. Archive the per-chunk handoff under existing memory/handoffs/; never load that history normally or mutate hashed completion evidence. No duplicate state tree, execution diary or vector memory. Run next_chunk.py --validate.
