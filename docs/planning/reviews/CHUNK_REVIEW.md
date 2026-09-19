# Independent chunk plan review

Date: 2026-09-14. Reviewer: workflow agent independently reviewing the root agent's
generated chunk plan, bindings, manifests and traceability. This is a planning review;
it does not claim that application features or their future tests are implemented.

Result: PASS for human planning review. Unresolved findings: Critical 0, High 0,
Medium 0, Low 0. Human scope approval remains a separate remote merge event.

## Evidence inspected

Reviewed all 62 records in [chunks.json](../chunks.json), their Markdown manifests,
[Code Blueprint](../../architecture/CODE_BLUEPRINT.md), requirement traceability,
the 313-operation backend catalog and the 110-component/101-route frontend catalog.
Checked objectives, lifecycle responsibilities, exact operation owners, prerequisites,
component composition/reuse, required context/skills, acceptance criteria, required
tests and the final launch gate. Reviewed the original 59/60-chunk definitions before
binding and rechecked the final generated files after the corrections below.

Independent cross-checks on the final artifacts found:

- All 219 required launch IDs are served; no unknown or orphan requirement ID appears.
- Every backend/API/worker operation has one named implementation owner and occurs
  in that owner's manifest. A frontend consumer lists its operation without becoming
  a second backend implementation owner.
- Every consumed operation's implementation owner is the consumer chunk or a verified
  transitive prerequisite. Every reused component's owner is the same chunk or a
  prerequisite. No undeclared component composition name or composition cycle exists.
- All chunk dependencies resolve; the graph is acyclic. The final gate reaches all
  61 other chunks. The end-to-end verification gate includes both parent checkout
  and complete notification producer wiring as prerequisites.
- All manifest frontmatter agrees with the canonical registry. Every declared
  required/optional skill and required context file exists. Every chunk has a bounded
  objective, acceptance criteria, required tests and an explicit PR-only handoff.
- The 111 mandatory scope witnesses cover current authority files and match their
  required raw/normalized digests. State fields can change without removing protection
  from chunk acceptance text, dependencies or scope/architecture versions.
- Teacher/student component composition has no finance/payment/refund/invoice
  component dependency. This supports the planned import boundary; implementation
  still requires the specified API, service, repository and frontend denial tests.

## Findings and verified corrections

| ID | Severity | Finding | Final correction and evidence |
|---|---|---|---|
| CH-01 | High | The launch gate required every chunk, including itself, to be effectively COMPLETE before its own PR_OPEN handoff. This was impossible under the human-merge workflow. | [ZE-P12-C07](../chunks/ZE-P12-C07.md) now requires all other chunks complete; its own passing verification/review is handed off PR_OPEN and becomes COMPLETE only after human merge. |
| CH-02 | Medium | One integration chunk mixed private export/retention with wiring every notification producer, two independently reviewable responsibilities. | [ZE-P08-C04](../chunks/ZE-P08-C04.md) owns private export/retention integration; [ZE-P08-C05](../chunks/ZE-P08-C05.md) owns notification producer integration and corresponding replay/audience tests. |
| CH-03 | Medium | Storage scanning claimed aggregate submission-size tests before the SubmissionService ownership boundary existed. | [ZE-P04-C02](../chunks/ZE-P04-C02.md) tests individual file/archive limits; [ZE-P07-C03](../chunks/ZE-P07-C03.md) owns the combined 100 MiB transactional submission cap. |
| CH-04 | Medium | Parent checkout was unnecessarily held behind admin financial reporting, and teacher marking behind certificate generation. | [ZE-P10-C02](../chunks/ZE-P10-C02.md) depends on financial documents/refunds rather than reports; [ZE-P11-C02](../chunks/ZE-P11-C02.md) obtains progress/marking through actual contracts and reuse prerequisites without a certificate dependency. |
| CH-05 | Medium | The admin authoring chunk combined at least 46 public/catalogue/curriculum/assessment operations, eight block editors and distinct publication/definition lifecycles. | [ZE-P11-C04](../chunks/ZE-P11-C04.md), [ZE-P11-C09](../chunks/ZE-P11-C09.md) and [ZE-P11-C10](../chunks/ZE-P11-C10.md) separate public/catalogue, curriculum/resources and assessment definitions. Attempt oversight and delivery closure remain in their operational workspaces. Final count is 62 coherent chunks. |
| CH-06 | High | End-to-end purchase/class/email verification could become eligible while parent checkout or notification wiring still had an unmerged PR. The final gate alone depended on those missing producers. | [ZE-P12-C05](../chunks/ZE-P12-C05.md) now transitively requires ZE-P10-C02 and ZE-P08-C05 before integration/journey verification. Rechecked the generated graph after transitive reduction. |
| CH-07 | Medium | The curriculum chunk promised activity/lesson completion writes and replay tests, although the bound operations belonged to ProgressService in another chunk. | [ZE-P03-C03](../chunks/ZE-P03-C03.md) owns typed activity block definitions; [ZE-P07-C05](../chunks/ZE-P07-C05.md) explicitly owns activity/lesson writes, release/ownership checks and idempotent replay tests. |

## Granularity and execution assessment

The plan separates backend delivery from frontend consumption, keeps provider adapters
behind ports and gives shared components explicit owners. Larger authoring and privacy
integration responsibilities now have bounded review surfaces. Related lifecycle
operations remain together rather than becoming one chunk per CRUD verb. Dependency
reduction retains real ownership and reuse requirements without imposing phase-wide
completion gates. Higher numbered capability phases may be prerequisites of lower
numbered phases; deterministic sequence applies only after readiness is recomputed.

Cross-module implementation can use the documented ports for isolated tests while
another adapter is unfinished. Concrete notification/privacy wiring and full provider
journeys have explicit later owners; no unfinished path is declared production ready.
Future scope/architecture changes must update the relevant manifests and authority
witnesses through the approved process, rather than silently changing these boundaries.

## Validation results and limits

`python3 scripts/validate_plan.py --bootstrap` passed: 219 requirements, 12 phases,
62 chunks, 69 objects, 31 services, 34 ports, 313 API/worker operations, 460 schemas,
110 frontend components, 101 routes, 46 skills and 111 scope witnesses. Planned
requirement coverage is 100%; application implementation coverage remains 0%.

`python3 -m unittest discover -s tests/workflow -v` passed all 29 tests in 56.427 seconds,
including the full-repository fresh-session simulation. See the separate
[state validation addendum](STATE_VALIDATION_ADDENDUM.md) for the distinction between
test execution and independent workflow review. Actual production/provider tests,
human business gates and human planning approval remain future evidence, not claims
made by this bootstrap review.

## Final contract and dependency addendum — 2026-09-20

Result: PASS for human planning review. Reviewer: `planning_validation_review`,
independently inspecting the root author's final catalogs, plan synchronization tool,
chunk records/manifests and targeted acceptance additions. Remaining findings from
this review: Critical 0, High 0, Medium 0. These final counts supersede the earlier
catalog counts above: 321 API/worker operations, 486 schemas, 71 objects, 31 services,
34 ports, 110 frontend components, 100 routes, 540 route-specific mappings, 62 chunks
and 111 matching mandatory authority witnesses. All 219 launch requirements remain
planned, with no application implementation.

Independent checks re-established every implementation operation's named owner and
manifest membership, every frontend API and reused component's same-chunk or
transitive prerequisite, manifest/frontmatter agreement, context and skill existence,
acyclic chunk dependencies, and all-PLANNED execution metadata. The final gate still
reaches all other 61 chunks; provider journey verification still requires parent
checkout and notification producer integration. Teacher/student composition reaches
no financial operation. No second chunk is made eligible by an unmerged prerequisite.

The frontend review corrections have these explicit backend owners:

| Added read contract | Implementation chunk |
|---|---|
| Account selection and account detail | ZE-P02-C04 |
| Legal-hold targets and current hold state | ZE-P02-C05 |
| Draft/unpriced course/cohort price targets | ZE-P06-C01 |
| Education-only named cohort learners | ZE-P06-C02 |
| Current assignment delivery closure | ZE-P07-C02 |
| Completion override history and progress token | ZE-P07-C05 |

The affected manifests retain bounded responsibilities and now include concrete
tests for exact version/absence tokens, first-write races, least-data selectors,
purpose-bound upload contexts, last-administrator preservation and neutral MFA
setup. Their frontend consumers obtain these backend implementations through the
verified dependency graph. These remain required future tests, not executed product
acceptance evidence.

One Medium validation gap was found and closed: the previous validator checked
references but could accept an erased owner/prerequisite, a composition cycle, a
missing route-local mapping hidden by another route, or stale mapping request and
authorization fields. This reviewer authored the bounded assertions and eight
mutation tests in `validate_plan.py` and `test_plan_validation.py`; the root agent
independently reviewed those changes and reported no Critical, High or Medium
findings. This addendum does not claim independent self-review of those additions.

The plan synchronization tool was reviewed without changing its implementation and
executed twice against an isolated copy: both runs succeeded, and the second run
changed zero files. Independent execution of the final full suite passed all
37 tests in 55.141 seconds. Both full bootstrap validation and offline graph
validation passed; neither grants execution authority before human planning merge.

Reviewed canonical SHA-256 digests:

- `backend-catalog.json`: `a0025e16226e89d2460b4afb257aa6f41b5c088f8bf95d1122a5325cd3aba80b`
- `frontend-catalog.json`: `4ee178ea7fafd96ad082969e7201f343331858b5e023ec97fc5f4b5405549f4b`
- `chunks.json`: `5c5b1ef9e29cc9a80a3e3dd48aef88ec921c4e11d1ce611be5b559a34e8938d5`
