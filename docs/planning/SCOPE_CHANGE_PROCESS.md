# Scope and architecture change control

During initial DRAFT planning, design may be improved within the user's required
product, technology, security and workflow boundaries. Record material decisions.
After the human merges the planning PR, the resulting baseline is locked. Neither a
difficult chunk, an agent's preference, nor an “MVP” interpretation authorizes change.

A change begins only with explicit human instruction identifying the scope being
changed. Capture the exact instruction or durable reference, the requester and the
requirements affected in a change proposal on a separate feature branch. Do not edit
master, implement the proposed product change, or infer consent from an unanswered
question. Work unaffected by a concrete blocker can continue through normal selection.

The proposal must state:

- Current approved behavior and proposed behavior, including additions, removals,
  replacements or postponements; identify any launch requirement being changed.
- Business reason and the demonstrated constraint. Distinguish an implementation
  defect from a design impossibility; document considered compatible fixes.
- Requirement IDs and impact on domain objects, services/ports, APIs, frontend mapping,
  authorization/child data, integrations, infrastructure, operations and tests.
- Revised acceptance criteria, traceability, dependency graph and chunk ownership;
  migration/backward compatibility, recovery and rollout impact where relevant.
- Scope/architecture versions, affected ADRs, immutable approval witnesses and the
  later implementation chunks needed. No hidden work can enter an unrelated chunk.

Independently review exact coverage, scope creep/erosion, architectural consistency,
authorization and operational risks. Resolve Critical/High findings. Recompute plan
witnesses and set the proposed lock record DRAFT with the new proposal PR number and
new version. The proposal PR may change authoritative planning documents; it must not
bundle implementation of its unapproved new scope. Run full planning validation.

The human reviews and merges the proposal into master if approved. That identified
human merge becomes the new approval evidence under the same reconciliation protocol.
The next fresh session synchronizes, verifies that merge and its plan witnesses, and
only then implements an eligible chunk against the new baseline. Preserve prior
version/decision references so the reason for the change remains auditable.

A pure architecture correction that changes no requirements still needs a reviewed
ADR, updated blueprint/contracts/mappings, impact analysis and architecture-version
increment before dependent implementation. If it changes locked behavior or weakens a
boundary, it is a scope change and needs explicit human scope-change instruction.

If the design cannot work, stop only the affected chunk, record the conflict and
proposed remedies, and report the exact decision needed. Never silently remove,
simplify, defer, broaden permissions, substitute partial functionality, or redesign
the agreed object model while calling the chunk complete.
