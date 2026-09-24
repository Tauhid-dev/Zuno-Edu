# ADR 0004 independent review

Risk: critical. Depth: deep. Independent: true.
Reviewer: /root/contract_review, separate agent, no proposal authorship or file edits.
Date: 2026-09-24. Final disposition: approved for planning PR, not execution.

The earlier review was interrupted by account usage limits and was not approval.
The resumed review inspected ADR 0004, the final canonical MFA service/API/schema,
MfaRepository and idempotency table contracts, generated catalog sections and
StaffMfaSetup retry behavior. It confirmed compatibility with the existing table
plan (simultaneous active and pending factors are possible).

Resolved findings: pending-factor selection and invalidation were missing from
the port; factor row locks alone cannot serialize first enrolment; pending proof
must follow the exact browser-bound challenge.factor_id; the keyed request digest
needs format/key-version encoding for rotation. The reviewed correction now uses
the shared Account row lock and authorization recheck, active-only lookup, scoped
exact pending lookup, pending factor/credential invalidation, active/recovery
preservation, versioned keyed metadata and NULL secret response ciphertext.

Final reviewer conclusion: no remaining High/Medium finding; one-time provisioning
and explicit restart semantics are consistent across the reviewed contracts.
Open findings: Critical 0, High 0, Medium 0, Low 0 reported.
Runtime race/security tests remain mandatory in the implementation chunks after
human merge. Plan witness hashes cover the exact authority files; this review
record makes no implementation completion claim.
