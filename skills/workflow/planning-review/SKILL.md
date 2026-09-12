---
name: planning-review
description: Independently review Zuno Edu bootstrap or formally revised launch planning; not implement the product or approve scope for the human.
---

# Planning Review

## Required context

Read the relevant product requirements, architecture/blueprint, contracts/mappings, chunk plan and authority files. Focus context on the assigned review dimension.

## Rules

Check complete launch coverage, explicit exclusions, bounded backend-first OOP design, service/repository/port responsibilities, consistent frontend mapping, role/ownership boundaries and dependency viability.

## Implementation standards

Record evidence-backed Critical/High/Medium/Low findings with file references, concrete impact and proposed correction. Distinguish unresolved business blockers from planner-owned decisions. Never invent human approval.

## Verification

Verify every requirement has a chunk and each chunk has requirements, tests, acceptance criteria and required context/skills. Independently test fresh-session selection for workflow review. Recheck resolved Critical/High findings.

## Common failures

Failure signals: vague later-design promises, teacher finance exposure, missing child age/name, missing frontend contract, unavoidable linear dependencies, unverifiable remote state.

See [the repository constitution](../../../AGENTS.md) and [state protocol](../../../docs/planning/STATE_RECONCILIATION.md) for shared authority. Do not load unrelated skills.

