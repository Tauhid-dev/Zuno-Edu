# Zuno Edu product definition

Status: DRAFT. Scope candidate 1.0; architecture candidate 1.0. This is the complete defined launch baseline, not an MVP. No product functionality is implemented by this bootstrap.

Zuno Edu is an Australian online education business helping school-age children learn AI and related technology through instructor-led courses. The service combines reusable curriculum, scheduled cohort delivery, a focused student learning environment, family purchasing and visibility, teaching operations and authorized business administration.

Five surfaces share one authoritative backend, domain model, PostgreSQL database and authorization model: Public Website, Parent Portal, Student LMS, Teacher Portal and Admin Portal. A portal is a presentation and access context, not a separate database or system of record.

The Public Website helps a family understand the business, age suitability, outcomes, schedule and total price. A verified parent establishes a family, registers the minimum child profile, selects a suitable cohort and pays the published upfront fee. The child follows Learn → Attend / Watch → Try → Build → Submit → Review / Reflect. The assigned teacher delivers live classes, records attendance, assesses work and releases feedback. Administrators operate curriculum, delivery, accounts, communications, commercial records and infrastructure through explicit privileges.

The launch outcome is an operating education platform with secure child-data boundaries, reliable payments and live-class logistics, recoverable infrastructure and complete verified learning journeys. The outcome is not reached solely by merging every feature PR: the production launch gate also requires live integration readiness, restoration evidence and approved human business/legal decisions.

## Binding product decisions

| Concern | Proposed launch decision | Reason |
|---|---|---|
| Purchase | One child, one cohort, one upfront AUD card payment through Stripe Checkout | Clear entitlements and reconciliation without complex billing |
| Pricing | Course default fee, explicit cohort override; immutable order snapshot | Offers can change without rewriting historical purchases |
| Family | Parent account creates one family membership; authorized guardian-child links are explicit, verified and revocable | Multiple children and guardians without discovery of unrelated people |
| Student identity | Required first/display name and numeric age-as-of; optional last/preferred name and school; guardian-provisioned credentials | Meets educational need without requiring child email or DOB |
| Curriculum | Reusable Course with immutable published revisions; Cohort pins a revision | New deliveries do not duplicate curriculum or change prior work |
| Learning media | Structured content, resources and approved video; no class recordings by default | Focused learning with controlled child exposure |
| Assessment | Single-/multiple-choice formative quizzes; assignments/project files assessed against a rubric | Covers the defined instructor-led teaching lifecycle |
| Completion | All required items plus ≥80% attendance at delivered sessions, or evidenced education-admin override | Reproducible certificate eligibility |
| Recognition | Course-completion achievement represented by completion state and certificate | Avoids an unapproved gamification system |
| Scheduling | Finite weekly recurrence materialized as individual sessions; teacher changes require assignment, ≥24h notice and no conflicts | Local exception control with authoritative schedule |
| Live delivery | Zoom through a port, just-in-time start/join authorization, waiting room, no join-before-host, recording off | Teaching logistics with controlled credentials |
| Calendar | Dedicated Google Calendar mirror plus authorized ICS export | Convenient schedules without a second domain authority |
| Communications | Resend adult transactional email plus role-scoped in-app notifications | Reliable notices without child marketing or private messaging |
| Storage | Private S3-compatible objects, quarantined validation, metadata in PostgreSQL | Safe learning and submission files |
| Privileges | Identity, education, finance, operations and audit admin capabilities; Teacher principal incompatible with finance grants | Prevents teacher financial access through additive roles |

Every behavior is specified by a stable requirement in `requirements.json`. Product files define approved scope; architecture files define how that scope is fulfilled. Decisions above are proposed for explicit human review and must not be silently altered during implementation.
