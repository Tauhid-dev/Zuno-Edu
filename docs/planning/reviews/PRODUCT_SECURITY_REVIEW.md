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


## Final independent consistency recheck — 2026-09-13

Final status: **PASS**. PS-01 through PS-06 are closed. Critical, High and material Medium findings remaining in this product/security review: **0**.

Final reviewer: product_inventory review agent, independently reviewing backend/security/integration work authored by other agents. This agent authored the product requirements and therefore does not replace the initial independent product-completeness review above. It independently checked the later architecture against that approved-for-review product inventory and verified the corrections below.

The recheck covered canonical requirements and LAUNCH_SCOPE, backend-catalog, SECURITY_ARCHITECTURE, AUTHORIZATION_MODEL, DATA_ACCESS_BOUNDARIES, PERMISSION_MATRIX, SETTINGS_CATALOG, billing/file integration documents and the new generated-document/financial-export chain. The prior PS-01–03 resolutions remain consistent: live join/start windows retain their exact role limits; late paid exceptions use serialized explicit allocation/refund; file purpose limits use the same MiB values and aggregate cap.

| ID | Original severity | Finding | Final closure evidence |
|---|---|---|---|
| PS-04 | High | Newly rendered security prose and scanner contract permitted larger ZIP expansion/entry/nesting limits than launch scope. | MalwareScanner canonical port and rendered security/file rules now require at most100MiB expanded,100entries,ratio20:1 and no nested archives. Executable/encrypted/traversal payloads are rejected and scanner failure remains closed. This restores LAUNCH_SCOPE consistency. |
| PS-05 | Medium | Security prose changed parent/student session lifetime and reset/contact/checkout limits relative to AUTH-003 and SEC-006. | Security architecture now uses staff idle30minutes,parent/student idle12hours,absolute7days; login5attempts/minute per identity,reset3/hour,contact5/hour,checkout10/hour/billing-family. These agree with the canonical requirement acceptance criteria. |
| PS-06 | Medium | Architecture used alternate human-gate labels and did not explicitly preserve staff approval in activation checks. | Canonical setting entries now use HG-MERCHANT and HG-PROVIDERS. Enrolment activation requires HG-LEGAL+HG-MERCHANT+HG-AGE+HG-PROVIDERS+HG-STAFF and passing launch evidence. Public publication requires HG-LEGAL+HG-AGE+HG-STAFF. SETTINGS_CATALOG explicitly maps historical aliases to the canonical gates, and AUTHORIZATION_MODEL requires HG-STAFF for production staff activation. A composite launch label cannot bypass any canonical approval. |

### Generated artifact and finance boundary conclusions

Generated receipt PDFs and financial CSVs have dedicated financial_document/financial_export purposes. Trusted workers write bounded bytes through ObjectStorageProvider.write_generated with immutable-key,checksum,size,retry and orphan-handling rules. Generic file metadata/download/delete paths reject financial purposes; financial-specific BillingService/ReportingService operations recheck billing-family membership or finance-admin requester/oversight scope. A teacher/learner/education-admin role cannot acquire financial grants by accessing a generic file ID or generated artifact.

Financial export status is readable by its authorized finance requester/oversight in every defined state. Download requires ready,unexpired state and a short-lived grant. Terminal generation failure exposes only a sanitized failure code; provider details and file content stay private. Revocation/expiry and retries do not create a persistent public link. Parent access to purchase documents remains based on independent billing membership rather than guardian relationship alone.

The typed setting catalogue rejects unlisted keys and mismatched value shapes. Secret material remains outside settings/API responses. Real human/legal/merchant/provider/staff decisions remain production gates, not fabricated approvals or missing launch implementation. The reviewed controls require role,resource relationship,ownership and state at API/application/query levels.

This is a final planning consistency/security review, not an executed penetration test or proof of live provider/production readiness. Required negative authorization,concurrency,malicious-upload,session/MFA and production checks remain implementation/launch gates. No application feature was implemented in this review.

Backend catalogue SHA-256 at this final consistency recheck: `61dddc7d3660fcc5ca50731b166e7c2187f5039dc233479a10065d4ea9ea9a31`.


## Final least-privilege contract addendum — 2026-09-20

Status: **PASS**. Reviewer: final_reviewer, independent of the correction authors. Unresolved Critical/High/Medium findings for this bounded security recheck: **0**. Reviewed backend catalog SHA-256: `a0025e16226e89d2460b4afb257aa6f41b5c088f8bf95d1122a5325cd3aba80b`; frontend catalog SHA-256: `4ee178ea7fafd96ad082969e7201f343331858b5e023ec97fc5f4b5405549f4b`.

The final frontend-read corrections were rechecked at the API, service, repository projection and frontend binding boundaries. Identity-only account/family/retention projections do not expose financial amounts, credentials, MFA secrets or file content. Finance price-target lookup returns course/cohort naming and lifecycle context without curriculum, learner or identity-directory access. Education learner lookup remains cohort-scoped and excludes contact/family/financial data. Parents do not inherit the new admin family relationship projection, and teachers/students do not inherit any financial operations through component reuse.

Mutation preconditions now come from their actual owning resources. Retention hold absence is distinct from the target's version, and hold changes serialize with purge. Guardian links and billing membership remain independent. Completion override history/evidence is education-admin-only and same-enrolment; source learning evidence is unchanged. First attendance/assessment/closure creation requires authorized absence and atomic conditional creation, while inaccessible resources never produce a permissive absence result.

Login and invitation MFA setup use the same purpose-bound limited context, with no full-session prerequisite or portal access before verification. The last active identity administrator cannot be lost through concurrent suspension/grant removal. Upload context is purpose-specific and rechecked against current ownership, privilege and lifecycle; standalone admin asset creation is limited to permitted internal/public assets. Generic file routes continue to reject generated finance purposes.

Public schedule rendering uses only the public DTO branch. Download reuse accepts a freshly issued ticket or an authorized issued URL without manufacturing metadata or introducing a financial client into shared components. Signed links and setup tokens remain transient. The independent mapping check found no authorization drift in 540 mappings and no financial component in the transitive teacher/student composition graph.

This is a contract/security design recheck, not a penetration test or proof of application enforcement. The affected manifests require the corresponding role-denial, stale-token, concurrent-first-write, upload-race, limited-MFA and projection-field tests during implementation; live approval and launch evidence remain separate gates.
