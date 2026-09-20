# Scope lock

STATUS: DRAFT
SCOPE_VERSION: 1.0
ARCHITECTURE_VERSION: 1
APPROVAL_EVIDENCE: none

This document does not claim that a human has approved or merged the bootstrap plan. The proposed complete launch baseline consists of `LAUNCH_SCOPE.md`, `OUT_OF_SCOPE.md`, the 219 stable required records in `requirements.json`, and the functional/non-functional requirement documents. No product feature is implemented during bootstrap.

## Authority

After approval, authority is: scope lock/launch scope; functional and non-functional requirements; accepted ADRs; Code Blueprint; detailed architecture; API/frontend-backend contracts; selected chunk manifest; engineering skills/standards; existing implementation; conversational assumptions. New explicit human instruction that identifies a scope change enters the formal change process below. A casual implementation suggestion, inconvenience or assumed MVP tradeoff cannot silently amend locked requirements.

## Activation after human review

The human reviews the planning/bootstrap PR, including product scope, exclusions, all human production gates, OOP/backend design, contracts/frontend mapping, security, chunk plan and deterministic state workflow. The human-approved merge into remote `master` is the approval event. The read-only reconciler verifies the identified planning PR, human merge, reachable merge commit and immutable plan witnesses from scope-lock.json. It reports effective `LOCKED` even when the approved file still says DRAFT; the next feature branch persists status and actual merge evidence. Do not infer approval merely from a local branch, commit, review report or an agent statement.

A DRAFT marker alone is not a blocker after verified human merge. Missing, mismatched or unverifiable merge evidence stops `next chunk` before product implementation. Reconciliation never modifies master and never assumes approval from a local file. Production human gates are separate from architecture approval: approved code can be implemented while live checkout/publication stays disabled pending real business/legal configuration.

## Formal scope and architecture change

1. Require explicit human instruction identifying the intended scope change, affected requirement IDs and reason. An implementation impossibility can be reported without granting permission to redesign.
2. Stop the affected chunk; preserve unrelated safe work and record the specific conflict, evidence and blocked dependencies. Never silently drop or weaken the requirement.
3. Draft a change proposal on a new feature branch from synchronized remote master. Include current behavior, requested behavior, alternatives, authorization/data impact, costs/risks, migration/rollback implications and changed acceptance criteria.
4. Update requirement inventory without renumbering/reusing IDs; mark any approved replacement relationship explicitly. Update launch/out-of-scope docs, ADRs, object/service/port contracts, API/frontend mapping, tests, affected chunks/dependencies and traceability together.
5. Obtain independent product/architecture/security review proportionate to the change and resolve Critical/High findings. Revalidate complete coverage and deterministic selection.
6. Open a PR targeting master for human review. Only the human normally merges remotely. Increment scope version for changed approved behavior and architecture version for material blueprint changes; record actual approval evidence.
7. A fresh session synchronizes and reconciles remote master before the revised chunk proceeds. Existing feature branches never become substitute authority for unmerged scope.

## Immutable implementation constraints

One selected chunk per session; synchronized remote master baseline; no dependent work on an unmerged branch; no master mutations during reconciliation; PR_OPEN is not COMPLETE; risk-appropriate review (independent deep review for high/critical risk) and required tests; no financial teacher privilege; no cross-family/student leakage; no provider details in domain entities; no opportunistic refactoring or future functionality; human PR-only handoff; stop after handoff.
