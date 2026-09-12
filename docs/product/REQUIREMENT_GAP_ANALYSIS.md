# Requirement gap analysis

Status: DRAFT. Performed before frontend design and implementation decomposition. This report distinguishes resolved planning choices from external production decision gates; it does not certify backend review before that review occurs.

| Source ambiguity/risk | Resolved proposed launch behavior | Coverage |
|---|---|---|
| Student name/age shape | Required first/display name + numeric age_as_of; optional last/preferred/school; no DOB or child email | PAR-005; SEC-001–002; AUTH-005 |
| Multiple children/guardians | Explicit revocable GuardianStudent and separate billing-family membership, verified admin-assisted linking | PAR-006; AUTH-007; ADM-004 |
| Course/cohort/session conflation | Reusable immutable course revision, independent cohort and individual scheduled session | LRN-001–004; CLS-001–004 |
| Billing mode | One upfront AUD card payment per child/cohort; no subscriptions/instalments/discounts/cart | PAY-001–003; OUT_OF_SCOPE |
| Capacity race/late payment | Transactional 30-minute seat hold; verified payment activates once or becomes paid exception without oversell | ENR-001–007; PAY-004–006 |
| Refund/access ambiguity | Financial refund and educational entitlement disposition are separate explicit decisions | PAY-008, PAY-011 |
| Parent scheduling | Schedule view and notices; support contact rather than unrestricted schedule mutation | PAR-009; WEB-009 |
| Teacher rescheduling | Assigned future session, ≥24h both ends, preserve duration, conflicts for cohort/teacher/learner | TCH-005; CLS-003, CLS-011 |
| Teacher finance loophole | No Teacher finance APIs/services/query scope; incompatible additive finance role rejected | TCH-016; AUTH-009–010; ADM-006 |
| Learning release/progress | Pin course version; release gates; required-item progress and explicit completion/attendance policy | LRN-004, LRN-006–010 |
| Quiz and assignment semantics | Exact-match choice quiz; bounded attempts/pass threshold; immutable work versions; late-label/return workflow | ASM-001–008 |
| Achievement scope | Course completion certificate only | STU-017; LRN-009–010 |
| Video/live recordings | Approved learning media; Zoom recording disabled at launch | LRN-005; CLS-008 |
| Calendar authority | Domain session is authoritative; one mirrored external event per occurrence; optional authenticated ICS | CAL-001–005 |
| Communications | Durable background intents; mandatory service notices; adult email and student in-app | COM-001–009 |
| File validation | Purpose-specific allowlists, limits, archive scanning, private grants and retention | FILE-001–007; LAUNCH_SCOPE |
| Policy/legal/tax uncertainty | Typed versioned approval gates block production use, with complete technical contracts | PAY-012; SEC-003; HG-LEGAL/HG-MERCHANT |
| Operational completeness | Containers/HTTPS/migrations/CI/staging/observability/backups/proven restore/runbooks/launch gate | OPS-001–015; NFR-001–012 |
| Scope erosion during implementation | Stable all-required inventory, traceability, locked blueprint and explicit change process | NFR-009–011; SCOPE_LOCK |

Every source launch surface and lifecycle is represented in the canonical 219 requirements. Mapping those requirements to objects, services, contracts, frontend consumers, chunks and evidence remains a mandatory downstream check. This inventory does not permit a coarse requirement-to-chunk link to substitute for complete operation/schema design.

The unresolved human decisions are HG-LEGAL, HG-MERCHANT, HG-AGE, HG-PROVIDERS and HG-STAFF. These are explicit production blockers with named owners and blocking behavior, not unspecified implementation architecture. The repository/Git remote and real human merge evidence are workflow prerequisites outside product capability design.
