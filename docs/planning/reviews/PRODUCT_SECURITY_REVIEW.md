# Independent product and integration security review

Reviewer: independent workflow/bootstrap agent reviewing product and integration work
authored by other agents. Date: 2026-09-11. This review does not self-approve the
workflow code authored by this reviewer, and does not approve scope for the human.

## Reviewed evidence

- Original launch request and all 219 canonical requirement records in
  `docs/product/requirements.json`, including each role surface and acceptance rules.
- PRODUCT_DEFINITION, LAUNCH_SCOPE, OUT_OF_SCOPE, FUTURE_CONSIDERATIONS, functional and
  non-functional requirement renderings.
- BILLING_ARCHITECTURE, LIVE_CLASS_ARCHITECTURE, CALENDAR_ARCHITECTURE,
  COMMUNICATION_ARCHITECTURE, FILE_STORAGE_ARCHITECTURE, INTEGRATIONS,
  DEPLOYMENT_ARCHITECTURE and business/external consistency ADRs.

This is a planning review, not executed product/security testing. No application
features exist. Detailed backend/OOP, API contract and frontend mapping reviews are
separate reviews and must be completed before claiming the full blueprint passed.

## Findings and remediation

| ID | Severity | Finding and concrete impact | Status / evidence |
|---|---|---|---|
| PS-01 | High | CLS-008/LAUNCH_SCOPE allowed student join from -15 minutes to session end and teacher start from -30 minutes to end; LIVE_CLASS_ARCHITECTURE initially gave both -15 minutes through end+30. Implementers would ship inconsistent privilege windows. | RESOLVED: LIVE_CLASS_ARCHITECTURE now explicitly uses the same role-specific windows as CLS-008 and LAUNCH_SCOPE. Rechecked after owner correction. |
| PS-02 | High | Billing initially automatically queued a full refund for late payment without a seat, while ENR-003/007 offered admin allocation or refund. No serialized winner prevented seat activation from racing the refund. | RESOLVED: BILLING_ARCHITECTURE checkout step 5 now records PAID_EXCEPTION and one locked, idempotent ALLOCATE/REFUND choice; allocation locks capacity and rejects pending/succeeded refund; refund reservation prevents activation and competing decisions return 409. Rechecked after owner correction. |
| PS-03 | Medium | File allowlists/size policies disagreed between LAUNCH_SCOPE/FILE-002 and FILE_STORAGE_ARCHITECTURE: MB versus MiB; aggregate submission cap absent initially; curriculum 25 versus 50; WebP absent from architecture; certificate 10 versus 5. This produced contradictory validators/UI guidance. | RESOLVED: rechecked LAUNCH_SCOPE and FILE_STORAGE_ARCHITECTURE: student 25 MiB/file and 100 MiB/submission, curriculum PDF/PNG/JPEG/TXT 50 MiB, MP4 500 MiB, internal 25 MiB and generated certificates 5 MiB agree. Product now states exact byte values and architecture enforces aggregate submission bytes transactionally. |

No Critical findings identified. High findings remaining in this review: 0.
Medium findings remaining: 0. Low findings remaining: 0.

## Positive conclusions supported by the plan

The required public, parent, student, teacher and admin surfaces are represented with
explicit scope and exclusions. Course, cohort and class-session meanings remain
distinct; reusable curriculum and instructor-led learning are retained. Billing,
refunds, receipts/reconciliation, all required provider integrations, operational
recovery and final launch acceptance are present rather than deferred as MVP extras.

Parent child access and billing-family membership are separate checks (AUTH-007,
PAR-017/018); guardian authority alone cannot reveal another family's finances.
Teacher finance denial is explicit across API/service/query and frontend requirements
(TCH-016, AUTH-009/012), including additive-role protection (AUTH-010, ADM-006).
Student data projections exclude finance/family administration, peers and drafts.
Child first/display name and numeric age are required; school, last/preferred name
are optional, no DOB/email is required, and stale age reconfirmation is bounded.

Transactional failure design includes server-verified payment outcomes, durable
inbox/outbox, idempotency request hashes, last-seat locks, immutable monetary snapshots,
refund reservations, provider ambiguity quarantine, desired-version reconciliation,
schedule tombstones and no browser-redirect activation. Child payloads are minimized
for Zoom/Calendar/email. Private file promotion binds verified bytes to immutable
objects and recognizes the finite revocation limitation of presigned URLs.

Production approval of legal texts, merchant/tax settings, course age bands, staff and
provider accounts remains an explicit human gate. It is correctly distinct from
software omission; no approval or live validation is claimed by this review.

## Required downstream verification

Implementation must prove the negative role/resource cases and concurrent provider
failure cases named in requirements and architecture. In particular: teacher finance
denial through additive roles; revoked guardian/teacher links; cross-family billing;
forged redirects and webhook replay; last-seat and ALLOCATE/REFUND races; stale
schedule jobs after cancellation; and post-scan upload replacement. This planning
review does not substitute for those tests, live provider checks or human scope review.
