# Frontend component catalog

Status: DRAFT, scope 1.0 / architecture 1. These are planned contracts, not implemented screens. Canonical data: [frontend-catalog.json](frontend-catalog.json). Backend schemas and authorization are authoritative; navigation and UI guards never confer access.

Reusable primitives accept DTOs and explicit callbacks. Feature controllers own their generated API subset and current request state. Composition is explicit and its cross-chunk ownership is included in the dependency graph. A shared renderer does not import a role-feature tree. Every field-level request/response is defined in API_SCHEMA_CATALOG.

- **DownloadHandoff:** {kind:ticket,ticket:DownloadTicketView}|{kind:issued_url,url:ApprovedHttpsUrl,label:string}
- **receipt_adapter:** Refetch API-PARENT-RECEIPTS or API-ADMIN-DOCUMENTS, select authorized ReceiptView.id; require nonnull download_url; return issued_url with document number label. No generic file grant for finance.
- **ticket_adapter:** Return {kind:ticket,ticket:await authorizedDownload()}; shared primitive imports no financial model/client.

## AppShell

- **Kind:** primitive
- **Surface:** shared
- **Responsibility:** Compose role-specific landmarks,header,content and navigation without importing every role feature.
- **Chunk:** ZE-P09-C01
- **Expected Module:** apps/web/src/components/shared/AppShell.tsx
- **Composition:** RoleNavigation, PageHeader, AsyncBoundary
- **Reuse:** Shared presentation/domain composition
- **Input Sources:**
- **Local State:** Mobile navigation open state only.
- **States:** loading: Keep structural headings and announce loading; disable duplicate dependent actions.; empty: Show a specific absence message and only permitted next action.; error: Field422,stale409,denied403/invisible404,expired401 and transient429/503 are distinct; show safe message/request_id and bounded retry.; success: Render authoritative returned DTO and invalidate relevant scoped query keys.; detail: 401 clears private state and returns to sign-in; no background private prefetch after denial.
- **Accessibility:** Semantic headings/labels,keyboard access,visible focus,live status,error association,200%reflow; never color alone.
- **Import Boundary:** Shared components accept data/callbacks and import no role-feature tree.
- **Requirements:** NFR-003, NFR-004, NFR-006

| Prop | Type | Required | Source |
|---|---|---|---|
| session | SessionView | True | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |
| navigation | RoleNavigationItem[] | True | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |
| children | ReactNode | True | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |
| onLogout | ()=>Promise<void> | True | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |

| Operation | Request schema | Response schema | Roles | Ownership / state |
|---|---|---|---|---|
| None | Typed supplied props | Presentation callbacks | Caller owns authorization | No autonomous provider/API access |

## RoleNavigation

- **Kind:** primitive
- **Surface:** shared
- **Responsibility:** Render caller-supplied permitted navigation with current-location semantics.
- **Chunk:** ZE-P09-C01
- **Expected Module:** apps/web/src/components/shared/RoleNavigation.tsx
- **Composition:**
- **Reuse:** Shared presentation/domain composition
- **Input Sources:**
- **Local State:** Disclosure state; no role authority computed from URL.
- **States:** loading: Keep structural headings and announce loading; disable duplicate dependent actions.; empty: Show a specific absence message and only permitted next action.; error: Field422,stale409,denied403/invisible404,expired401 and transient429/503 are distinct; show safe message/request_id and bounded retry.; success: Render authoritative returned DTO and invalidate relevant scoped query keys.; detail: Teacher/student registries contain no finance entries.
- **Accessibility:** Use nav landmark,aria-current,page headings and keyboard disclosure.
- **Import Boundary:** Shared components accept data/callbacks and import no role-feature tree.
- **Requirements:** NFR-003, NFR-004, NFR-006

| Prop | Type | Required | Source |
|---|---|---|---|
| items | RoleNavigationItem[] | True | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |
| activePath | string | True | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |

| Operation | Request schema | Response schema | Roles | Ownership / state |
|---|---|---|---|---|
| None | Typed supplied props | Presentation callbacks | Caller owns authorization | No autonomous provider/API access |

## PageHeader

- **Kind:** primitive
- **Surface:** shared
- **Responsibility:** Title,breadcrumb and contextual actions with consistent hierarchy.
- **Chunk:** ZE-P09-C01
- **Expected Module:** apps/web/src/components/shared/PageHeader.tsx
- **Composition:**
- **Reuse:** Shared presentation/domain composition
- **Input Sources:**
- **Local State:** No durable client state; transient presentation state only.
- **States:** loading: Keep structural headings and announce loading; disable duplicate dependent actions.; empty: Show a specific absence message and only permitted next action.; error: Field422,stale409,denied403/invisible404,expired401 and transient429/503 are distinct; show safe message/request_id and bounded retry.; success: Render authoritative returned DTO and invalidate relevant scoped query keys.; detail: State changes are driven by backend response; no guessed success.
- **Accessibility:** Exactly one page h1; breadcrumb list and descriptive action names.
- **Import Boundary:** Shared components accept data/callbacks and import no role-feature tree.
- **Requirements:** NFR-003, NFR-004, NFR-006

| Prop | Type | Required | Source |
|---|---|---|---|
| title | string | True | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |
| breadcrumbs | Breadcrumb[] | True | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |
| actions | ReactNode | False | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |

| Operation | Request schema | Response schema | Roles | Ownership / state |
|---|---|---|---|---|
| None | Typed supplied props | Presentation callbacks | Caller owns authorization | No autonomous provider/API access |

## AsyncBoundary

- **Kind:** primitive
- **Surface:** shared
- **Responsibility:** Consistent loading,empty,error,denial and stale states.
- **Chunk:** ZE-P09-C01
- **Expected Module:** apps/web/src/components/shared/AsyncBoundary.tsx
- **Composition:**
- **Reuse:** Shared presentation/domain composition
- **Input Sources:**
- **Local State:** Retry focus position only.
- **States:** loading: Keep structural headings and announce loading; disable duplicate dependent actions.; empty: Show a specific absence message and only permitted next action.; error: Field422,stale409,denied403/invisible404,expired401 and transient429/503 are distinct; show safe message/request_id and bounded retry.; success: Render authoritative returned DTO and invalidate relevant scoped query keys.; detail: Never render previously cached private data after401/403/404; stale409 retains unsaved local draft visibly.
- **Accessibility:** Polite live loading/success,assertive validation summary; avoid repeating every polling event.
- **Import Boundary:** Shared components accept data/callbacks and import no role-feature tree.
- **Requirements:** NFR-003, NFR-004, NFR-006

| Prop | Type | Required | Source |
|---|---|---|---|
| status | QueryStatus | True | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |
| error | Error | False | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |
| emptyMessage | string | True | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |
| onRetry | ()=>void | False | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |
| children | ReactNode | True | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |

| Operation | Request schema | Response schema | Roles | Ownership / state |
|---|---|---|---|---|
| None | Typed supplied props | Presentation callbacks | Caller owns authorization | No autonomous provider/API access |

## FormFields

- **Kind:** primitive
- **Surface:** shared
- **Responsibility:** Reusable labeled text,number,select,radio,checkbox and error-summary composition.
- **Chunk:** ZE-P09-C01
- **Expected Module:** apps/web/src/components/shared/FormFields.tsx
- **Composition:**
- **Reuse:** Shared presentation/domain composition
- **Input Sources:**
- **Local State:** Draft values and dirty flags only; secrets in memory.
- **States:** loading: Keep structural headings and announce loading; disable duplicate dependent actions.; empty: Show a specific absence message and only permitted next action.; error: Field422,stale409,denied403/invisible404,expired401 and transient429/503 are distinct; show safe message/request_id and bounded retry.; success: Render authoritative returned DTO and invalidate relevant scoped query keys.; detail: Unknown fields never sent; optional blank=>null and omitted PATCH remain distinct.
- **Accessibility:** Labels and descriptions linked to controls; errors linked to fields; focus first invalid field.
- **Import Boundary:** Shared components accept data/callbacks and import no role-feature tree.
- **Requirements:** NFR-003, NFR-004, NFR-006

| Prop | Type | Required | Source |
|---|---|---|---|
| schemaName | GeneratedRequestSchemaName | True | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |
| values | KnownSchemaFields | True | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |
| errors | FieldError[] | False | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |
| onChange | FieldChangeHandler | True | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |

| Operation | Request schema | Response schema | Roles | Ownership / state |
|---|---|---|---|---|
| None | Typed supplied props | Presentation callbacks | Caller owns authorization | No autonomous provider/API access |

## ConfirmActionDialog

- **Kind:** primitive
- **Surface:** shared
- **Responsibility:** Confirm deliberate lifecycle transitions with reason/evidence when required.
- **Chunk:** ZE-P09-C01
- **Expected Module:** apps/web/src/components/shared/ConfirmActionDialog.tsx
- **Composition:** FormFields
- **Reuse:** Shared presentation/domain composition
- **Input Sources:**
- **Local State:** Open,state,reason/evidence draft and submit pending.
- **States:** loading: Keep structural headings and announce loading; disable duplicate dependent actions.; empty: Show a specific absence message and only permitted next action.; error: Field422,stale409,denied403/invisible404,expired401 and transient429/503 are distinct; show safe message/request_id and bounded retry.; success: Render authoritative returned DTO and invalidate relevant scoped query keys.; detail: Do not close on409/422; show change preview and reason; no success until authoritative result.
- **Accessibility:** Modal focus trap,Escape where safe,return focus to trigger; destructive action text explicit.
- **Import Boundary:** Shared components accept data/callbacks and import no role-feature tree.
- **Requirements:** NFR-003, NFR-004, NFR-006

| Prop | Type | Required | Source |
|---|---|---|---|
| title | string | True | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |
| description | string | True | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |
| reasonRequired | boolean | True | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |
| evidenceRequired | boolean | False | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |
| pending | boolean | True | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |
| onConfirm | ConfirmationHandler | True | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |

| Operation | Request schema | Response schema | Roles | Ownership / state |
|---|---|---|---|---|
| None | Typed supplied props | Presentation callbacks | Caller owns authorization | No autonomous provider/API access |

## ResourceTable

- **Kind:** primitive
- **Surface:** shared
- **Responsibility:** Display bounded typed rows with filter,sort,page cursor and row actions.
- **Chunk:** ZE-P09-C01
- **Expected Module:** apps/web/src/components/shared/ResourceTable.tsx
- **Composition:** AsyncBoundary
- **Reuse:** Shared presentation/domain composition
- **Input Sources:**
- **Local State:** Filter draft/cursor in URL; no row editing authority.
- **States:** loading: Keep structural headings and announce loading; disable duplicate dependent actions.; empty: Show a specific absence message and only permitted next action.; error: Field422,stale409,denied403/invisible404,expired401 and transient429/503 are distinct; show safe message/request_id and bounded retry.; success: Render authoritative returned DTO and invalidate relevant scoped query keys.; detail: Clear cursor when filter changes; row action state server-driven.
- **Accessibility:** Semantic table headers and caption; mobile labelled cards; keyboard actions independent of hover.
- **Import Boundary:** Shared components accept data/callbacks and import no role-feature tree.
- **Requirements:** NFR-003, NFR-004, NFR-006

| Prop | Type | Required | Source |
|---|---|---|---|
| columns | ColumnSpec[] | True | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |
| rows | DisplayRow[] | True | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |
| page | PageMeta | True | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |
| onPage | CursorHandler | True | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |
| actions | RowActionFactory | False | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |

| Operation | Request schema | Response schema | Roles | Ownership / state |
|---|---|---|---|---|
| None | Typed supplied props | Presentation callbacks | Caller owns authorization | No autonomous provider/API access |

## ScheduleView

- **Kind:** domain
- **Surface:** shared
- **Responsibility:** Present timezone-aware calendar/list data without scheduling authority.
- **Chunk:** ZE-P09-C01
- **Expected Module:** apps/web/src/components/shared/ScheduleView.tsx
- **Composition:** AsyncBoundary
- **Reuse:** Shared presentation/domain composition
- **Input Sources:**
- **Local State:** List/calendar mode and display timezone only.
- **States:** loading: Keep structural headings and announce loading; disable duplicate dependent actions.; empty: Show a specific absence message and only permitted next action.; error: Field422,stale409,denied403/invisible404,expired401 and transient429/503 are distinct; show safe message/request_id and bounded retry.; success: Render authoritative returned DTO and invalidate relevant scoped query keys.; detail: Public rows render only id/start/end/timezone. Narrow to ClassSessionView before using title/status/integration/action fields; never fabricate private state for a public row. Public onOpen is optional. Parent/student receive no mutation callbacks.
- **Accessibility:** Equivalent list view,explicit timezone/DST labels,keyboard date navigation and readable cancelled status.
- **Import Boundary:** Shared components accept data/callbacks and import no role-feature tree.
- **Requirements:** NFR-003, NFR-004, NFR-006

| Prop | Type | Required | Source |
|---|---|---|---|
| sessions | readonly(PublicSessionView\|ClassSessionView)[] | True | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |
| displayZone | IanaTimezone | True | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |
| onOpen | SessionHandler | False | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |
| editableActions | SessionActionFactory | False | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |

| Operation | Request schema | Response schema | Roles | Ownership / state |
|---|---|---|---|---|
| None | Typed supplied props | Presentation callbacks | Caller owns authorization | No autonomous provider/API access |

## UploadControl

- **Kind:** primitive
- **Surface:** shared
- **Responsibility:** Coordinate permitted file selection,transfer and visible scan state through supplied typed adapter.
- **Chunk:** ZE-P09-C01
- **Expected Module:** apps/web/src/components/shared/UploadControl.tsx
- **Composition:** AsyncBoundary
- **Reuse:** Shared presentation/domain composition
- **Input Sources:**
- **Local State:** File selection,transfer progress,cancel intent; no durable local file copy.
- **States:** loading: Keep structural headings and announce loading; disable duplicate dependent actions.; empty: Show a specific absence message and only permitted next action.; error: Field422,stale409,denied403/invisible404,expired401 and transient429/503 are distinct; show safe message/request_id and bounded retry.; success: Render authoritative returned DTO and invalidate relevant scoped query keys.; detail: Selected→ticket→upload→confirm→quarantined/scanning→ready/rejected; only ready assets returned; no client scan authority.
- **Accessibility:** Accessible file picker and progress; announce completion/error not every byte; text size/type instructions.
- **Import Boundary:** Shared components accept data/callbacks and import no role-feature tree.
- **Requirements:** NFR-003, NFR-004, NFR-006

| Prop | Type | Required | Source |
|---|---|---|---|
| policy | UploadPolicy | True | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |
| assets | FileAssetView[] | True | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |
| adapter | AuthorizedUploadAdapter | True | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |
| onReady | AssetHandler | True | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |
| onRemove | AssetHandler | True | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |

| Operation | Request schema | Response schema | Roles | Ownership / state |
|---|---|---|---|---|
| None | Typed supplied props | Presentation callbacks | Caller owns authorization | No autonomous provider/API access |

## ProtectedDownloadAction

- **Kind:** primitive
- **Surface:** shared
- **Responsibility:** Acquire an authorized short-lived download only on deliberate user action.
- **Chunk:** ZE-P09-C01
- **Expected Module:** apps/web/src/components/shared/ProtectedDownloadAction.tsx
- **Composition:**
- **Reuse:** Shared presentation/domain composition
- **Input Sources:**
- **Local State:** Pending and safe error only; URL transient.
- **States:** loading: Keep structural headings and announce loading; disable duplicate dependent actions.; empty: Show a specific absence message and only permitted next action.; error: Field422,stale409,denied403/invisible404,expired401 and transient429/503 are distinct; show safe message/request_id and bounded retry.; success: Render authoritative returned DTO and invalidate relevant scoped query keys.; detail: Ticket callers wrap a freshly issued DownloadTicketView. Receipt/invoice callers refetch their authorized document list on click and select its nonnull download_url; null means not ready. Issued URLs are immediately used, never persisted. Do not fabricate expiry,filename or MIME metadata. Expired/denied use requires a new authorized read.
- **Accessibility:** Describe file kind/size and new-window/download action; keyboard button; announce ready/error.
- **Import Boundary:** Shared components accept data/callbacks and import no role-feature tree.
- **Requirements:** NFR-003, NFR-004, NFR-006

| Prop | Type | Required | Source |
|---|---|---|---|
| label | string | True | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |
| issueDownload | ()=>Promise<DownloadHandoff> | True | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |
| disabledReason | string | False | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |

| Operation | Request schema | Response schema | Roles | Ownership / state |
|---|---|---|---|---|
| None | Typed supplied props | Presentation callbacks | Caller owns authorization | No autonomous provider/API access |

## MoneyText

- **Kind:** primitive
- **Surface:** shared
- **Responsibility:** Format server-supplied AUD minor units without price calculation or billing authority.
- **Chunk:** ZE-P09-C01
- **Expected Module:** apps/web/src/components/shared/MoneyText.tsx
- **Composition:**
- **Reuse:** Shared presentation/domain composition
- **Input Sources:**
- **Local State:** No durable client state; transient presentation state only.
- **States:** loading: Keep structural headings and announce loading; disable duplicate dependent actions.; empty: Show a specific absence message and only permitted next action.; error: Field422,stale409,denied403/invisible404,expired401 and transient429/503 are distinct; show safe message/request_id and bounded retry.; success: Render authoritative returned DTO and invalidate relevant scoped query keys.; detail: State changes are driven by backend response; no guessed success.
- **Accessibility:** Intl currency formatting; text includes AUD where ambiguity exists; no color-only refund amounts.
- **Import Boundary:** Shared components accept data/callbacks and import no role-feature tree.
- **Requirements:** NFR-003, NFR-004, NFR-006

| Prop | Type | Required | Source |
|---|---|---|---|
| amountMinor | number | True | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |
| currency | Currency | True | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |
| taxLabel | string | False | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |

| Operation | Request schema | Response schema | Roles | Ownership / state |
|---|---|---|---|---|
| None | Typed supplied props | Presentation callbacks | Caller owns authorization | No autonomous provider/API access |

## StatusBadge

- **Kind:** primitive
- **Surface:** shared
- **Responsibility:** Render supplied lifecycle state as plain text and semantic status.
- **Chunk:** ZE-P09-C01
- **Expected Module:** apps/web/src/components/shared/StatusBadge.tsx
- **Composition:**
- **Reuse:** Shared presentation/domain composition
- **Input Sources:**
- **Local State:** No durable client state; transient presentation state only.
- **States:** loading: Keep structural headings and announce loading; disable duplicate dependent actions.; empty: Show a specific absence message and only permitted next action.; error: Field422,stale409,denied403/invisible404,expired401 and transient429/503 are distinct; show safe message/request_id and bounded retry.; success: Render authoritative returned DTO and invalidate relevant scoped query keys.; detail: State changes are driven by backend response; no guessed success.
- **Accessibility:** Text+icon with sufficient contrast; never rely on color.
- **Import Boundary:** Shared components accept data/callbacks and import no role-feature tree.
- **Requirements:** NFR-003, NFR-004, NFR-006

| Prop | Type | Required | Source |
|---|---|---|---|
| status | string | True | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |
| label | string | True | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |
| tone | StatusTone | True | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |

| Operation | Request schema | Response schema | Roles | Ownership / state |
|---|---|---|---|---|
| None | Typed supplied props | Presentation callbacks | Caller owns authorization | No autonomous provider/API access |

## ProgressSummary

- **Kind:** domain
- **Surface:** shared
- **Responsibility:** Explain source progress counts,attendance and server completion basis.
- **Chunk:** ZE-P09-C01
- **Expected Module:** apps/web/src/components/shared/ProgressSummary.tsx
- **Composition:** StatusBadge
- **Reuse:** Shared presentation/domain composition
- **Input Sources:**
- **Local State:** No durable client state; transient presentation state only.
- **States:** loading: Keep structural headings and announce loading; disable duplicate dependent actions.; empty: Show a specific absence message and only permitted next action.; error: Field422,stale409,denied403/invisible404,expired401 and transient429/503 are distinct; show safe message/request_id and bounded retry.; success: Render authoritative returned DTO and invalidate relevant scoped query keys.; detail: Display counts and standards/admin_override basis; no client completion calculation.
- **Accessibility:** Labeled progressbar plus textual counts; readable low-progress states without punitive imagery.
- **Import Boundary:** Shared components accept data/callbacks and import no role-feature tree.
- **Requirements:** NFR-003, NFR-004, NFR-006

| Prop | Type | Required | Source |
|---|---|---|---|
| progress | ProgressView | True | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |
| showTeachingActions | boolean | False | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |

| Operation | Request schema | Response schema | Roles | Ownership / state |
|---|---|---|---|---|
| None | Typed supplied props | Presentation callbacks | Caller owns authorization | No autonomous provider/API access |

## ReleasedResultView

- **Kind:** domain
- **Surface:** shared
- **Responsibility:** Present only provided released assessment/quiz feedback without answer-key lookup.
- **Chunk:** ZE-P09-C01
- **Expected Module:** apps/web/src/components/shared/ReleasedResultView.tsx
- **Composition:** StatusBadge
- **Reuse:** Shared presentation/domain composition
- **Input Sources:**
- **Local State:** No durable client state; transient presentation state only.
- **States:** loading: Keep structural headings and announce loading; disable duplicate dependent actions.; empty: Show a specific absence message and only permitted next action.; error: Field422,stale409,denied403/invisible404,expired401 and transient429/503 are distinct; show safe message/request_id and bounded retry.; success: Render authoritative returned DTO and invalidate relevant scoped query keys.; detail: Null/unreleased unavailable; withdrawn results refetch and disappear; correctness/explanation only supplied submitted result.
- **Accessibility:** Score in text; approved explanation adjacent to question; screen-reader labels and no color-only correctness.
- **Import Boundary:** Shared components accept data/callbacks and import no role-feature tree.
- **Requirements:** NFR-003, NFR-004, NFR-006

| Prop | Type | Required | Source |
|---|---|---|---|
| assessment | AssessmentView | False | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |
| quizResult | ReleasedQuizResult | False | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |
| feedback | FeedbackView[] | False | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |

| Operation | Request schema | Response schema | Roles | Ownership / state |
|---|---|---|---|---|
| None | Typed supplied props | Presentation callbacks | Caller owns authorization | No autonomous provider/API access |

## CertificateCard

- **Kind:** domain
- **Surface:** shared
- **Responsibility:** Show valid/revoked/pending certificate and delegate protected download.
- **Chunk:** ZE-P09-C01
- **Expected Module:** apps/web/src/components/shared/CertificateCard.tsx
- **Composition:** StatusBadge, ProtectedDownloadAction
- **Reuse:** Shared presentation/domain composition
- **Input Sources:**
- **Local State:** No durable client state; transient presentation state only.
- **States:** loading: Keep structural headings and announce loading; disable duplicate dependent actions.; empty: Show a specific absence message and only permitted next action.; error: Field422,stale409,denied403/invisible404,expired401 and transient429/503 are distinct; show safe message/request_id and bounded retry.; success: Render authoritative returned DTO and invalidate relevant scoped query keys.; detail: Pending render has no download; revoked labelled and no current-document representation.
- **Accessibility:** Text course/issue/status; document action includes learner-safe name; no public child lookup.
- **Import Boundary:** Shared components accept data/callbacks and import no role-feature tree.
- **Requirements:** NFR-003, NFR-004, NFR-006

| Prop | Type | Required | Source |
|---|---|---|---|
| certificate | CertificateView | True | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |
| onDownload | ()=>Promise<DownloadTicketView> | True | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |

| Operation | Request schema | Response schema | Roles | Ownership / state |
|---|---|---|---|---|
| None | Typed supplied props | Presentation callbacks | Caller owns authorization | No autonomous provider/API access |

## NotificationList

- **Kind:** domain
- **Surface:** shared
- **Responsibility:** Render recipient-owned inbox and supplied read action.
- **Chunk:** ZE-P09-C01
- **Expected Module:** apps/web/src/components/shared/NotificationList.tsx
- **Composition:** AsyncBoundary, StatusBadge
- **Reuse:** Shared presentation/domain composition
- **Input Sources:**
- **Local State:** Unread filter and selected row only.
- **States:** loading: Keep structural headings and announce loading; disable duplicate dependent actions.; empty: Show a specific absence message and only permitted next action.; error: Field422,stale409,denied403/invisible404,expired401 and transient429/503 are distinct; show safe message/request_id and bounded retry.; success: Render authoritative returned DTO and invalidate relevant scoped query keys.; detail: Safe allowlisted deep links; no payment notification types presented to teacher/student.
- **Accessibility:** Unread text,keyboard list actions,polite unread-count updates.
- **Import Boundary:** Shared components accept data/callbacks and import no role-feature tree.
- **Requirements:** NFR-003, NFR-004, NFR-006

| Prop | Type | Required | Source |
|---|---|---|---|
| items | NotificationView[] | True | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |
| page | PageMeta | True | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |
| onRead | NotificationReadHandler | True | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |
| onOpen | PortalPathHandler | True | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |

| Operation | Request schema | Response schema | Roles | Ownership / state |
|---|---|---|---|---|
| None | Typed supplied props | Presentation callbacks | Caller owns authorization | No autonomous provider/API access |

## AuditReasonForm

- **Kind:** primitive
- **Surface:** shared
- **Responsibility:** Collect explicit reason and verification/evidence reference for a privileged action.
- **Chunk:** ZE-P09-C01
- **Expected Module:** apps/web/src/components/shared/AuditReasonForm.tsx
- **Composition:** FormFields
- **Reuse:** Shared presentation/domain composition
- **Input Sources:**
- **Local State:** Unsaved reason/evidence draft only.
- **States:** loading: Keep structural headings and announce loading; disable duplicate dependent actions.; empty: Show a specific absence message and only permitted next action.; error: Field422,stale409,denied403/invisible404,expired401 and transient429/503 are distinct; show safe message/request_id and bounded retry.; success: Render authoritative returned DTO and invalidate relevant scoped query keys.; detail: Reference is sent for server verification; UI never declares arbitrary text approved evidence.
- **Accessibility:** Describe required evidence clearly; errors focus relevant field.
- **Import Boundary:** Shared components accept data/callbacks and import no role-feature tree.
- **Requirements:** NFR-003, NFR-004, NFR-006

| Prop | Type | Required | Source |
|---|---|---|---|
| reason | string | True | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |
| evidenceReferences | string[] | False | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |
| requirements | ReasonPolicy | True | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |
| onChange | ReasonChangeHandler | True | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |

| Operation | Request schema | Response schema | Roles | Ownership / state |
|---|---|---|---|---|
| None | Typed supplied props | Presentation callbacks | Caller owns authorization | No autonomous provider/API access |

## ActorSessionProvider

- **Kind:** foundation
- **Surface:** shared
- **Responsibility:** Load current session identity and scope all private query state.
- **Chunk:** ZE-P09-C01
- **Expected Module:** apps/web/src/features/shared/ActorSessionProvider.tsx
- **Composition:**
- **Reuse:** Shared presentation/domain composition
- **Input Sources:**
- **Local State:** Session availability only; opaque cookie inaccessible to JS.
- **States:** loading: Keep structural headings and announce loading; disable duplicate dependent actions.; empty: Show a specific absence message and only permitted next action.; error: Field422,stale409,denied403/invisible404,expired401 and transient429/503 are distinct; show safe message/request_id and bounded retry.; success: Render authoritative returned DTO and invalidate relevant scoped query keys.; detail: 401 flushes all private query state; role/account change remounts context; setup challenge is not a full session.
- **Accessibility:** Redirect/focus announcement only after final auth decision.
- **Import Boundary:** Shared components accept data/callbacks and import no role-feature tree.
- **Requirements:** ADM-001, AUTH-001, AUTH-002, AUTH-003, AUTH-004, AUTH-005, PAR-001, STU-001, TCH-001

| Prop | Type | Required | Source |
|---|---|---|---|
| children | ReactNode | True | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |
| initialSession | SessionView | False | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |

| Operation | Request schema | Response schema | Roles | Ownership / state |
|---|---|---|---|---|
| API-AUTH-ME | API_AUTH_MERequest | SessionView | parent, student, teacher, admin | Authenticated principal owns this account/session/notification; server resolves subject, never trusts requested role. |

## PublishedPage

- **Kind:** feature
- **Surface:** public
- **Responsibility:** Render explicitly published business information for fixed page slug.
- **Chunk:** ZE-P09-C02
- **Expected Module:** apps/web/src/features/public/PublishedPage.tsx
- **Composition:** PageHeader, AsyncBoundary
- **Reuse:** Feature-specific orchestration using shared domain and UI components
- **Input Sources:**
- **Local State:** No durable client state; transient presentation state only.
- **States:** loading: Keep structural headings and announce loading; disable duplicate dependent actions.; empty: Show a specific absence message and only permitted next action.; error: Field422,stale409,denied403/invisible404,expired401 and transient429/503 are distinct; show safe message/request_id and bounded retry.; success: Render authoritative returned DTO and invalidate relevant scoped query keys.; detail: Draft404 returns unavailable; sanitize-approved content rendered with semantic headings; no raw unsafe HTML.
- **Accessibility:** Accessible approved images/headings and responsive content.
- **Import Boundary:** May import shared and declared feature dependencies; generated API subset only.
- **Requirements:** LRN-001, WEB-001, WEB-002, WEB-003, WEB-004, WEB-007, WEB-008, WEB-009, WEB-012

| Prop | Type | Required | Source |
|---|---|---|---|
| slug | PublicPageSlug | True | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |

| Operation | Request schema | Response schema | Roles | Ownership / state |
|---|---|---|---|---|
| API-PUBLIC-PAGE | API_PUBLIC_PAGERequest | PublicPageView | public | Only explicitly published projection; no private child, roster, billing or operational data. |

## CourseCatalogue

- **Kind:** feature
- **Surface:** public
- **Responsibility:** Browse published programs/courses and age-fit information.
- **Chunk:** ZE-P09-C02
- **Expected Module:** apps/web/src/features/public/CourseCatalogue.tsx
- **Composition:** PageHeader, ResourceTable, MoneyText
- **Reuse:** Feature-specific orchestration using shared domain and UI components
- **Input Sources:**
- **Local State:** Client presentation filters over authorized page data; filters do not determine enrolment eligibility.
- **States:** loading: Keep structural headings and announce loading; disable duplicate dependent actions.; empty: Show a specific absence message and only permitted next action.; error: Field422,stale409,denied403/invisible404,expired401 and transient429/503 are distinct; show safe message/request_id and bounded retry.; success: Render authoritative returned DTO and invalidate relevant scoped query keys.; detail: Show published-course empty state and pagination; no unpublished query fallback.
- **Accessibility:** Semantic headings/labels,keyboard access,visible focus,live status,error association,200%reflow; never color alone.
- **Import Boundary:** May import shared and declared feature dependencies; generated API subset only.
- **Requirements:** LRN-001, WEB-001, WEB-002, WEB-003, WEB-004, WEB-007, WEB-008, WEB-009, WEB-012

| Prop | Type | Required | Source |
|---|---|---|---|
| initialProgram | string | False | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |
| initialAge | number | False | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |

| Operation | Request schema | Response schema | Roles | Ownership / state |
|---|---|---|---|---|
| API-PUBLIC-PROGRAMS | API_PUBLIC_PROGRAMSRequest | PublicProgramViewPage | public | Only explicitly published projection; no private child, roster, billing or operational data. |
| API-PUBLIC-COURSES | API_PUBLIC_COURSESRequest | PublicCourseViewPage | public | Only explicitly published projection; no private child, roster, billing or operational data. |

## CourseDetail

- **Kind:** feature
- **Surface:** public
- **Responsibility:** Show outcomes,age band,duration,delivery,fee and available scheduled cohorts with enrolment entry.
- **Chunk:** ZE-P09-C02
- **Expected Module:** apps/web/src/features/public/CourseDetail.tsx
- **Composition:** PageHeader, MoneyText, ScheduleView, StatusBadge
- **Reuse:** Feature-specific orchestration using shared domain and UI components
- **Input Sources:**
- **Local State:** Selected cohort only; stored return path contains allowed course/cohort IDs.
- **States:** loading: Keep structural headings and announce loading; disable duplicate dependent actions.; empty: Show a specific absence message and only permitted next action.; error: Field422,stale409,denied403/invisible404,expired401 and transient429/503 are distinct; show safe message/request_id and bounded retry.; success: Render authoritative returned DTO and invalidate relevant scoped query keys.; detail: Resolve course_id from returned course.id before cohorts read; full/closed cohorts have no enabled checkout entry.
- **Accessibility:** Semantic headings/labels,keyboard access,visible focus,live status,error association,200%reflow; never color alone.
- **Import Boundary:** May import shared and declared feature dependencies; generated API subset only.
- **Requirements:** LRN-001, WEB-001, WEB-002, WEB-003, WEB-004, WEB-007, WEB-008, WEB-009, WEB-012

| Prop | Type | Required | Source |
|---|---|---|---|
| courseSlug | string | True | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |

| Operation | Request schema | Response schema | Roles | Ownership / state |
|---|---|---|---|---|
| API-PUBLIC-COURSE | API_PUBLIC_COURSERequest | PublicCourseView | public | Only explicitly published projection; no private child, roster, billing or operational data. |
| API-PUBLIC-COHORTS | API_PUBLIC_COHORTSRequest | PublicCohortViewPage | public | Only explicitly published projection; no private child, roster, billing or operational data. |

## InstructorDirectory

- **Kind:** feature
- **Surface:** public
- **Responsibility:** Show approved public instructor biographies/photos.
- **Chunk:** ZE-P09-C02
- **Expected Module:** apps/web/src/features/public/InstructorDirectory.tsx
- **Composition:** PageHeader, AsyncBoundary
- **Reuse:** Feature-specific orchestration using shared domain and UI components
- **Input Sources:**
- **Local State:** No durable client state; transient presentation state only.
- **States:** loading: Keep structural headings and announce loading; disable duplicate dependent actions.; empty: Show a specific absence message and only permitted next action.; error: Field422,stale409,denied403/invisible404,expired401 and transient429/503 are distinct; show safe message/request_id and bounded retry.; success: Render authoritative returned DTO and invalidate relevant scoped query keys.; detail: No private contact/operational profile fields.
- **Accessibility:** Portrait alternatives and biography headings; no card link without target API.
- **Import Boundary:** May import shared and declared feature dependencies; generated API subset only.
- **Requirements:** LRN-001, WEB-001, WEB-002, WEB-003, WEB-004, WEB-007, WEB-008, WEB-009, WEB-012

| Prop | Type | Required | Source |
|---|---|---|---|
| None | Route/session controller obtains its own authorized state | — | No implicit client identity authority |

| Operation | Request schema | Response schema | Roles | Ownership / state |
|---|---|---|---|---|
| API-PUBLIC-TEACHERS | API_PUBLIC_TEACHERSRequest | PublicTeacherViewPage | public | Only explicitly published projection; no private child, roster, billing or operational data. |

## PolicyLibrary

- **Kind:** feature
- **Surface:** public
- **Responsibility:** Read current published policy versions,terms,privacy and child-safety information.
- **Chunk:** ZE-P09-C02
- **Expected Module:** apps/web/src/features/public/PolicyLibrary.tsx
- **Composition:** PageHeader, AsyncBoundary
- **Reuse:** Feature-specific orchestration using shared domain and UI components
- **Input Sources:**
- **Local State:** Selected policy key from route; read immutable document version.
- **States:** loading: Keep structural headings and announce loading; disable duplicate dependent actions.; empty: Show a specific absence message and only permitted next action.; error: Field422,stale409,denied403/invisible404,expired401 and transient429/503 are distinct; show safe message/request_id and bounded retry.; success: Render authoritative returned DTO and invalidate relevant scoped query keys.; detail: Draft/unapproved policy absent; effective date/version visible; reporting channel linked from approved content.
- **Accessibility:** Semantic headings/labels,keyboard access,visible focus,live status,error association,200%reflow; never color alone.
- **Import Boundary:** May import shared and declared feature dependencies; generated API subset only.
- **Requirements:** SEC-003

| Prop | Type | Required | Source |
|---|---|---|---|
| policyKey | PolicyKey | False | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |

| Operation | Request schema | Response schema | Roles | Ownership / state |
|---|---|---|---|---|
| API-POLICY-LIST | API_POLICY_LISTRequest | PolicyViewPage | public | Only explicitly published projection; no private child, roster, billing or operational data. |

## ContactEnquiryForm

- **Kind:** feature
- **Surface:** public
- **Responsibility:** Display approved contact guidance and submit bounded enquiry.
- **Chunk:** ZE-P09-C02
- **Expected Module:** apps/web/src/features/public/ContactEnquiryForm.tsx
- **Composition:** PageHeader, FormFields, AsyncBoundary
- **Reuse:** Feature-specific orchestration using shared domain and UI components
- **Input Sources:**
- **Local State:** Name,email,message,honeypot/token if configured.
- **States:** loading: Keep structural headings and announce loading; disable duplicate dependent actions.; empty: Show a specific absence message and only permitted next action.; error: Field422,stale409,denied403/invisible404,expired401 and transient429/503 are distinct; show safe message/request_id and bounded retry.; success: Render authoritative returned DTO and invalidate relevant scoped query keys.; detail: Uniform receipt/reference; rate-limit feedback; no attachments or child-record matching.
- **Accessibility:** Accessible error summary and successful receipt status.
- **Import Boundary:** May import shared and declared feature dependencies; generated API subset only.
- **Requirements:** LRN-001, WEB-001, WEB-002, WEB-003, WEB-004, WEB-007, WEB-008, WEB-009, WEB-012

| Prop | Type | Required | Source |
|---|---|---|---|
| None | Route/session controller obtains its own authorized state | — | No implicit client identity authority |

| Operation | Request schema | Response schema | Roles | Ownership / state |
|---|---|---|---|---|
| API-PUBLIC-PAGE | API_PUBLIC_PAGERequest | PublicPageView | public | Only explicitly published projection; no private child, roster, billing or operational data. |
| API-PUBLIC-CONTACT | API_PUBLIC_CONTACTRequest | ContactReceipt | public | Rate limit; honeypot; no attachments, child profile matching or marketing subscription. |

## PublicEvents

- **Kind:** feature
- **Surface:** public
- **Responsibility:** Read explicitly public upcoming event information.
- **Chunk:** ZE-P09-C02
- **Expected Module:** apps/web/src/features/public/PublicEvents.tsx
- **Composition:** PageHeader, AsyncBoundary, StatusBadge
- **Reuse:** Feature-specific orchestration using shared domain and UI components
- **Input Sources:**
- **Local State:** No durable client state; transient presentation state only.
- **States:** loading: Keep structural headings and announce loading; disable duplicate dependent actions.; empty: Show a specific absence message and only permitted next action.; error: Field422,stale409,denied403/invisible404,expired401 and transient429/503 are distinct; show safe message/request_id and bounded retry.; success: Render authoritative returned DTO and invalidate relevant scoped query keys.; detail: No private audience membership or learner roster shown.
- **Accessibility:** Semantic headings/labels,keyboard access,visible focus,live status,error association,200%reflow; never color alone.
- **Import Boundary:** May import shared and declared feature dependencies; generated API subset only.
- **Requirements:** COM-001, COM-002, COM-003, COM-004, COM-005, COM-006, COM-008, COM-009

| Prop | Type | Required | Source |
|---|---|---|---|
| None | Route/session controller obtains its own authorized state | — | No implicit client identity authority |

| Operation | Request schema | Response schema | Roles | Ownership / state |
|---|---|---|---|---|
| API-PUBLIC-EVENTS | API_PUBLIC_EVENTSRequest | EventViewPage | public | Only explicitly published projection; no private child, roster, billing or operational data. |

## SignInForm

- **Kind:** feature
- **Surface:** public
- **Responsibility:** Authenticate adult,student alias or staff and branch on exact AuthOutcomeView.
- **Chunk:** ZE-P09-C03
- **Expected Module:** apps/web/src/features/public/SignInForm.tsx
- **Composition:** FormFields, AsyncBoundary
- **Reuse:** Feature-specific orchestration using shared domain and UI components
- **Input Sources:**
- **Local State:** Identifier,password,pending state in memory only.
- **States:** loading: Keep structural headings and announce loading; disable duplicate dependent actions.; empty: Show a specific absence message and only permitted next action.; error: Field422,stale409,denied403/invisible404,expired401 and transient429/503 are distinct; show safe message/request_id and bounded retry.; success: Render authoritative returned DTO and invalidate relevant scoped query keys.; detail: authenticated enters authorized role home from SessionView; mfa_challenge enters challenge screen; mfa_setup_required enters /mfa-setup with the opaque limited token, without inferring role. Preserve only an allowlisted return path.
- **Accessibility:** Autocomplete username/current-password; accessible show-password control; uniform error,not account-existence leak.
- **Import Boundary:** May import shared and declared feature dependencies; generated API subset only.
- **Requirements:** AUTH-001, AUTH-002, AUTH-003, AUTH-004, AUTH-005, WEB-011

| Prop | Type | Required | Source |
|---|---|---|---|
| returnPath | AllowedPortalPath | False | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |

| Operation | Request schema | Response schema | Roles | Ownership / state |
|---|---|---|---|---|
| API-AUTH-LOGIN | API_AUTH_LOGINRequest | AuthOutcomeView | public | Credential and account status; staff MFA challenge before privileged session. |

## ParentRegistrationForm

- **Kind:** feature
- **Surface:** public
- **Responsibility:** Create verified parent-family registration with current required policy IDs.
- **Chunk:** ZE-P09-C03
- **Expected Module:** apps/web/src/features/public/ParentRegistrationForm.tsx
- **Composition:** FormFields, AsyncBoundary
- **Reuse:** Feature-specific orchestration using shared domain and UI components
- **Input Sources:**
- **Local State:** Required adult name,email,password,policy acknowledgements.
- **States:** loading: Keep structural headings and announce loading; disable duplicate dependent actions.; empty: Show a specific absence message and only permitted next action.; error: Field422,stale409,denied403/invisible404,expired401 and transient429/503 are distinct; show safe message/request_id and bounded retry.; success: Render authoritative returned DTO and invalidate relevant scoped query keys.; detail: Verification pending message; do not activate child account/checkout before verified email.
- **Accessibility:** Semantic headings/labels,keyboard access,visible focus,live status,error association,200%reflow; never color alone.
- **Import Boundary:** May import shared and declared feature dependencies; generated API subset only.
- **Requirements:** AUTH-001, AUTH-002, AUTH-003, AUTH-004, AUTH-005, SEC-003, WEB-011

| Prop | Type | Required | Source |
|---|---|---|---|
| returnPath | AllowedPortalPath | False | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |

| Operation | Request schema | Response schema | Roles | Ownership / state |
|---|---|---|---|---|
| API-AUTH-REGISTER | API_AUTH_REGISTERRequest | AccountView | public | Email uniqueness; accepted current required policy versions; rate-limit by address/network. |
| API-POLICY-LIST | API_POLICY_LISTRequest | PolicyViewPage | public | Only explicitly published projection; no private child, roster, billing or operational data. |

## EmailVerificationFlow

- **Kind:** feature
- **Surface:** public
- **Responsibility:** Consume verification token or request bounded resend.
- **Chunk:** ZE-P09-C03
- **Expected Module:** apps/web/src/features/public/EmailVerificationFlow.tsx
- **Composition:** FormFields, AsyncBoundary
- **Reuse:** Feature-specific orchestration using shared domain and UI components
- **Input Sources:**
- **Local State:** Single-use token held briefly and removed from displayed URL/history.
- **States:** loading: Keep structural headings and announce loading; disable duplicate dependent actions.; empty: Show a specific absence message and only permitted next action.; error: Field422,stale409,denied403/invisible404,expired401 and transient429/503 are distinct; show safe message/request_id and bounded retry.; success: Render authoritative returned DTO and invalidate relevant scoped query keys.; detail: Consumed/expired token has resend path without exposing account existence; returnedEmpty treated success not JSON parse.
- **Accessibility:** Semantic headings/labels,keyboard access,visible focus,live status,error association,200%reflow; never color alone.
- **Import Boundary:** May import shared and declared feature dependencies; generated API subset only.
- **Requirements:** AUTH-001, AUTH-002, AUTH-003, AUTH-004, AUTH-005, WEB-011

| Prop | Type | Required | Source |
|---|---|---|---|
| token | OneTimeToken | False | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |

| Operation | Request schema | Response schema | Roles | Ownership / state |
|---|---|---|---|---|
| API-AUTH-VERIFY | API_AUTH_VERIFYRequest | Empty | public | Hashed token bound to account and purpose; 24h expiry. |
| API-AUTH-RESEND | API_AUTH_RESENDRequest | Empty | public | Uniform response and throttled per identifier. |

## AdultRecoveryFlow

- **Kind:** feature
- **Surface:** public
- **Responsibility:** Request and consume adult password recovery without child-email dependency.
- **Chunk:** ZE-P09-C03
- **Expected Module:** apps/web/src/features/public/AdultRecoveryFlow.tsx
- **Composition:** FormFields, AsyncBoundary
- **Reuse:** Feature-specific orchestration using shared domain and UI components
- **Input Sources:**
- **Local State:** Email or new-password+token in memory; mode comes from route.
- **States:** loading: Keep structural headings and announce loading; disable duplicate dependent actions.; empty: Show a specific absence message and only permitted next action.; error: Field422,stale409,denied403/invisible404,expired401 and transient429/503 are distinct; show safe message/request_id and bounded retry.; success: Render authoritative returned DTO and invalidate relevant scoped query keys.; detail: Uniform reset-request response; expiry and consumed-token clear actions; success requires sign-in after sessions revoked.
- **Accessibility:** Semantic headings/labels,keyboard access,visible focus,live status,error association,200%reflow; never color alone.
- **Import Boundary:** May import shared and declared feature dependencies; generated API subset only.
- **Requirements:** AUTH-001, AUTH-002, AUTH-003, AUTH-004, AUTH-005, WEB-011

| Prop | Type | Required | Source |
|---|---|---|---|
| token | OneTimeToken | False | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |

| Operation | Request schema | Response schema | Roles | Ownership / state |
|---|---|---|---|---|
| API-AUTH-RESET-REQUEST | API_AUTH_RESET_REQUESTRequest | Empty | public | Uniform response; adult verified email only; student recovery managed by guardian. |
| API-AUTH-RESET | API_AUTH_RESETRequest | Empty | public | One-time hashed token, 30-minute lifetime; revocation transactional. |

## MfaChallengeForm

- **Kind:** feature
- **Surface:** public
- **Responsibility:** Verify pending staff TOTP or one unused recovery code.
- **Chunk:** ZE-P09-C03
- **Expected Module:** apps/web/src/features/public/MfaChallengeForm.tsx
- **Composition:** FormFields, AsyncBoundary
- **Reuse:** Feature-specific orchestration using shared domain and UI components
- **Input Sources:**
- **Local State:** Code,recovery/TOTP mode,countdown presentation.
- **States:** loading: Keep structural headings and announce loading; disable duplicate dependent actions.; empty: Show a specific absence message and only permitted next action.; error: Field422,stale409,denied403/invisible404,expired401 and transient429/503 are distinct; show safe message/request_id and bounded retry.; success: Render authoritative returned DTO and invalidate relevant scoped query keys.; detail: No token→restart login; expired/replay/attempt limit→new login; success replaces limited context with full SessionView.
- **Accessibility:** Paste/autocomplete one-time-code; no forced six-digit widget for recovery mode; text expiry warnings.
- **Import Boundary:** May import shared and declared feature dependencies; generated API subset only.
- **Requirements:** AUTH-001, AUTH-002, AUTH-003, AUTH-004, AUTH-005, WEB-011

| Prop | Type | Required | Source |
|---|---|---|---|
| challengeToken | EphemeralToken | True | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |
| expiresAt | DateTime | True | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |

| Operation | Request schema | Response schema | Roles | Ownership / state |
|---|---|---|---|---|
| API-AUTH-MFA | API_AUTH_MFARequest | SessionView | public | Short-lived challenge bound to browser, user and purpose. |

## StaffInvitationFlow

- **Kind:** feature
- **Surface:** public
- **Responsibility:** Accept staff invitation and proceed to limited MFA setup.
- **Chunk:** ZE-P09-C03
- **Expected Module:** apps/web/src/features/public/StaffInvitationFlow.tsx
- **Composition:** FormFields, AsyncBoundary
- **Reuse:** Feature-specific orchestration using shared domain and UI components
- **Input Sources:**
- **Local State:** Password/token in memory; role read from returned account.
- **States:** loading: Keep structural headings and announce loading; disable duplicate dependent actions.; empty: Show a specific absence message and only permitted next action.; error: Field422,stale409,denied403/invisible404,expired401 and transient429/503 are distinct; show safe message/request_id and bounded retry.; success: Render authoritative returned DTO and invalidate relevant scoped query keys.; detail: StaffSetupSessionView permits only enrollment. Navigate to /mfa-setup with its limited token; final activated SessionView determines role landing.
- **Accessibility:** Semantic headings/labels,keyboard access,visible focus,live status,error association,200%reflow; never color alone.
- **Import Boundary:** May import shared and declared feature dependencies; generated API subset only.
- **Requirements:** AUTH-001, AUTH-002, AUTH-003, AUTH-004, AUTH-005, WEB-011

| Prop | Type | Required | Source |
|---|---|---|---|
| token | OneTimeToken | True | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |

| Operation | Request schema | Response schema | Roles | Ownership / state |
|---|---|---|---|---|
| API-AUTH-INVITE-ACCEPT | API_AUTH_INVITE_ACCEPTRequest | StaffSetupSessionView | public | Single-use invitation token; no privilege upgrades from request. |

## StaffMfaSetup

- **Kind:** feature
- **Surface:** shared
- **Responsibility:** Enroll and confirm required TOTP using restricted setup context or recent reauthenticated staff session.
- **Chunk:** ZE-P09-C03
- **Expected Module:** apps/web/src/features/shared/StaffMfaSetup.tsx
- **Composition:** FormFields, AsyncBoundary
- **Reuse:** Shared presentation/domain composition
- **Input Sources:**
- **Local State:** Provisioning URI/setup token/TOTP code/recovery codes transient.
- **States:** loading: Keep structural headings and announce loading; disable duplicate dependent actions.; empty: Show a specific absence message and only permitted next action.; error: Field422,stale409,denied403/invisible404,expired401 and transient429/503 are distinct; show safe message/request_id and bounded retry.; success: Render authoritative returned DTO and invalidate relevant scoped query keys.; detail: Show URI once; confirm yields MfaActivationView; require acknowledgement of recovery-code saving before leaving; never analytics/log QR seed.
- **Accessibility:** Text setup key/URI alternative to QR; copy feedback accessible; recovery codes selectable without being auto-downloaded publicly.
- **Import Boundary:** Shared components accept data/callbacks and import no role-feature tree.
- **Requirements:** ADM-001, AUTH-001, AUTH-002, AUTH-003, AUTH-004, AUTH-005, TCH-001

| Prop | Type | Required | Source |
|---|---|---|---|
| setupToken | EphemeralToken | False | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |

| Operation | Request schema | Response schema | Roles | Ownership / state |
|---|---|---|---|---|
| API-AUTH-MFA-ENROL | API_AUTH_MFA_ENROLRequest | MfaSetupView | teacher, admin | Full staff session with recent password reauthentication OR unexpired purpose-bound MFA setup token returned by password-verified login (mfa_setup_required) or staff invitation acceptance. Server resolves teacher/admin account identity from the token, never a browser-selected role. Limited context permits only enrolment/confirmation; it grants no full session or privileged page access. Enforce token expiry, purpose, account binding, single-use activation and attempt limits. |
| API-AUTH-MFA-CONFIRM | API_AUTH_MFA_CONFIRMRequest | MfaActivationView | teacher, admin | Purpose-bound setup token plus valid first TOTP proof; consume setup token, activate staff account and full MFA session atomically. |

## AccountSecurityPanel

- **Kind:** feature
- **Surface:** shared
- **Responsibility:** Read own account,change adult/staff password,manage sessions and logout.
- **Chunk:** ZE-P09-C03
- **Expected Module:** apps/web/src/features/shared/AccountSecurityPanel.tsx
- **Composition:** ResourceTable, FormFields, ConfirmActionDialog
- **Reuse:** Shared presentation/domain composition
- **Input Sources:**
- **Local State:** Current/new password and revoke confirmation only.
- **States:** loading: Keep structural headings and announce loading; disable duplicate dependent actions.; empty: Show a specific absence message and only permitted next action.; error: Field422,stale409,denied403/invisible404,expired401 and transient429/503 are distinct; show safe message/request_id and bounded retry.; success: Render authoritative returned DTO and invalidate relevant scoped query keys.; detail: Revoked current session clears private data; other-device removal idempotent; password success invalidates sessions and refetches current auth.
- **Accessibility:** Semantic headings/labels,keyboard access,visible focus,live status,error association,200%reflow; never color alone.
- **Import Boundary:** Shared components accept data/callbacks and import no role-feature tree.
- **Requirements:** ADM-001, ADM-003, ADM-006, AUTH-001, AUTH-002, AUTH-003, AUTH-004, AUTH-005, AUTH-011, PAR-001, PAR-002, PAR-021, STU-001, STU-019, TCH-001

| Prop | Type | Required | Source |
|---|---|---|---|
| role | parent\|teacher\|admin | True | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |

| Operation | Request schema | Response schema | Roles | Ownership / state |
|---|---|---|---|---|
| API-ACCOUNT-PROFILE | API_ACCOUNT_PROFILERequest | AccountView | parent, student, teacher, admin | Authenticated principal owns this account/session/notification; server resolves subject, never trusts requested role. |
| API-ACCOUNT-PASSWORD | API_ACCOUNT_PASSWORDRequest | Empty | parent, teacher, admin | Authenticated principal owns this account/session/notification; server resolves subject, never trusts requested role. |
| API-ACCOUNT-SESSIONS | API_ACCOUNT_SESSIONSRequest | DeviceSessionViewPage | parent, teacher, admin | Authenticated principal owns this account/session/notification; server resolves subject, never trusts requested role. |
| API-ACCOUNT-REVOKE | API_ACCOUNT_REVOKERequest | Empty | parent, teacher, admin | Authenticated principal owns this account/session/notification; server resolves subject, never trusts requested role. |
| API-AUTH-LOGOUT | API_AUTH_LOGOUTRequest | Empty | parent, student, teacher, admin | Authenticated principal owns this account/session/notification; server resolves subject, never trusts requested role. |

## FamilyDashboard

- **Kind:** feature
- **Surface:** parent
- **Responsibility:** Show own family,only linked children and role-safe pending action counts.
- **Chunk:** ZE-P10-C01
- **Expected Module:** apps/web/src/features/parent/FamilyDashboard.tsx
- **Composition:** PageHeader, AsyncBoundary, StatusBadge
- **Reuse:** Feature-specific orchestration using shared domain and UI components
- **Input Sources:**
- **Local State:** Selected child card only.
- **States:** loading: Keep structural headings and announce loading; disable duplicate dependent actions.; empty: Show a specific absence message and only permitted next action.; error: Field422,stale409,denied403/invisible404,expired401 and transient429/503 are distinct; show safe message/request_id and bounded retry.; success: Render authoritative returned DTO and invalidate relevant scoped query keys.; detail: Zero-child state offers first registration; missing/revoked child links never reveal sibling data.
- **Accessibility:** Semantic headings/labels,keyboard access,visible focus,live status,error association,200%reflow; never color alone.
- **Import Boundary:** May import shared and declared feature dependencies; generated API subset only.
- **Requirements:** PAR-006

| Prop | Type | Required | Source |
|---|---|---|---|
| None | Route/session controller obtains its own authorized state | — | No implicit client identity authority |

| Operation | Request schema | Response schema | Roles | Ownership / state |
|---|---|---|---|---|
| API-PARENT-DASHBOARD | API_PARENT_DASHBOARDRequest | DashboardView | parent | Authenticated verified parent owns an active family membership. Child list is filtered to active GuardianStudent links; an empty family is valid and does not require an existing child. |
| API-FAMILY-GET | API_FAMILY_GETRequest | FamilyView | parent | Authenticated verified parent owns an active family membership. Child list is filtered to active GuardianStudent links; an empty family is valid and does not require an existing child. |

## GuardianProfileForm

- **Kind:** feature
- **Surface:** parent
- **Responsibility:** Edit own contact/preferences and complete verified email change.
- **Chunk:** ZE-P10-C01
- **Expected Module:** apps/web/src/features/parent/GuardianProfileForm.tsx
- **Composition:** FormFields, AsyncBoundary
- **Reuse:** Feature-specific orchestration using shared domain and UI components
- **Input Sources:**
- **Local State:** Profile draft,email/password confirmation,optional preferences.
- **States:** loading: Keep structural headings and announce loading; disable duplicate dependent actions.; empty: Show a specific absence message and only permitted next action.; error: Field422,stale409,denied403/invisible404,expired401 and transient429/503 are distinct; show safe message/request_id and bounded retry.; success: Render authoritative returned DTO and invalidate relevant scoped query keys.; detail: Essential security/billing messages clearly nonoptional; new email waits for confirmation; secret token removed after consume.
- **Accessibility:** Semantic headings/labels,keyboard access,visible focus,live status,error association,200%reflow; never color alone.
- **Import Boundary:** May import shared and declared feature dependencies; generated API subset only.
- **Requirements:** AUTH-011, PAR-002, PAR-021

| Prop | Type | Required | Source |
|---|---|---|---|
| emailChangeToken | OneTimeToken | False | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |

| Operation | Request schema | Response schema | Roles | Ownership / state |
|---|---|---|---|---|
| API-PARENT-PROFILE | API_PARENT_PROFILERequest | GuardianView | parent | Authenticated principal owns this account/session/notification; server resolves subject, never trusts requested role. |
| API-PARENT-UPDATE | API_PARENT_UPDATERequest | GuardianView | parent | Authenticated principal owns this account/session/notification; server resolves subject, never trusts requested role. |
| API-PARENT-EMAIL-CHANGE | API_PARENT_EMAIL_CHANGERequest | Empty | parent | Authenticated principal owns this account/session/notification; server resolves subject, never trusts requested role. Reauthentication; new address never takes effect until verification. |
| API-PARENT-EMAIL-CONFIRM | API_PARENT_EMAIL_CONFIRMRequest | GuardianView | parent | Authenticated principal owns this account/session/notification; server resolves subject, never trusts requested role. |

## ChildProfileForm

- **Kind:** feature
- **Surface:** parent
- **Responsibility:** Register or edit required child name/age and optional minimized fields.
- **Chunk:** ZE-P10-C01
- **Expected Module:** apps/web/src/features/parent/ChildProfileForm.tsx
- **Composition:** FormFields, AsyncBoundary
- **Reuse:** Feature-specific orchestration using shared domain and UI components
- **Input Sources:**
- **Local State:** Name1–80,required age4–18,nullable school<=160,closed school-year/interests/experience values.
- **States:** loading: Keep structural headings and announce loading; disable duplicate dependent actions.; empty: Show a specific absence message and only permitted next action.; error: Field422,stale409,denied403/invisible404,expired401 and transient429/503 are distinct; show safe message/request_id and bounded retry.; success: Render authoritative returned DTO and invalidate relevant scoped query keys.; detail: Age date server-assigned; stale age confirmed explicitly; school/surname/preferred name optional; new child initially linked atomically.
- **Accessibility:** Semantic headings/labels,keyboard access,visible focus,live status,error association,200%reflow; never color alone.
- **Import Boundary:** May import shared and declared feature dependencies; generated API subset only.
- **Requirements:** PAR-005

| Prop | Type | Required | Source |
|---|---|---|---|
| studentId | Uuid | False | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |

| Operation | Request schema | Response schema | Roles | Ownership / state |
|---|---|---|---|---|
| API-STUDENT-CREATE | API_STUDENT_CREATERequest | StudentProfileView | parent | Authenticated verified parent owns an active family membership. Child list is filtered to active GuardianStudent links; an empty family is valid and does not require an existing child. Create StudentProfile and verified GuardianStudent link to requesting parent atomically in same family; no pre-existing child required. |
| API-STUDENT-GET | API_STUDENT_GETRequest | StudentProfileView | parent | Active verified GuardianStudent link for requested student within principal family; deny revoked links and unrelated family IDs. |
| API-STUDENT-UPDATE | API_STUDENT_UPDATERequest | StudentProfileView | parent | Active verified GuardianStudent link for requested student within principal family; deny revoked links and unrelated family IDs. |
| API-STUDENT-AGE | API_STUDENT_AGERequest | StudentProfileView | parent | Active verified GuardianStudent link for requested student within principal family; deny revoked links and unrelated family IDs. |

## ChildCredentialsPanel

- **Kind:** feature
- **Surface:** parent
- **Responsibility:** Provision or rotate linked child nonpublic alias and one-time secret after guardian step-up.
- **Chunk:** ZE-P10-C01
- **Expected Module:** apps/web/src/features/parent/ChildCredentialsPanel.tsx
- **Composition:** FormFields, ConfirmActionDialog
- **Reuse:** Feature-specific orchestration using shared domain and UI components
- **Input Sources:**
- **Local State:** Guardian password and transient once-only credentials.
- **States:** loading: Keep structural headings and announce loading; disable duplicate dependent actions.; empty: Show a specific absence message and only permitted next action.; error: Field422,stale409,denied403/invisible404,expired401 and transient429/503 are distinct; show safe message/request_id and bounded retry.; success: Render authoritative returned DTO and invalidate relevant scoped query keys.; detail: Warn that existing student sessions are revoked; no email requirement; secret never persisted or automatically copied.
- **Accessibility:** Accessible show/copy secret action with clear once-only presentation.
- **Import Boundary:** May import shared and declared feature dependencies; generated API subset only.
- **Requirements:** PAR-005

| Prop | Type | Required | Source |
|---|---|---|---|
| studentId | Uuid | True | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |

| Operation | Request schema | Response schema | Roles | Ownership / state |
|---|---|---|---|---|
| API-STUDENT-GET | API_STUDENT_GETRequest | StudentProfileView | parent | Active verified GuardianStudent link for requested student within principal family; deny revoked links and unrelated family IDs. |
| API-STUDENT-CREDENTIALS | API_STUDENT_CREDENTIALSRequest | StudentCredentialsView | parent | Active verified GuardianStudent link for requested student within principal family; deny revoked links and unrelated family IDs. Guardian password reauthentication; revoke prior student sessions. |

## ConsentPanel

- **Kind:** feature
- **Surface:** parent
- **Responsibility:** Read required effective policy versions and record adult family/child acknowledgement.
- **Chunk:** ZE-P10-C01
- **Expected Module:** apps/web/src/features/parent/ConsentPanel.tsx
- **Composition:** FormFields, AsyncBoundary
- **Reuse:** Feature-specific orchestration using shared domain and UI components
- **Input Sources:**
- **Local State:** Selected unacknowledged policy IDs and optional linked-child scope.
- **States:** loading: Keep structural headings and announce loading; disable duplicate dependent actions.; empty: Show a specific absence message and only permitted next action.; error: Field422,stale409,denied403/invisible404,expired401 and transient429/503 are distinct; show safe message/request_id and bounded retry.; success: Render authoritative returned DTO and invalidate relevant scoped query keys.; detail: Stale policy refreshes required version; previous immutable acknowledgements remain visible.
- **Accessibility:** Semantic headings/labels,keyboard access,visible focus,live status,error association,200%reflow; never color alone.
- **Import Boundary:** May import shared and declared feature dependencies; generated API subset only.
- **Requirements:** PAR-004, SEC-003

| Prop | Type | Required | Source |
|---|---|---|---|
| studentId | Uuid | False | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |

| Operation | Request schema | Response schema | Roles | Ownership / state |
|---|---|---|---|---|
| API-POLICY-LIST | API_POLICY_LISTRequest | PolicyViewPage | public | Only explicitly published projection; no private child, roster, billing or operational data. |
| API-CONSENT-LIST | API_CONSENT_LISTRequest | AcknowledgementViewPage | parent | Authenticated verified parent owns an active family membership. Child list is filtered to active GuardianStudent links; an empty family is valid and does not require an existing child. If student_id is supplied, additionally require active explicit child link. |
| API-CONSENT-ACK | API_CONSENT_ACKRequest | AcknowledgementView | parent | Active verified GuardianStudent link for requested student within principal family; deny revoked links and unrelated family IDs. |

## FamilyPrivacyRequests

- **Kind:** feature
- **Surface:** parent
- **Responsibility:** Request verified access/correction/deletion/closure and retrieve approved own export.
- **Chunk:** ZE-P10-C01
- **Expected Module:** apps/web/src/features/parent/FamilyPrivacyRequests.tsx
- **Composition:** FormFields, ResourceTable, ProtectedDownloadAction
- **Reuse:** Feature-specific orchestration using shared domain and UI components
- **Input Sources:** Family GET.students supplies optional named child scope; requests list supplies request.id for approved export retrieval. Never accept another family child ID or infer approval from a local flag.
- **Local State:** Request kind/details/student scope/password in memory.
- **States:** loading: Keep structural headings and announce loading; disable duplicate dependent actions.; empty: Show a specific absence message and only permitted next action.; error: Field422,stale409,denied403/invisible404,expired401 and transient429/503 are distinct; show safe message/request_id and bounded retry.; success: Render authoritative returned DTO and invalidate relevant scoped query keys.; detail: No request automatically deletes data; show decision state/reason; export only ready approved request; no other guardian finances.
- **Accessibility:** Semantic headings/labels,keyboard access,visible focus,live status,error association,200%reflow; never color alone.
- **Import Boundary:** May import shared and declared feature dependencies; generated API subset only.
- **Requirements:** PAR-006, SEC-001, SEC-002, SEC-008, SEC-009, SEC-010

| Prop | Type | Required | Source |
|---|---|---|---|
| None | Route/session controller obtains its own authorized state | — | No implicit client identity authority |

| Operation | Request schema | Response schema | Roles | Ownership / state |
|---|---|---|---|---|
| API-PARENT-PRIVACY-REQUEST | API_PARENT_PRIVACY_REQUESTRequest | PrivacyRequestView | parent | Authenticated verified parent owns an active family membership. Child list is filtered to active GuardianStudent links; an empty family is valid and does not require an existing child. If student_id is supplied, additionally require active explicit child link. |
| API-PARENT-PRIVACY-LIST | API_PARENT_PRIVACY_LISTRequest | PrivacyRequestViewPage | parent | Authenticated verified parent owns an active family membership. Child list is filtered to active GuardianStudent links; an empty family is valid and does not require an existing child. If student_id is supplied, additionally require active explicit child link. |
| API-PARENT-PRIVACY-EXPORT | API_PARENT_PRIVACY_EXPORTRequest | DownloadTicketView | parent | Active verified GuardianStudent link for requested student within principal family; deny revoked links and unrelated family IDs. Approved access request only; exclude unrelated guardian finances. |
| API-FAMILY-GET | API_FAMILY_GETRequest | FamilyView | parent | Authenticated verified parent owns an active family membership. Child list is filtered to active GuardianStudent links; an empty family is valid and does not require an existing child. |

## ParentCheckout

- **Kind:** feature
- **Surface:** parent
- **Responsibility:** Select linked child/cohort,show server fee and terms,then create hosted checkout.
- **Chunk:** ZE-P10-C02
- **Expected Module:** apps/web/src/features/parent/ParentCheckout.tsx
- **Composition:** FormFields, MoneyText, ScheduleView, ConsentPanel, ChildProfileForm
- **Reuse:** Feature-specific orchestration using shared domain and UI components
- **Input Sources:**
- **Local State:** Child/cohort/policy selections and per-intent idempotency key.
- **States:** loading: Keep structural headings and announce loading; disable duplicate dependent actions.; empty: Show a specific absence message and only permitted next action.; error: Field422,stale409,denied403/invisible404,expired401 and transient429/503 are distinct; show safe message/request_id and bounded retry.; success: Render authoritative returned DTO and invalidate relevant scoped query keys.; detail: Validate current choice on server; full/age-stale/policy-stale errors link to appropriate form; checkout URL from server only; no client amount field.
- **Accessibility:** Semantic headings/labels,keyboard access,visible focus,live status,error association,200%reflow; never color alone.
- **Import Boundary:** May import shared and declared feature dependencies; generated API subset only.
- **Requirements:** LRN-001, PAR-004, PAR-006, PAR-017, PAR-018, PAR-019, PAR-020, PAY-002, PAY-003, PAY-006, PAY-007, PAY-009, PAY-011, PAY-012, SEC-003, WEB-001, WEB-002, WEB-003, WEB-004, WEB-007, WEB-008, WEB-009, WEB-012

| Prop | Type | Required | Source |
|---|---|---|---|
| courseSlug | string | True | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |
| initialCohortId | Uuid | False | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |
| initialStudentId | Uuid | False | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |

| Operation | Request schema | Response schema | Roles | Ownership / state |
|---|---|---|---|---|
| API-FAMILY-GET | API_FAMILY_GETRequest | FamilyView | parent | Authenticated verified parent owns an active family membership. Child list is filtered to active GuardianStudent links; an empty family is valid and does not require an existing child. |
| API-PUBLIC-COURSE | API_PUBLIC_COURSERequest | PublicCourseView | public | Only explicitly published projection; no private child, roster, billing or operational data. |
| API-PUBLIC-COHORTS | API_PUBLIC_COHORTSRequest | PublicCohortViewPage | public | Only explicitly published projection; no private child, roster, billing or operational data. |
| API-CONSENT-LIST | API_CONSENT_LISTRequest | AcknowledgementViewPage | parent | Authenticated verified parent owns an active family membership. Child list is filtered to active GuardianStudent links; an empty family is valid and does not require an existing child. If student_id is supplied, additionally require active explicit child link. |
| API-POLICY-LIST | API_POLICY_LISTRequest | PolicyViewPage | public | Only explicitly published projection; no private child, roster, billing or operational data. |
| API-PARENT-CHECKOUT | API_PARENT_CHECKOUTRequest | CheckoutSessionView | parent | Active verified GuardianStudent link for requested student within principal family; deny revoked links and unrelated family IDs. Parent principal has active billing membership in payment family; child link alone grants no billing rights; child eligibility additionally checked for checkout. Verified email; age reconfirmed within180d; current required consents. |

## FamilyBillingHistory

- **Kind:** feature
- **Surface:** parent
- **Responsibility:** Read own billing-family payments and eligible receipt/refund status.
- **Chunk:** ZE-P10-C02
- **Expected Module:** apps/web/src/features/parent/FamilyBillingHistory.tsx
- **Composition:** ResourceTable, MoneyText, StatusBadge
- **Reuse:** Feature-specific orchestration using shared domain and UI components
- **Input Sources:**
- **Local State:** Status filter/cursor in URL.
- **States:** loading: Keep structural headings and announce loading; disable duplicate dependent actions.; empty: Show a specific absence message and only permitted next action.; error: Field422,stale409,denied403/invisible404,expired401 and transient429/503 are distinct; show safe message/request_id and bounded retry.; success: Render authoritative returned DTO and invalidate relevant scoped query keys.; detail: Empty legitimate no-purchase state;403 billing membership denied even if child linkage exists.
- **Accessibility:** Semantic headings/labels,keyboard access,visible focus,live status,error association,200%reflow; never color alone.
- **Import Boundary:** May import shared and declared feature dependencies; generated API subset only.
- **Requirements:** PAR-017, PAR-018, PAR-019, PAR-020, PAY-002, PAY-003, PAY-006, PAY-007, PAY-009, PAY-011, PAY-012

| Prop | Type | Required | Source |
|---|---|---|---|
| None | Route/session controller obtains its own authorized state | — | No implicit client identity authority |

| Operation | Request schema | Response schema | Roles | Ownership / state |
|---|---|---|---|---|
| API-PARENT-PAYMENTS | API_PARENT_PAYMENTSRequest | PaymentViewPage | parent | Parent principal has active billing membership in payment family; child link alone grants no billing rights; child eligibility additionally checked for checkout. |

## FamilyPaymentDetail

- **Kind:** feature
- **Surface:** parent
- **Responsibility:** Track authoritative payment state,hosted checkout retry,documents and refund outcomes.
- **Chunk:** ZE-P10-C02
- **Expected Module:** apps/web/src/features/parent/FamilyPaymentDetail.tsx
- **Composition:** MoneyText, StatusBadge, ProtectedDownloadAction, ConfirmActionDialog
- **Reuse:** Feature-specific orchestration using shared domain and UI components
- **Input Sources:**
- **Local State:** Polling state,return flag and retry/hold-cancel intent.
- **States:** loading: Keep structural headings and announce loading; disable duplicate dependent actions.; empty: Show a specific absence message and only permitted next action.; error: Field422,stale409,denied403/invisible404,expired401 and transient429/503 are distinct; show safe message/request_id and bounded retry.; success: Render authoritative returned DTO and invalidate relevant scoped query keys.; detail: Browser return never success proof; pending/failed/expired/exception distinct; hold cancellation uses returned enrolment_id; no administrative refund controls.
- **Accessibility:** Semantic headings/labels,keyboard access,visible focus,live status,error association,200%reflow; never color alone.
- **Import Boundary:** May import shared and declared feature dependencies; generated API subset only.
- **Requirements:** ENR-001, ENR-002, ENR-003, ENR-004, ENR-005, ENR-006, ENR-007, PAR-008, PAR-017, PAR-018, PAR-019, PAR-020, PAY-002, PAY-003, PAY-006, PAY-007, PAY-008, PAY-009, PAY-011, PAY-012

| Prop | Type | Required | Source |
|---|---|---|---|
| paymentId | Uuid | True | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |
| fromCheckoutReturn | boolean | False | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |

| Operation | Request schema | Response schema | Roles | Ownership / state |
|---|---|---|---|---|
| API-PARENT-PAYMENT | API_PARENT_PAYMENTRequest | PaymentView | parent | Parent principal has active billing membership in payment family; child link alone grants no billing rights; child eligibility additionally checked for checkout. |
| API-PARENT-CHECKOUT-RETRY | API_PARENT_CHECKOUT_RETRYRequest | CheckoutSessionView | parent | Parent principal has active billing membership in payment family; child link alone grants no billing rights; child eligibility additionally checked for checkout. |
| API-PARENT-RECEIPTS | API_PARENT_RECEIPTSRequest | ReceiptViewPage | parent | Parent principal has active billing membership in payment family; child link alone grants no billing rights; child eligibility additionally checked for checkout. |
| API-PARENT-REFUNDS | API_PARENT_REFUNDSRequest | RefundViewPage | parent | Parent principal has active billing membership in payment family; child link alone grants no billing rights; child eligibility additionally checked for checkout. |
| API-PARENT-CHECKOUT-CANCEL | API_PARENT_CHECKOUT_CANCELRequest | EnrolmentView | parent | Active verified GuardianStudent link for requested student within principal family; deny revoked links and unrelated family IDs. Held/pending payment only; provider expiry reconciled. |

## ChildLearningOverview

- **Kind:** feature
- **Surface:** parent
- **Responsibility:** Read linked child enrolments,progress and attendance summaries.
- **Chunk:** ZE-P10-C03
- **Expected Module:** apps/web/src/features/parent/ChildLearningOverview.tsx
- **Composition:** ProgressSummary, ResourceTable, StatusBadge
- **Reuse:** Feature-specific orchestration using shared domain and UI components
- **Input Sources:**
- **Local State:** Selected cohort filter.
- **States:** loading: Keep structural headings and announce loading; disable duplicate dependent actions.; empty: Show a specific absence message and only permitted next action.; error: Field422,stale409,denied403/invisible404,expired401 and transient429/503 are distinct; show safe message/request_id and bounded retry.; success: Render authoritative returned DTO and invalidate relevant scoped query keys.; detail: Released/own educational evidence only; parent cannot change progress or attendance.
- **Accessibility:** Semantic headings/labels,keyboard access,visible focus,live status,error association,200%reflow; never color alone.
- **Import Boundary:** May import shared and declared feature dependencies; generated API subset only.
- **Requirements:** CLS-010, ENR-001, ENR-002, ENR-003, ENR-004, ENR-005, ENR-006, ENR-007, LRN-007, LRN-008, PAR-008, PAR-010, PAR-011

| Prop | Type | Required | Source |
|---|---|---|---|
| studentId | Uuid | True | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |

| Operation | Request schema | Response schema | Roles | Ownership / state |
|---|---|---|---|---|
| API-PARENT-ENROLMENTS | API_PARENT_ENROLMENTSRequest | EnrolmentViewPage | parent | Active verified GuardianStudent link for requested student within principal family; deny revoked links and unrelated family IDs. |
| API-PARENT-PROGRESS | API_PARENT_PROGRESSRequest | ProgressViewPage | parent | Active verified GuardianStudent link for requested student within principal family; deny revoked links and unrelated family IDs. Released records only. |
| API-PARENT-ATTENDANCE | API_PARENT_ATTENDANCERequest | AttendanceViewPage | parent | Active verified GuardianStudent link for requested student within principal family; deny revoked links and unrelated family IDs. |

## ChildWorkResults

- **Kind:** feature
- **Surface:** parent
- **Responsibility:** Support child with assignment due state,submission history and released results/feedback.
- **Chunk:** ZE-P10-C03
- **Expected Module:** apps/web/src/features/parent/ChildWorkResults.tsx
- **Composition:** ResourceTable, ReleasedResultView
- **Reuse:** Feature-specific orchestration using shared domain and UI components
- **Input Sources:**
- **Local State:** Assignment/cohort filter and selected released record.
- **States:** loading: Keep structural headings and announce loading; disable duplicate dependent actions.; empty: Show a specific absence message and only permitted next action.; error: Field422,stale409,denied403/invisible404,expired401 and transient429/503 are distinct; show safe message/request_id and bounded retry.; success: Render authoritative returned DTO and invalidate relevant scoped query keys.; detail: Status projection never shows draft body/files; no submit-as-child or answer-key controls.
- **Accessibility:** Semantic headings/labels,keyboard access,visible focus,live status,error association,200%reflow; never color alone.
- **Import Boundary:** May import shared and declared feature dependencies; generated API subset only.
- **Requirements:** ASM-001, ASM-002, ASM-003, ASM-004, ASM-005, ASM-006, ASM-007, ASM-008, PAR-012, PAR-013

| Prop | Type | Required | Source |
|---|---|---|---|
| studentId | Uuid | True | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |

| Operation | Request schema | Response schema | Roles | Ownership / state |
|---|---|---|---|---|
| API-PARENT-ASSIGNMENTS | API_PARENT_ASSIGNMENTSRequest | AssignmentViewPage | parent | Active verified GuardianStudent link for requested student within principal family; deny revoked links and unrelated family IDs. |
| API-PARENT-SUBMISSIONS | API_PARENT_SUBMISSIONSRequest | ChildSubmissionStatusViewPage | parent | Active verified GuardianStudent link for requested student within principal family; deny revoked links and unrelated family IDs. |
| API-PARENT-ASSESSMENTS | API_PARENT_ASSESSMENTSRequest | AssessmentViewPage | parent | Active verified GuardianStudent link for requested student within principal family; deny revoked links and unrelated family IDs. Released records only. |
| API-PARENT-QUIZ-RESULTS | API_PARENT_QUIZ_RESULTSRequest | ChildQuizResultViewPage | parent | Active verified GuardianStudent link for requested student within principal family; deny revoked links and unrelated family IDs. |
| API-PARENT-FEEDBACK | API_PARENT_FEEDBACKRequest | FeedbackViewPage | parent | Active verified GuardianStudent link for requested student within principal family; deny revoked links and unrelated family IDs. Released records only. |

## ChildCertificates

- **Kind:** feature
- **Surface:** parent
- **Responsibility:** List linked child certificate status and authorize ready PDF download.
- **Chunk:** ZE-P10-C03
- **Expected Module:** apps/web/src/features/parent/ChildCertificates.tsx
- **Composition:** CertificateCard, AsyncBoundary
- **Reuse:** Feature-specific orchestration using shared domain and UI components
- **Input Sources:**
- **Local State:** No durable client state; transient presentation state only.
- **States:** loading: Keep structural headings and announce loading; disable duplicate dependent actions.; empty: Show a specific absence message and only permitted next action.; error: Field422,stale409,denied403/invisible404,expired401 and transient429/503 are distinct; show safe message/request_id and bounded retry.; success: Render authoritative returned DTO and invalidate relevant scoped query keys.; detail: Only certificate-purpose ready asset; revoked status clear; generic financial assets never sent to this grant.
- **Accessibility:** Semantic headings/labels,keyboard access,visible focus,live status,error association,200%reflow; never color alone.
- **Import Boundary:** May import shared and declared feature dependencies; generated API subset only.
- **Requirements:** ADM-023, FILE-001, FILE-002, FILE-003, FILE-004, FILE-005, FILE-006, FILE-007, LRN-009, LRN-010, PAR-014

| Prop | Type | Required | Source |
|---|---|---|---|
| studentId | Uuid | True | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |

| Operation | Request schema | Response schema | Roles | Ownership / state |
|---|---|---|---|---|
| API-PARENT-CERTIFICATES | API_PARENT_CERTIFICATESRequest | CertificateViewPage | parent | Active verified GuardianStudent link for requested student within principal family; deny revoked links and unrelated family IDs. Released records only. |
| API-FILE-GET | API_FILE_GETRequest | FileAssetView | parent, student, teacher, admin:education_admin, admin:operations_admin | FileAccessPolicy derives released curriculum, own submission, guardian link, teaching assignment or scoped admin purpose. Reject financial_document/financial_export purposes on this generic endpoint even for a parent; financial-specific BillingService/ReportingService grants are required. |
| API-FILE-DOWNLOAD | API_FILE_DOWNLOADRequest | DownloadTicketView | parent, student, teacher, admin:education_admin, admin:operations_admin | FileAccessPolicy validates ready state and linked resource scope; submission parents read only authorized child; internal files never learner-readable. Reject financial_document/financial_export purposes on this generic endpoint even for a parent; financial-specific BillingService/ReportingService grants are required. |

## ParentSchedule

- **Kind:** feature
- **Surface:** parent
- **Responsibility:** Show linked family schedule,class details,guardian-assisted learner join and calendar export.
- **Chunk:** ZE-P10-C03
- **Expected Module:** apps/web/src/features/parent/ParentSchedule.tsx
- **Composition:** ScheduleView, StatusBadge
- **Reuse:** Feature-specific orchestration using shared domain and UI components
- **Input Sources:** Family GET.students supplies named linked child id selection for schedule, join and calendar requests; session_id comes from the authorized schedule response. Recheck current guardian/enrolment at every action.
- **Local State:** Date range/display zone/child selection.
- **States:** loading: Keep structural headings and announce loading; disable duplicate dependent actions.; empty: Show a specific absence message and only permitted next action.; error: Field422,stale409,denied403/invisible404,expired401 and transient429/503 are distinct; show safe message/request_id and bounded retry.; success: Render authoritative returned DTO and invalidate relevant scoped query keys.; detail: Read-only schedule; join requires selected linked child and server window; calendar file labelled snapshot,portal links only.
- **Accessibility:** Semantic headings/labels,keyboard access,visible focus,live status,error association,200%reflow; never color alone.
- **Import Boundary:** May import shared and declared feature dependencies; generated API subset only.
- **Requirements:** CAL-001, CAL-002, CAL-003, CAL-004, CAL-005, CLS-002, CLS-003, CLS-004, CLS-006, CLS-007, CLS-008, CLS-009, CLS-011, PAR-006, PAR-009

| Prop | Type | Required | Source |
|---|---|---|---|
| sessionId | Uuid | False | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |
| studentId | Uuid | False | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |

| Operation | Request schema | Response schema | Roles | Ownership / state |
|---|---|---|---|---|
| API-PARENT-SCHEDULE | API_PARENT_SCHEDULERequest | ClassSessionViewPage | parent | Active verified GuardianStudent link for requested student within principal family; deny revoked links and unrelated family IDs. |
| API-PARENT-SESSION | API_PARENT_SESSIONRequest | ClassSessionView | parent | Active verified GuardianStudent link for requested student within principal family; deny revoked links and unrelated family IDs. |
| API-PARENT-JOIN | API_PARENT_JOINRequest | JoinLinkView | parent | Active verified GuardianStudent link for requested student within principal family; deny revoked links and unrelated family IDs. Active enrolment; now within start-15m through scheduled end; no host URL. |
| API-PARENT-CALENDAR | API_PARENT_CALENDARRequest | CalendarExport | parent | Active verified GuardianStudent link for requested student within principal family; deny revoked links and unrelated family IDs. |
| API-FAMILY-GET | API_FAMILY_GETRequest | FamilyView | parent | Authenticated verified parent owns an active family membership. Child list is filtered to active GuardianStudent links; an empty family is valid and does not require an existing child. |

## ParentCommunications

- **Kind:** feature
- **Surface:** parent
- **Responsibility:** Show relevant events/announcements and recipient inbox.
- **Chunk:** ZE-P10-C03
- **Expected Module:** apps/web/src/features/parent/ParentCommunications.tsx
- **Composition:** NotificationList, ResourceTable
- **Reuse:** Feature-specific orchestration using shared domain and UI components
- **Input Sources:**
- **Local State:** Tab/filter/cursor/read pending.
- **States:** loading: Keep structural headings and announce loading; disable duplicate dependent actions.; empty: Show a specific absence message and only permitted next action.; error: Field422,stale409,denied403/invisible404,expired401 and transient429/503 are distinct; show safe message/request_id and bounded retry.; success: Render authoritative returned DTO and invalidate relevant scoped query keys.; detail: Audience membership/current ownership rechecked; no family-wide shared unread state.
- **Accessibility:** Semantic headings/labels,keyboard access,visible focus,live status,error association,200%reflow; never color alone.
- **Import Boundary:** May import shared and declared feature dependencies; generated API subset only.
- **Requirements:** ADM-022, COM-001, COM-002, COM-003, COM-004, COM-005, COM-006, COM-007, COM-008, COM-009, PAR-003, PAR-015, PAR-016, TCH-015

| Prop | Type | Required | Source |
|---|---|---|---|
| tab | events\|announcements\|notifications | True | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |

| Operation | Request schema | Response schema | Roles | Ownership / state |
|---|---|---|---|---|
| API-PARENT-EVENTS | API_PARENT_EVENTSRequest | EventViewPage | parent | Active verified GuardianStudent link for requested student within principal family; deny revoked links and unrelated family IDs. Audience membership rechecked at read. |
| API-PARENT-ANNOUNCEMENTS | API_PARENT_ANNOUNCEMENTSRequest | AnnouncementViewPage | parent | Active verified GuardianStudent link for requested student within principal family; deny revoked links and unrelated family IDs. Audience membership rechecked at read. |
| API-NOTIFICATIONS | API_NOTIFICATIONSRequest | NotificationViewPage | parent, student, teacher, admin | Authenticated principal owns this account/session/notification; server resolves subject, never trusts requested role. |
| API-NOTIFICATION-READ | API_NOTIFICATION_READRequest | NotificationView | parent, student, teacher, admin | Authenticated principal owns this account/session/notification; server resolves subject, never trusts requested role. |

## StudentDashboard

- **Kind:** feature
- **Surface:** student
- **Responsibility:** Show own enrolled learning journey and safe next-action counts.
- **Chunk:** ZE-P10-C04
- **Expected Module:** apps/web/src/features/student/StudentDashboard.tsx
- **Composition:** PageHeader, ResourceTable, StatusBadge
- **Reuse:** Feature-specific orchestration using shared domain and UI components
- **Input Sources:**
- **Local State:** Chosen enrolled course.
- **States:** loading: Keep structural headings and announce loading; disable duplicate dependent actions.; empty: Show a specific absence message and only permitted next action.; error: Field422,stale409,denied403/invisible404,expired401 and transient429/503 are distinct; show safe message/request_id and bounded retry.; success: Render authoritative returned DTO and invalidate relevant scoped query keys.; detail: No payment/family admin fields or finance imports; empty dashboard guides learner to ask guardian.
- **Accessibility:** Semantic headings/labels,keyboard access,visible focus,live status,error association,200%reflow; never color alone.
- **Import Boundary:** May import shared/own-surface features only; no finance feature/client imports.
- **Requirements:** ENR-001, ENR-002, ENR-003, ENR-004, ENR-005, ENR-006, ENR-007, LRN-007, LRN-008, STU-016

| Prop | Type | Required | Source |
|---|---|---|---|
| None | Route/session controller obtains its own authorized state | — | No implicit client identity authority |

| Operation | Request schema | Response schema | Roles | Ownership / state |
|---|---|---|---|---|
| API-STUDENT-DASHBOARD | API_STUDENT_DASHBOARDRequest | DashboardView | student | Student principal identity equals resource student_id; active/completed eligible enrolment and released pinned curriculum; no finances. |
| API-STUDENT-ENROLMENTS | API_STUDENT_ENROLMENTSRequest | EnrolmentViewPage | student | Student principal identity equals resource student_id; active/completed eligible enrolment and released pinned curriculum; no finances. |

## EnrolledCourseJourney

- **Kind:** feature
- **Surface:** student
- **Responsibility:** Navigate released modules and lessons of the cohort-pinned curriculum.
- **Chunk:** ZE-P10-C04
- **Expected Module:** apps/web/src/features/student/EnrolledCourseJourney.tsx
- **Composition:** PageHeader, ModuleNavigation, AsyncBoundary
- **Reuse:** Feature-specific orchestration using shared domain and UI components
- **Input Sources:**
- **Local State:** Expanded module and active lesson; identifiers from returned released hierarchy.
- **States:** loading: Keep structural headings and announce loading; disable duplicate dependent actions.; empty: Show a specific absence message and only permitted next action.; error: Field422,stale409,denied403/invisible404,expired401 and transient429/503 are distinct; show safe message/request_id and bounded retry.; success: Render authoritative returned DTO and invalidate relevant scoped query keys.; detail: Unreleased IDs produce404 with no title/answer leak; no duplicate curriculum per cohort.
- **Accessibility:** Semantic headings/labels,keyboard access,visible focus,live status,error association,200%reflow; never color alone.
- **Import Boundary:** May import shared/own-surface features only; no finance feature/client imports.
- **Requirements:** LRN-002, LRN-003, LRN-004, STU-003, STU-004

| Prop | Type | Required | Source |
|---|---|---|---|
| enrolmentId | Uuid | True | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |

| Operation | Request schema | Response schema | Roles | Ownership / state |
|---|---|---|---|---|
| API-STUDENT-CURRICULUM | API_STUDENT_CURRICULUMRequest | CurriculumRevisionView | student | Student principal identity equals resource student_id; active/completed eligible enrolment and released pinned curriculum; no finances. |
| API-STUDENT-RESOURCE | API_STUDENT_RESOURCERequest | ResourceViewPage | student | Student principal identity equals resource student_id; active/completed eligible enrolment and released pinned curriculum; no finances. |

## ModuleNavigation

- **Kind:** domain
- **Surface:** shared
- **Responsibility:** Render ordered released module/lesson navigation from supplied safe DTO.
- **Chunk:** ZE-P10-C04
- **Expected Module:** apps/web/src/components/shared/ModuleNavigation.tsx
- **Composition:**
- **Reuse:** Shared presentation/domain composition
- **Input Sources:**
- **Local State:** Expanded sections only.
- **States:** loading: Keep structural headings and announce loading; disable duplicate dependent actions.; empty: Show a specific absence message and only permitted next action.; error: Field422,stale409,denied403/invisible404,expired401 and transient429/503 are distinct; show safe message/request_id and bounded retry.; success: Render authoritative returned DTO and invalidate relevant scoped query keys.; detail: Never infer unreleased title from sequence gaps.
- **Accessibility:** Tree/disclosure keyboard semantics or simple nested links; aria-current lesson.
- **Import Boundary:** Shared components accept data/callbacks and import no role-feature tree.
- **Requirements:** NFR-003, NFR-004, NFR-006

| Prop | Type | Required | Source |
|---|---|---|---|
| curriculum | CurriculumRevisionView | True | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |
| activeLessonId | Uuid | False | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |
| onSelect | LessonSelectionHandler | True | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |

| Operation | Request schema | Response schema | Roles | Ownership / state |
|---|---|---|---|---|
| None | Typed supplied props | Presentation callbacks | Caller owns authorization | No autonomous provider/API access |

## LessonExperience

- **Kind:** feature
- **Surface:** student
- **Responsibility:** Render all supported typed lesson blocks and own lesson/activity completion.
- **Chunk:** ZE-P10-C04
- **Expected Module:** apps/web/src/features/student/LessonExperience.tsx
- **Composition:** PageHeader, LessonRenderer, AsyncBoundary
- **Reuse:** Feature-specific orchestration using shared domain and UI components
- **Input Sources:**
- **Local State:** Own activity reflection draft and completion action pending; no private localStorage.
- **States:** loading: Keep structural headings and announce loading; disable duplicate dependent actions.; empty: Show a specific absence message and only permitted next action.; error: Field422,stale409,denied403/invisible404,expired401 and transient429/503 are distinct; show safe message/request_id and bounded retry.; success: Render authoritative returned DTO and invalidate relevant scoped query keys.; detail: Only released ready resources; save reflection via own activity API; lesson completion acknowledgement uses server response; graded results not computed here.
- **Accessibility:** Semantic headings/labels,keyboard access,visible focus,live status,error association,200%reflow; never color alone.
- **Import Boundary:** May import shared/own-surface features only; no finance feature/client imports.
- **Requirements:** ADM-023, FILE-001, FILE-002, FILE-003, FILE-004, FILE-005, FILE-006, FILE-007, LRN-002, LRN-003, LRN-004, LRN-007, LRN-008, STU-003, STU-004, STU-016

| Prop | Type | Required | Source |
|---|---|---|---|
| enrolmentId | Uuid | True | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |
| lessonId | Uuid | True | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |

| Operation | Request schema | Response schema | Roles | Ownership / state |
|---|---|---|---|---|
| API-STUDENT-LESSON | API_STUDENT_LESSONRequest | LessonView | student | Student principal identity equals resource student_id; active/completed eligible enrolment and released pinned curriculum; no finances. |
| API-STUDENT-ACTIVITY-GET | API_STUDENT_ACTIVITY_GETRequest | ActivityCompletionViewPage | student | Student principal identity equals resource student_id; active/completed eligible enrolment and released pinned curriculum; no finances. |
| API-STUDENT-ACTIVITY | API_STUDENT_ACTIVITYRequest | ActivityCompletionView | student | Student principal identity equals resource student_id; active/completed eligible enrolment and released pinned curriculum; no finances. |
| API-STUDENT-LESSON-COMPLETE | API_STUDENT_LESSON_COMPLETERequest | ActivityCompletionView | student | Student principal identity equals resource student_id; active/completed eligible enrolment and released pinned curriculum; no finances. |
| API-FILE-GET | API_FILE_GETRequest | FileAssetView | parent, student, teacher, admin:education_admin, admin:operations_admin | FileAccessPolicy derives released curriculum, own submission, guardian link, teaching assignment or scoped admin purpose. Reject financial_document/financial_export purposes on this generic endpoint even for a parent; financial-specific BillingService/ReportingService grants are required. |
| API-FILE-DOWNLOAD | API_FILE_DOWNLOADRequest | DownloadTicketView | parent, student, teacher, admin:education_admin, admin:operations_admin | FileAccessPolicy validates ready state and linked resource scope; submission parents read only authorized child; internal files never learner-readable. Reject financial_document/financial_export purposes on this generic endpoint even for a parent; financial-specific BillingService/ReportingService grants are required. |

## LessonRenderer

- **Kind:** domain
- **Surface:** shared
- **Responsibility:** Dispatch closed LessonBlockView.kind variants in documented order; reject unknown/unvalidated payload.
- **Chunk:** ZE-P10-C04
- **Expected Module:** apps/web/src/components/shared/LessonRenderer.tsx
- **Composition:** HeadingBlock, RichTextBlock, ImageBlock, VideoBlock, DownloadBlock, ActivityBlock, QuizReferenceBlock, AssignmentReferenceBlock
- **Reuse:** Shared presentation/domain composition
- **Input Sources:**
- **Local State:** No durable state; delegated child interaction.
- **States:** loading: Keep structural headings and announce loading; disable duplicate dependent actions.; empty: Show a specific absence message and only permitted next action.; error: Field422,stale409,denied403/invisible404,expired401 and transient429/503 are distinct; show safe message/request_id and bounded retry.; success: Render authoritative returned DTO and invalidate relevant scoped query keys.; detail: Learner mode cannot load teacher/admin draft DTO; referenced activities use owning lesson/enrolment context.
- **Accessibility:** Semantic headings/labels,keyboard access,visible focus,live status,error association,200%reflow; never color alone.
- **Import Boundary:** Shared components accept data/callbacks and import no role-feature tree.
- **Requirements:** NFR-003, NFR-004, NFR-006

| Prop | Type | Required | Source |
|---|---|---|---|
| lesson | LessonView | True | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |
| mode | student\|teacher | True | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |
| actions | LessonActionAdapters | True | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |

| Operation | Request schema | Response schema | Roles | Ownership / state |
|---|---|---|---|---|
| None | Typed supplied props | Presentation callbacks | Caller owns authorization | No autonomous provider/API access |

## HeadingBlock

- **Kind:** domain
- **Surface:** shared
- **Responsibility:** Render validated semantic lesson heading.
- **Chunk:** ZE-P10-C04
- **Expected Module:** apps/web/src/components/shared/HeadingBlock.tsx
- **Composition:**
- **Reuse:** Shared presentation/domain composition
- **Input Sources:**
- **Local State:** Local interaction only.
- **States:** loading: Keep structural headings and announce loading; disable duplicate dependent actions.; empty: Show a specific absence message and only permitted next action.; error: Field422,stale409,denied403/invisible404,expired401 and transient429/503 are distinct; show safe message/request_id and bounded retry.; success: Render authoritative returned DTO and invalidate relevant scoped query keys.; detail: Normalize hierarchy relative to page h1 without decorative-only heading.
- **Accessibility:** Semantic heading order.
- **Import Boundary:** Shared components accept data/callbacks and import no role-feature tree.
- **Requirements:** LRN-003, NFR-003, STU-004

| Prop | Type | Required | Source |
|---|---|---|---|
| content | HeadingBlockContent | True | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |
| mode | student\|teacher | True | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |
| actions | LessonActionAdapters | True | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |

| Operation | Request schema | Response schema | Roles | Ownership / state |
|---|---|---|---|---|
| None | Typed supplied props | Presentation callbacks | Caller owns authorization | No autonomous provider/API access |

## RichTextBlock

- **Kind:** domain
- **Surface:** shared
- **Responsibility:** Render approved sanitized instructional text.
- **Chunk:** ZE-P10-C04
- **Expected Module:** apps/web/src/components/shared/RichTextBlock.tsx
- **Composition:**
- **Reuse:** Shared presentation/domain composition
- **Input Sources:**
- **Local State:** Local interaction only.
- **States:** loading: Keep structural headings and announce loading; disable duplicate dependent actions.; empty: Show a specific absence message and only permitted next action.; error: Field422,stale409,denied403/invisible404,expired401 and transient429/503 are distinct; show safe message/request_id and bounded retry.; success: Render authoritative returned DTO and invalidate relevant scoped query keys.; detail: No arbitrary HTML/scripts; allowlisted semantic renderer.
- **Accessibility:** Readable text widths,lists and meaningful link labels.
- **Import Boundary:** Shared components accept data/callbacks and import no role-feature tree.
- **Requirements:** LRN-003, NFR-003, STU-004

| Prop | Type | Required | Source |
|---|---|---|---|
| content | RichTextBlockContent | True | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |
| mode | student\|teacher | True | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |
| actions | LessonActionAdapters | True | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |

| Operation | Request schema | Response schema | Roles | Ownership / state |
|---|---|---|---|---|
| None | Typed supplied props | Presentation callbacks | Caller owns authorization | No autonomous provider/API access |

## ImageBlock

- **Kind:** domain
- **Surface:** shared
- **Responsibility:** Render protected instructional image with alternative text.
- **Chunk:** ZE-P10-C04
- **Expected Module:** apps/web/src/components/shared/ImageBlock.tsx
- **Composition:** AsyncBoundary
- **Reuse:** Shared presentation/domain composition
- **Input Sources:**
- **Local State:** Local interaction only.
- **States:** loading: Keep structural headings and announce loading; disable duplicate dependent actions.; empty: Show a specific absence message and only permitted next action.; error: Field422,stale409,denied403/invisible404,expired401 and transient429/503 are distinct; show safe message/request_id and bounded retry.; success: Render authoritative returned DTO and invalidate relevant scoped query keys.; detail: Acquire authorized ready asset; image alt_text required; no permanent public object URL.
- **Accessibility:** Useful alt text and optional expanded view with focus return.
- **Import Boundary:** Shared components accept data/callbacks and import no role-feature tree.
- **Requirements:** LRN-003, NFR-003, STU-004

| Prop | Type | Required | Source |
|---|---|---|---|
| content | ImageBlockContent | True | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |
| mode | student\|teacher | True | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |
| actions | LessonActionAdapters | True | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |

| Operation | Request schema | Response schema | Roles | Ownership / state |
|---|---|---|---|---|
| None | Typed supplied props | Presentation callbacks | Caller owns authorization | No autonomous provider/API access |

## VideoBlock

- **Kind:** domain
- **Surface:** shared
- **Responsibility:** Render approved MP4/HTTPS video with captions or transcript.
- **Chunk:** ZE-P10-C04
- **Expected Module:** apps/web/src/components/shared/VideoBlock.tsx
- **Composition:** AsyncBoundary
- **Reuse:** Shared presentation/domain composition
- **Input Sources:**
- **Local State:** Local interaction only.
- **States:** loading: Keep structural headings and announce loading; disable duplicate dependent actions.; empty: Show a specific absence message and only permitted next action.; error: Field422,stale409,denied403/invisible404,expired401 and transient429/503 are distinct; show safe message/request_id and bounded retry.; success: Render authoritative returned DTO and invalidate relevant scoped query keys.; detail: Only approved sources; paused until explicit play; no arbitrary embed; transcript available.
- **Accessibility:** Keyboard player controls,captions/transcript,playback controls; no autoplay audio.
- **Import Boundary:** Shared components accept data/callbacks and import no role-feature tree.
- **Requirements:** LRN-003, NFR-003, STU-004

| Prop | Type | Required | Source |
|---|---|---|---|
| content | VideoBlockContent | True | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |
| mode | student\|teacher | True | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |
| actions | LessonActionAdapters | True | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |

| Operation | Request schema | Response schema | Roles | Ownership / state |
|---|---|---|---|---|
| None | Typed supplied props | Presentation callbacks | Caller owns authorization | No autonomous provider/API access |

## DownloadBlock

- **Kind:** domain
- **Surface:** shared
- **Responsibility:** Offer authorized learning-resource download.
- **Chunk:** ZE-P10-C04
- **Expected Module:** apps/web/src/components/shared/DownloadBlock.tsx
- **Composition:** ProtectedDownloadAction
- **Reuse:** Shared presentation/domain composition
- **Input Sources:**
- **Local State:** Local interaction only.
- **States:** loading: Keep structural headings and announce loading; disable duplicate dependent actions.; empty: Show a specific absence message and only permitted next action.; error: Field422,stale409,denied403/invisible404,expired401 and transient429/503 are distinct; show safe message/request_id and bounded retry.; success: Render authoritative returned DTO and invalidate relevant scoped query keys.; detail: Resource ID/purpose ties to released current course; no financial file grant.
- **Accessibility:** Descriptive filename/type/size and accessible download button.
- **Import Boundary:** Shared components accept data/callbacks and import no role-feature tree.
- **Requirements:** LRN-003, NFR-003, STU-004

| Prop | Type | Required | Source |
|---|---|---|---|
| content | DownloadBlockContent | True | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |
| mode | student\|teacher | True | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |
| actions | LessonActionAdapters | True | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |

| Operation | Request schema | Response schema | Roles | Ownership / state |
|---|---|---|---|---|
| None | Typed supplied props | Presentation callbacks | Caller owns authorization | No autonomous provider/API access |

## ActivityBlock

- **Kind:** domain
- **Surface:** shared
- **Responsibility:** Show practice instructions and own completion/reflection controls in student mode.
- **Chunk:** ZE-P10-C04
- **Expected Module:** apps/web/src/components/shared/ActivityBlock.tsx
- **Composition:** FormFields
- **Reuse:** Shared presentation/domain composition
- **Input Sources:**
- **Local State:** Local interaction only.
- **States:** loading: Keep structural headings and announce loading; disable duplicate dependent actions.; empty: Show a specific absence message and only permitted next action.; error: Field422,stale409,denied403/invisible404,expired401 and transient429/503 are distinct; show safe message/request_id and bounded retry.; success: Render authoritative returned DTO and invalidate relevant scoped query keys.; detail: Teacher mode read-only; student sends own completion/reflection through supplied adapter.
- **Accessibility:** Short plain instructions; text-area labels; saved indicator without grading language.
- **Import Boundary:** Shared components accept data/callbacks and import no role-feature tree.
- **Requirements:** LRN-003, NFR-003, STU-004

| Prop | Type | Required | Source |
|---|---|---|---|
| content | ActivityBlockContent | True | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |
| mode | student\|teacher | True | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |
| actions | LessonActionAdapters | True | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |

| Operation | Request schema | Response schema | Roles | Ownership / state |
|---|---|---|---|---|
| None | Typed supplied props | Presentation callbacks | Caller owns authorization | No autonomous provider/API access |

## QuizReferenceBlock

- **Kind:** domain
- **Surface:** shared
- **Responsibility:** Link released quiz within current enrolment.
- **Chunk:** ZE-P10-C04
- **Expected Module:** apps/web/src/components/shared/QuizReferenceBlock.tsx
- **Composition:**
- **Reuse:** Shared presentation/domain composition
- **Input Sources:**
- **Local State:** Local interaction only.
- **States:** loading: Keep structural headings and announce loading; disable duplicate dependent actions.; empty: Show a specific absence message and only permitted next action.; error: Field422,stale409,denied403/invisible404,expired401 and transient429/503 are distinct; show safe message/request_id and bounded retry.; success: Render authoritative returned DTO and invalidate relevant scoped query keys.; detail: No answer key/proactive attempt start; link to quiz experience.
- **Accessibility:** Descriptive quiz action and attempt-state text.
- **Import Boundary:** Shared components accept data/callbacks and import no role-feature tree.
- **Requirements:** LRN-003, NFR-003, STU-004

| Prop | Type | Required | Source |
|---|---|---|---|
| content | QuizReferenceBlockContent | True | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |
| mode | student\|teacher | True | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |
| actions | LessonActionAdapters | True | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |

| Operation | Request schema | Response schema | Roles | Ownership / state |
|---|---|---|---|---|
| None | Typed supplied props | Presentation callbacks | Caller owns authorization | No autonomous provider/API access |

## AssignmentReferenceBlock

- **Kind:** domain
- **Surface:** shared
- **Responsibility:** Link assignment/project requirements within current enrolment.
- **Chunk:** ZE-P10-C04
- **Expected Module:** apps/web/src/components/shared/AssignmentReferenceBlock.tsx
- **Composition:**
- **Reuse:** Shared presentation/domain composition
- **Input Sources:**
- **Local State:** Local interaction only.
- **States:** loading: Keep structural headings and announce loading; disable duplicate dependent actions.; empty: Show a specific absence message and only permitted next action.; error: Field422,stale409,denied403/invisible404,expired401 and transient429/503 are distinct; show safe message/request_id and bounded retry.; success: Render authoritative returned DTO and invalidate relevant scoped query keys.; detail: Link references validated same revision; no automatic submission creation.
- **Accessibility:** Clear assignment/project label and next action.
- **Import Boundary:** Shared components accept data/callbacks and import no role-feature tree.
- **Requirements:** LRN-003, NFR-003, STU-004

| Prop | Type | Required | Source |
|---|---|---|---|
| content | AssignmentReferenceBlockContent | True | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |
| mode | student\|teacher | True | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |
| actions | LessonActionAdapters | True | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |

| Operation | Request schema | Response schema | Roles | Ownership / state |
|---|---|---|---|---|
| None | Typed supplied props | Presentation callbacks | Caller owns authorization | No autonomous provider/API access |

## StudentQuizExperience

- **Kind:** feature
- **Surface:** student
- **Responsibility:** Begin,save and submit own allowed quiz attempt,then show released formative correctness/explanation.
- **Chunk:** ZE-P10-C05
- **Expected Module:** apps/web/src/features/student/StudentQuizExperience.tsx
- **Composition:** FormFields, ReleasedResultView, ConfirmActionDialog
- **Reuse:** Feature-specific orchestration using shared domain and UI components
- **Input Sources:**
- **Local State:** Own selected options and dirty version,pending save/submit,stable idempotency key.
- **States:** loading: Keep structural headings and announce loading; disable duplicate dependent actions.; empty: Show a specific absence message and only permitted next action.; error: Field422,stale409,denied403/invisible404,expired401 and transient429/503 are distinct; show safe message/request_id and bounded retry.; success: Render authoritative returned DTO and invalidate relevant scoped query keys.; detail: Explicit save/submission; final submit disables editing; network retry same key; limit/replay/version errors refetch; no answer key in initial view.
- **Accessibility:** Radio/checkbox groups with legend; navigation does not require dragging; unsaved leave warning; no inaccessible timer.
- **Import Boundary:** May import shared/own-surface features only; no finance feature/client imports.
- **Requirements:** ASM-001, ASM-002, ASM-003, STU-007

| Prop | Type | Required | Source |
|---|---|---|---|
| enrolmentId | Uuid | True | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |
| quizId | Uuid | True | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |

| Operation | Request schema | Response schema | Roles | Ownership / state |
|---|---|---|---|---|
| API-STUDENT-QUIZ | API_STUDENT_QUIZRequest | LearnerQuizView | student | Student principal identity equals resource student_id; active/completed eligible enrolment and released pinned curriculum; no finances. |
| API-STUDENT-ATTEMPTS | API_STUDENT_ATTEMPTSRequest | QuizAttemptViewPage | student | Student principal identity equals resource student_id; active/completed eligible enrolment and released pinned curriculum; no finances. |
| API-STUDENT-ATTEMPT-CREATE | API_STUDENT_ATTEMPT_CREATERequest | QuizAttemptView | student | Student principal identity equals resource student_id; active/completed eligible enrolment and released pinned curriculum; no finances. |
| API-STUDENT-ATTEMPT-SAVE | API_STUDENT_ATTEMPT_SAVERequest | QuizAttemptView | student | Student principal identity equals resource student_id; active/completed eligible enrolment and released pinned curriculum; no finances. |
| API-STUDENT-ATTEMPT-SUBMIT | API_STUDENT_ATTEMPT_SUBMITRequest | QuizAttemptView | student | Student principal identity equals resource student_id; active/completed eligible enrolment and released pinned curriculum; no finances. |

## StudentAssignmentWork

- **Kind:** feature
- **Surface:** student
- **Responsibility:** Read assignment/project instructions,rubric,due time and immutable submission history; edit own allowed draft.
- **Chunk:** ZE-P10-C05
- **Expected Module:** apps/web/src/features/student/StudentAssignmentWork.tsx
- **Composition:** UploadControl, FormFields, ResourceTable, ConfirmActionDialog
- **Reuse:** Feature-specific orchestration using shared domain and UI components
- **Input Sources:**
- **Local State:** Body and selected ready asset IDs,current submission ID/version,upload pipeline and idempotency key.
- **States:** loading: Keep structural headings and announce loading; disable duplicate dependent actions.; empty: Show a specific absence message and only permitted next action.; error: Field422,stale409,denied403/invisible404,expired401 and transient429/503 are distinct; show safe message/request_id and bounded retry.; success: Render authoritative returned DTO and invalidate relevant scoped query keys.; detail: Assignment detail selected from authorized enrolment assignment list; individual file<=25MiB,total<=100MiB,max5; freeze on submit; returned permits new version; late flag server-authoritative.
- **Accessibility:** Accessible file progress/rubric/due timezone; clear saved vs submitted; no parent impersonation.
- **Import Boundary:** May import shared/own-surface features only; no finance feature/client imports.
- **Requirements:** ADM-023, ASM-004, ASM-005, FILE-001, FILE-002, FILE-003, FILE-004, FILE-005, FILE-006, FILE-007, STU-008, STU-009, STU-010

| Prop | Type | Required | Source |
|---|---|---|---|
| enrolmentId | Uuid | True | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |
| assignmentId | Uuid | True | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |

| Operation | Request schema | Response schema | Roles | Ownership / state |
|---|---|---|---|---|
| API-STUDENT-ASSIGNMENTS | API_STUDENT_ASSIGNMENTSRequest | AssignmentViewPage | student | Student principal identity equals resource student_id; active/completed eligible enrolment and released pinned curriculum; no finances. |
| API-STUDENT-SUBMISSIONS | API_STUDENT_SUBMISSIONSRequest | SubmissionViewPage | student | Student principal identity equals resource student_id; active/completed eligible enrolment and released pinned curriculum; no finances. |
| API-STUDENT-SUBMISSION-CREATE | API_STUDENT_SUBMISSION_CREATERequest | SubmissionView | student | Student principal identity equals resource student_id; active/completed eligible enrolment and released pinned curriculum; no finances. New attempt only if policy permits or prior attempt returned. |
| API-STUDENT-SUBMISSION-SAVE | API_STUDENT_SUBMISSION_SAVERequest | SubmissionView | student | Student principal identity equals resource student_id; active/completed eligible enrolment and released pinned curriculum; no finances. |
| API-STUDENT-SUBMISSION-SEND | API_STUDENT_SUBMISSION_SENDRequest | SubmissionView | student | Student principal identity equals resource student_id; active/completed eligible enrolment and released pinned curriculum; no finances. Late work accepted and labelled until cohort complete or explicitly closed. |
| API-STUDENT-SUBMISSION-DELETE | API_STUDENT_SUBMISSION_DELETERequest | Empty | student | Student principal identity equals resource student_id; active/completed eligible enrolment and released pinned curriculum; no finances. |
| API-FILE-UPLOAD | API_FILE_UPLOADRequest | UploadTicketView | student, admin:education_admin, admin:operations_admin | Student own draft submission only; admin matching purpose privilege. No parent upload feature. Resolve current FileUploadContext from purpose + context_id: submission -> Submission.id from owned draft submission create/detail, same authenticated student and eligible enrolment; resource -> CurriculumRevision.id from education-admin revision list/detail, must still be writable draft; internal/public_asset -> authenticated SessionView.user_id (the same Account.id as principal), current admin:operations_admin only. No caller-selected other account/context; certificate/financial_document/financial_export are server-generated and forbidden here. Recheck immutable owner/purpose/context on confirmation and deletion; publication/release or submission finalization races reject mutation. Scan promotion checks context still permits the asset before exposing it. |
| API-FILE-CONFIRM | API_FILE_CONFIRMRequest | FileAssetView | student, admin:education_admin, admin:operations_admin | Upload owner and same original scope; uploaded object metadata/checksum must match ticket. Resolve current FileUploadContext from purpose + context_id: submission -> Submission.id from owned draft submission create/detail, same authenticated student and eligible enrolment; resource -> CurriculumRevision.id from education-admin revision list/detail, must still be writable draft; internal/public_asset -> authenticated SessionView.user_id (the same Account.id as principal), current admin:operations_admin only. No caller-selected other account/context; certificate/financial_document/financial_export are server-generated and forbidden here. Recheck immutable owner/purpose/context on confirmation and deletion; publication/release or submission finalization races reject mutation. Scan promotion checks context still permits the asset before exposing it. |
| API-FILE-GET | API_FILE_GETRequest | FileAssetView | parent, student, teacher, admin:education_admin, admin:operations_admin | FileAccessPolicy derives released curriculum, own submission, guardian link, teaching assignment or scoped admin purpose. Reject financial_document/financial_export purposes on this generic endpoint even for a parent; financial-specific BillingService/ReportingService grants are required. |
| API-FILE-DOWNLOAD | API_FILE_DOWNLOADRequest | DownloadTicketView | parent, student, teacher, admin:education_admin, admin:operations_admin | FileAccessPolicy validates ready state and linked resource scope; submission parents read only authorized child; internal files never learner-readable. Reject financial_document/financial_export purposes on this generic endpoint even for a parent; financial-specific BillingService/ReportingService grants are required. |
| API-FILE-DELETE | API_FILE_DELETERequest | Empty | student, admin:education_admin, admin:operations_admin | No referenced submitted work/published resource/certificate deletion; retention and legal hold apply. Reject financial_document/financial_export purposes on this generic endpoint even for a parent; financial-specific BillingService/ReportingService grants are required. If-Match uses current FileAsset.version obtained from API-FILE-GET, upload confirmation or permitted asset listing; delete is owner-draft/purpose scoped and still checks linked resource state. Resolve current FileUploadContext from purpose + context_id: submission -> Submission.id from owned draft submission create/detail, same authenticated student and eligible enrolment; resource -> CurriculumRevision.id from education-admin revision list/detail, must still be writable draft; internal/public_asset -> authenticated SessionView.user_id (the same Account.id as principal), current admin:operations_admin only. No caller-selected other account/context; certificate/financial_document/financial_export are server-generated and forbidden here. Recheck immutable owner/purpose/context on confirmation and deletion; publication/release or submission finalization races reject mutation. Scan promotion checks context still permits the asset before exposing it. |

## StudentResults

- **Kind:** feature
- **Surface:** student
- **Responsibility:** Read own released assessments and feedback with progress/completion evidence.
- **Chunk:** ZE-P10-C06
- **Expected Module:** apps/web/src/features/student/StudentResults.tsx
- **Composition:** ReleasedResultView, ProgressSummary
- **Reuse:** Feature-specific orchestration using shared domain and UI components
- **Input Sources:**
- **Local State:** Cohort filter and selected result.
- **States:** loading: Keep structural headings and announce loading; disable duplicate dependent actions.; empty: Show a specific absence message and only permitted next action.; error: Field422,stale409,denied403/invisible404,expired401 and transient429/503 are distinct; show safe message/request_id and bounded retry.; success: Render authoritative returned DTO and invalidate relevant scoped query keys.; detail: Draft/withdrawn hidden; explicit incomplete/standard/admin_override basis supplied by backend; no client grade calculations.
- **Accessibility:** Semantic headings/labels,keyboard access,visible focus,live status,error association,200%reflow; never color alone.
- **Import Boundary:** May import shared/own-surface features only; no finance feature/client imports.
- **Requirements:** ASM-006, ASM-007, ASM-008, LRN-007, LRN-008, STU-011, STU-012, STU-016

| Prop | Type | Required | Source |
|---|---|---|---|
| None | Route/session controller obtains its own authorized state | — | No implicit client identity authority |

| Operation | Request schema | Response schema | Roles | Ownership / state |
|---|---|---|---|---|
| API-STUDENT-ASSESSMENTS | API_STUDENT_ASSESSMENTSRequest | AssessmentViewPage | student | Student principal identity equals resource student_id; active/completed eligible enrolment and released pinned curriculum; no finances. Released records only. |
| API-STUDENT-FEEDBACK | API_STUDENT_FEEDBACKRequest | FeedbackViewPage | student | Student principal identity equals resource student_id; active/completed eligible enrolment and released pinned curriculum; no finances. Released records only. |
| API-STUDENT-PROGRESS | API_STUDENT_PROGRESSRequest | ProgressViewPage | student | Student principal identity equals resource student_id; active/completed eligible enrolment and released pinned curriculum; no finances. Released records only. |

## StudentCertificates

- **Kind:** feature
- **Surface:** student
- **Responsibility:** View own course-completion certificates and protected artifact state.
- **Chunk:** ZE-P10-C06
- **Expected Module:** apps/web/src/features/student/StudentCertificates.tsx
- **Composition:** CertificateCard, AsyncBoundary
- **Reuse:** Feature-specific orchestration using shared domain and UI components
- **Input Sources:**
- **Local State:** No durable client state; transient presentation state only.
- **States:** loading: Keep structural headings and announce loading; disable duplicate dependent actions.; empty: Show a specific absence message and only permitted next action.; error: Field422,stale409,denied403/invisible404,expired401 and transient429/503 are distinct; show safe message/request_id and bounded retry.; success: Render authoritative returned DTO and invalidate relevant scoped query keys.; detail: Only own certificate-purpose ready asset; no public certificate directory.
- **Accessibility:** Semantic headings/labels,keyboard access,visible focus,live status,error association,200%reflow; never color alone.
- **Import Boundary:** May import shared/own-surface features only; no finance feature/client imports.
- **Requirements:** ADM-023, FILE-001, FILE-002, FILE-003, FILE-004, FILE-005, FILE-006, FILE-007, LRN-009, LRN-010, STU-017

| Prop | Type | Required | Source |
|---|---|---|---|
| None | Route/session controller obtains its own authorized state | — | No implicit client identity authority |

| Operation | Request schema | Response schema | Roles | Ownership / state |
|---|---|---|---|---|
| API-STUDENT-CERTIFICATES | API_STUDENT_CERTIFICATESRequest | CertificateViewPage | student | Student principal identity equals resource student_id; active/completed eligible enrolment and released pinned curriculum; no finances. Released records only. |
| API-FILE-GET | API_FILE_GETRequest | FileAssetView | parent, student, teacher, admin:education_admin, admin:operations_admin | FileAccessPolicy derives released curriculum, own submission, guardian link, teaching assignment or scoped admin purpose. Reject financial_document/financial_export purposes on this generic endpoint even for a parent; financial-specific BillingService/ReportingService grants are required. |
| API-FILE-DOWNLOAD | API_FILE_DOWNLOADRequest | DownloadTicketView | parent, student, teacher, admin:education_admin, admin:operations_admin | FileAccessPolicy validates ready state and linked resource scope; submission parents read only authorized child; internal files never learner-readable. Reject financial_document/financial_export purposes on this generic endpoint even for a parent; financial-specific BillingService/ReportingService grants are required. |

## StudentSchedule

- **Kind:** feature
- **Surface:** student
- **Responsibility:** Show own classes/details,join eligible live class and read attendance.
- **Chunk:** ZE-P10-C07
- **Expected Module:** apps/web/src/features/student/StudentSchedule.tsx
- **Composition:** ScheduleView, StatusBadge
- **Reuse:** Feature-specific orchestration using shared domain and UI components
- **Input Sources:**
- **Local State:** Date range/display timezone and join pending.
- **States:** loading: Keep structural headings and announce loading; disable duplicate dependent actions.; empty: Show a specific absence message and only permitted next action.; error: Field422,stale409,denied403/invisible404,expired401 and transient429/503 are distinct; show safe message/request_id and bounded retry.; success: Render authoritative returned DTO and invalidate relevant scoped query keys.; detail: Join window/cancellation/providerfailure shown from server; never host URL or edit scheduling.
- **Accessibility:** Semantic headings/labels,keyboard access,visible focus,live status,error association,200%reflow; never color alone.
- **Import Boundary:** May import shared/own-surface features only; no finance feature/client imports.
- **Requirements:** CLS-002, CLS-003, CLS-004, CLS-006, CLS-007, CLS-008, CLS-009, CLS-010, CLS-011, STU-013, STU-014, STU-015

| Prop | Type | Required | Source |
|---|---|---|---|
| sessionId | Uuid | False | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |

| Operation | Request schema | Response schema | Roles | Ownership / state |
|---|---|---|---|---|
| API-STUDENT-SCHEDULE | API_STUDENT_SCHEDULERequest | ClassSessionViewPage | student | Student principal identity equals resource student_id; active/completed eligible enrolment and released pinned curriculum; no finances. |
| API-STUDENT-SESSION | API_STUDENT_SESSIONRequest | ClassSessionView | student | Student principal identity equals resource student_id; active/completed eligible enrolment and released pinned curriculum; no finances. |
| API-STUDENT-JOIN | API_STUDENT_JOINRequest | JoinLinkView | student | Student principal identity equals resource student_id; active/completed eligible enrolment and released pinned curriculum; no finances. Active enrolment; now within start-15m through scheduled end; no host URL. |
| API-STUDENT-ATTENDANCE | API_STUDENT_ATTENDANCERequest | AttendanceViewPage | student | Student principal identity equals resource student_id; active/completed eligible enrolment and released pinned curriculum; no finances. |

## StudentCommunications

- **Kind:** feature
- **Surface:** student
- **Responsibility:** Read relevant announcements/events and own notification inbox.
- **Chunk:** ZE-P10-C07
- **Expected Module:** apps/web/src/features/student/StudentCommunications.tsx
- **Composition:** NotificationList, ResourceTable
- **Reuse:** Feature-specific orchestration using shared domain and UI components
- **Input Sources:**
- **Local State:** Tab/cursor/unread filter.
- **States:** loading: Keep structural headings and announce loading; disable duplicate dependent actions.; empty: Show a specific absence message and only permitted next action.; error: Field422,stale409,denied403/invisible404,expired401 and transient429/503 are distinct; show safe message/request_id and bounded retry.; success: Render authoritative returned DTO and invalidate relevant scoped query keys.; detail: No child marketing,peer messages or private staff operations.
- **Accessibility:** Semantic headings/labels,keyboard access,visible focus,live status,error association,200%reflow; never color alone.
- **Import Boundary:** May import shared/own-surface features only; no finance feature/client imports.
- **Requirements:** ADM-022, COM-001, COM-002, COM-003, COM-004, COM-005, COM-006, COM-007, COM-008, COM-009, PAR-016, STU-018, TCH-015

| Prop | Type | Required | Source |
|---|---|---|---|
| tab | announcements\|events\|notifications | True | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |

| Operation | Request schema | Response schema | Roles | Ownership / state |
|---|---|---|---|---|
| API-STUDENT-ANNOUNCEMENTS | API_STUDENT_ANNOUNCEMENTSRequest | AnnouncementViewPage | student | Student principal identity equals resource student_id; active/completed eligible enrolment and released pinned curriculum; no finances. Audience membership rechecked at read. |
| API-STUDENT-EVENTS | API_STUDENT_EVENTSRequest | EventViewPage | student | Student principal identity equals resource student_id; active/completed eligible enrolment and released pinned curriculum; no finances. Audience membership rechecked at read. |
| API-NOTIFICATIONS | API_NOTIFICATIONSRequest | NotificationViewPage | parent, student, teacher, admin | Authenticated principal owns this account/session/notification; server resolves subject, never trusts requested role. |
| API-NOTIFICATION-READ | API_NOTIFICATION_READRequest | NotificationView | parent, student, teacher, admin | Authenticated principal owns this account/session/notification; server resolves subject, never trusts requested role. |

## StudentProfilePanel

- **Kind:** feature
- **Surface:** student
- **Responsibility:** Read own safe profile and edit permitted display/interests/experience or logout.
- **Chunk:** ZE-P10-C07
- **Expected Module:** apps/web/src/features/student/StudentProfilePanel.tsx
- **Composition:** FormFields, AsyncBoundary
- **Reuse:** Feature-specific orchestration using shared domain and UI components
- **Input Sources:**
- **Local State:** Preferred name and optional closed educational selections.
- **States:** loading: Keep structural headings and announce loading; disable duplicate dependent actions.; empty: Show a specific absence message and only permitted next action.; error: Field422,stale409,denied403/invisible404,expired401 and transient429/503 are distinct; show safe message/request_id and bounded retry.; success: Render authoritative returned DTO and invalidate relevant scoped query keys.; detail: No age/school/guardian/role/finance edits; save sends only allowed fields; logout clears private cache.
- **Accessibility:** Semantic headings/labels,keyboard access,visible focus,live status,error association,200%reflow; never color alone.
- **Import Boundary:** May import shared/own-surface features only; no finance feature/client imports.
- **Requirements:** ADM-001, ADM-003, ADM-004, ADM-006, AUTH-001, AUTH-002, AUTH-003, AUTH-004, AUTH-005, AUTH-011, PAR-001, PAR-002, PAR-005, PAR-021, STU-001, STU-019, TCH-001, TCH-009

| Prop | Type | Required | Source |
|---|---|---|---|
| None | Route/session controller obtains its own authorized state | — | No implicit client identity authority |

| Operation | Request schema | Response schema | Roles | Ownership / state |
|---|---|---|---|---|
| API-STUDENT-SELF | API_STUDENT_SELFRequest | StudentSelfProfileView | student | Student principal identity equals resource student_id; active/completed eligible enrolment and released pinned curriculum; no finances. |
| API-STUDENT-PREFERRED | API_STUDENT_PREFERREDRequest | StudentSelfProfileView | student | Student principal identity equals resource student_id; active/completed eligible enrolment and released pinned curriculum; no finances. |
| API-ACCOUNT-PROFILE | API_ACCOUNT_PROFILERequest | AccountView | parent, student, teacher, admin | Authenticated principal owns this account/session/notification; server resolves subject, never trusts requested role. |
| API-AUTH-LOGOUT | API_AUTH_LOGOUTRequest | Empty | parent, student, teacher, admin | Authenticated principal owns this account/session/notification; server resolves subject, never trusts requested role. |

## TeacherDeliveryDashboard

- **Kind:** feature
- **Surface:** teacher
- **Responsibility:** Read assigned teaching courses/cohorts,upcoming responsibilities and own professional profile.
- **Chunk:** ZE-P11-C01
- **Expected Module:** apps/web/src/features/teacher/TeacherDeliveryDashboard.tsx
- **Composition:** PageHeader, ResourceTable, StatusBadge
- **Reuse:** Feature-specific orchestration using shared domain and UI components
- **Input Sources:**
- **Local State:** Selected assigned cohort.
- **States:** loading: Keep structural headings and announce loading; disable duplicate dependent actions.; empty: Show a specific absence message and only permitted next action.; error: Field422,stale409,denied403/invisible404,expired401 and transient429/503 are distinct; show safe message/request_id and bounded retry.; success: Render authoritative returned DTO and invalidate relevant scoped query keys.; detail: Only current assignments; teacher profile read-only operational data; public biography editor remains identity-admin.
- **Accessibility:** Semantic headings/labels,keyboard access,visible focus,live status,error association,200%reflow; never color alone.
- **Import Boundary:** May import shared/own-surface features only; no finance feature/client imports.
- **Requirements:** CLS-001, CLS-005

| Prop | Type | Required | Source |
|---|---|---|---|
| None | Route/session controller obtains its own authorized state | — | No implicit client identity authority |

| Operation | Request schema | Response schema | Roles | Ownership / state |
|---|---|---|---|---|
| API-TEACHER-DASHBOARD | API_TEACHER_DASHBOARDRequest | DashboardView | teacher | Active teacher assignment covers cohort/session and requested learner enrolment; purpose-limited educational projection; never finance. |
| API-TEACHER-COURSES | API_TEACHER_COURSESRequest | CourseViewPage | teacher | Active teacher assignment covers cohort/session and requested learner enrolment; purpose-limited educational projection; never finance. |
| API-TEACHER-COHORTS | API_TEACHER_COHORTSRequest | CohortViewPage | teacher | Active teacher assignment covers cohort/session and requested learner enrolment; purpose-limited educational projection; never finance. |
| API-TEACHER-PROFILE | API_TEACHER_PROFILERequest | TeacherView | teacher | Authenticated principal owns this account/session/notification; server resolves subject, never trusts requested role. |

## TeacherSchedule

- **Kind:** feature
- **Surface:** teacher
- **Responsibility:** Read assigned schedule/session details,reschedule permitted future session and obtain authorized host start.
- **Chunk:** ZE-P11-C01
- **Expected Module:** apps/web/src/features/teacher/TeacherSchedule.tsx
- **Composition:** ScheduleView, FormFields, ConfirmActionDialog
- **Reuse:** Feature-specific orchestration using shared domain and UI components
- **Input Sources:**
- **Local State:** Proposed local time,IANA timezone,explicit offset,duration,reason.
- **States:** loading: Keep structural headings and announce loading; disable duplicate dependent actions.; empty: Show a specific absence message and only permitted next action.; error: Field422,stale409,denied403/invisible404,expired401 and transient429/503 are distinct; show safe message/request_id and bounded retry.; success: Render authoritative returned DTO and invalidate relevant scoped query keys.; detail: >=24h rule/conflicts/DST server checked; start server window only; no global schedule controls and no saved host URL.
- **Accessibility:** Semantic headings/labels,keyboard access,visible focus,live status,error association,200%reflow; never color alone.
- **Import Boundary:** May import shared/own-surface features only; no finance feature/client imports.
- **Requirements:** CLS-002, CLS-003, CLS-004, CLS-006, CLS-007, CLS-008, CLS-009, CLS-011, TCH-004, TCH-005, TCH-006

| Prop | Type | Required | Source |
|---|---|---|---|
| sessionId | Uuid | False | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |

| Operation | Request schema | Response schema | Roles | Ownership / state |
|---|---|---|---|---|
| API-TEACHER-SCHEDULE | API_TEACHER_SCHEDULERequest | ClassSessionViewPage | teacher | Active teacher assignment covers cohort/session and requested learner enrolment; purpose-limited educational projection; never finance. |
| API-TEACHER-SESSION | API_TEACHER_SESSIONRequest | ClassSessionView | teacher | Active teacher assignment covers cohort/session and requested learner enrolment; purpose-limited educational projection; never finance. |
| API-TEACHER-RESCHEDULE | API_TEACHER_RESCHEDULERequest | ClassSessionView | teacher | Active teacher assignment covers cohort/session and requested learner enrolment; purpose-limited educational projection; never finance. Start >= now+24h; future assigned session only; no overlap for teacher/learner. |
| API-TEACHER-START | API_TEACHER_STARTRequest | JoinLinkView | teacher | Active teacher assignment covers cohort/session and requested learner enrolment; purpose-limited educational projection; never finance. Assigned authorized host; now within start-30m through scheduled end. |

## TeacherTeachingPlan

- **Kind:** feature
- **Surface:** teacher
- **Responsibility:** Read assigned cohort pinned curriculum,lesson plans and ready teaching resources.
- **Chunk:** ZE-P11-C01
- **Expected Module:** apps/web/src/features/teacher/TeacherTeachingPlan.tsx
- **Composition:** ModuleNavigation, LessonRenderer, ResourceTable
- **Reuse:** Feature-specific orchestration using shared domain and UI components
- **Input Sources:**
- **Local State:** Selected planned lesson.
- **States:** loading: Keep structural headings and announce loading; disable duplicate dependent actions.; empty: Show a specific absence message and only permitted next action.; error: Field422,stale409,denied403/invisible404,expired401 and transient429/503 are distinct; show safe message/request_id and bounded retry.; success: Render authoritative returned DTO and invalidate relevant scoped query keys.; detail: Teacher mode sees assigned teaching plan but no curriculum editing; file grants only assigned educational resources/work.
- **Accessibility:** Semantic headings/labels,keyboard access,visible focus,live status,error association,200%reflow; never color alone.
- **Import Boundary:** May import shared/own-surface features only; no finance feature/client imports.
- **Requirements:** ADM-023, FILE-001, FILE-002, FILE-003, FILE-004, FILE-005, FILE-006, FILE-007, LRN-002, LRN-003, LRN-004, TCH-003

| Prop | Type | Required | Source |
|---|---|---|---|
| cohortId | Uuid | True | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |
| lessonId | Uuid | False | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |

| Operation | Request schema | Response schema | Roles | Ownership / state |
|---|---|---|---|---|
| API-TEACHER-CURRICULUM | API_TEACHER_CURRICULUMRequest | CurriculumRevisionView | teacher | Active teacher assignment covers cohort/session and requested learner enrolment; purpose-limited educational projection; never finance. |
| API-TEACHER-LESSON | API_TEACHER_LESSONRequest | LessonView | teacher | Active teacher assignment covers cohort/session and requested learner enrolment; purpose-limited educational projection; never finance. |
| API-TEACHER-RESOURCES | API_TEACHER_RESOURCESRequest | ResourceViewPage | teacher | Active teacher assignment covers cohort/session and requested learner enrolment; purpose-limited educational projection; never finance. |
| API-FILE-GET | API_FILE_GETRequest | FileAssetView | parent, student, teacher, admin:education_admin, admin:operations_admin | FileAccessPolicy derives released curriculum, own submission, guardian link, teaching assignment or scoped admin purpose. Reject financial_document/financial_export purposes on this generic endpoint even for a parent; financial-specific BillingService/ReportingService grants are required. |
| API-FILE-DOWNLOAD | API_FILE_DOWNLOADRequest | DownloadTicketView | parent, student, teacher, admin:education_admin, admin:operations_admin | FileAccessPolicy validates ready state and linked resource scope; submission parents read only authorized child; internal files never learner-readable. Reject financial_document/financial_export purposes on this generic endpoint even for a parent; financial-specific BillingService/ReportingService grants are required. |

## TeacherLearnerRoster

- **Kind:** feature
- **Surface:** teacher
- **Responsibility:** Read assigned learners and minimum educational profile.
- **Chunk:** ZE-P11-C01
- **Expected Module:** apps/web/src/features/teacher/TeacherLearnerRoster.tsx
- **Composition:** ResourceTable, AsyncBoundary
- **Reuse:** Feature-specific orchestration using shared domain and UI components
- **Input Sources:**
- **Local State:** Learner filter and selected row.
- **States:** loading: Keep structural headings and announce loading; disable duplicate dependent actions.; empty: Show a specific absence message and only permitted next action.; error: Field422,stale409,denied403/invisible404,expired401 and transient429/503 are distinct; show safe message/request_id and bounded retry.; success: Render authoritative returned DTO and invalidate relevant scoped query keys.; detail: No guardian contact,school name,unnecessary surname,family ID,billing or unrelated learner data.
- **Accessibility:** Semantic headings/labels,keyboard access,visible focus,live status,error association,200%reflow; never color alone.
- **Import Boundary:** May import shared/own-surface features only; no finance feature/client imports.
- **Requirements:** CLS-005

| Prop | Type | Required | Source |
|---|---|---|---|
| cohortId | Uuid | True | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |
| studentId | Uuid | False | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |

| Operation | Request schema | Response schema | Roles | Ownership / state |
|---|---|---|---|---|
| API-TEACHER-STUDENTS | API_TEACHER_STUDENTSRequest | TeachingStudentViewPage | teacher | Active teacher assignment covers cohort/session and requested learner enrolment; purpose-limited educational projection; never finance. |
| API-TEACHER-STUDENT | API_TEACHER_STUDENTRequest | TeachingStudentView | teacher | Active teacher assignment covers cohort/session and requested learner enrolment; purpose-limited educational projection; never finance. |

## TeacherAttendanceManager

- **Kind:** feature
- **Surface:** teacher
- **Responsibility:** Record/amend attendance for learners in assigned session with reason.
- **Chunk:** ZE-P11-C01
- **Expected Module:** apps/web/src/features/teacher/TeacherAttendanceManager.tsx
- **Composition:** ResourceTable, FormFields, AuditReasonForm
- **Reuse:** Feature-specific orchestration using shared domain and UI components
- **Input Sources:** Authorized session GET.cohort_id supplies teacher-students roster lookup; join roster student/enrolment references to the current session attendance read. Exact-student attendance GET validates assignment/membership and empty result means no row. First PUT uses If-None-Match:*; existing PUT uses the returned positive row If-Match, exactly one header. No guessed learner names or initial version.
- **Local State:** Per-row pending status/minutes/reason and server version.
- **States:** loading: Keep structural headings and announce loading; disable duplicate dependent actions.; empty: Show a specific absence message and only permitted next action.; error: Field422,stale409,denied403/invisible404,expired401 and transient429/503 are distinct; show safe message/request_id and bounded retry.; success: Render authoritative returned DTO and invalidate relevant scoped query keys.; detail: One explicit record/amend request per learner; no optimistic bulk success; stale row refetches and preserves unsaved reason.
- **Accessibility:** Keyboard table/select controls,announced row result,focus after failed record; no color-only attendance.
- **Import Boundary:** May import shared/own-surface features only; no finance feature/client imports.
- **Requirements:** CLS-002, CLS-003, CLS-004, CLS-005, CLS-010, CLS-011, TCH-005, TCH-006, TCH-007, TCH-008

| Prop | Type | Required | Source |
|---|---|---|---|
| sessionId | Uuid | True | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |

| Operation | Request schema | Response schema | Roles | Ownership / state |
|---|---|---|---|---|
| API-TEACHER-ATTENDANCE | API_TEACHER_ATTENDANCERequest | AttendanceViewPage | teacher | Active teacher assignment covers cohort/session and requested learner enrolment; purpose-limited educational projection; never finance. With exact student_id filter, first authorize that student in the session cohort, then return one persisted row or an empty items array. Empty items means no record yet, not permission to infer a version. Read never creates virtual AttendanceRecord IDs/versions; UI shows unrecorded from absence. |
| API-TEACHER-ATTENDANCE-RECORD | API_TEACHER_ATTENDANCE_RECORDRequest | AttendanceView | teacher | Active teacher assignment covers cohort/session and requested learner enrolment; purpose-limited educational projection; never finance. Student enrolled in this session cohort. First-write concurrency requires exactly one If-None-Match:* for absent AttendanceRecord, or If-Match current AttendanceRecord.version for existing row; never a definition, submission or other aggregate token. |
| API-TEACHER-SESSION | API_TEACHER_SESSIONRequest | ClassSessionView | teacher | Active teacher assignment covers cohort/session and requested learner enrolment; purpose-limited educational projection; never finance. |
| API-TEACHER-STUDENTS | API_TEACHER_STUDENTSRequest | TeachingStudentViewPage | teacher | Active teacher assignment covers cohort/session and requested learner enrolment; purpose-limited educational projection; never finance. |

## TeacherCommunications

- **Kind:** feature
- **Surface:** teacher
- **Responsibility:** Read relevant teaching events,announcements and own operational notifications.
- **Chunk:** ZE-P11-C01
- **Expected Module:** apps/web/src/features/teacher/TeacherCommunications.tsx
- **Composition:** NotificationList, ResourceTable
- **Reuse:** Feature-specific orchestration using shared domain and UI components
- **Input Sources:**
- **Local State:** Tab/cursor only.
- **States:** loading: Keep structural headings and announce loading; disable duplicate dependent actions.; empty: Show a specific absence message and only permitted next action.; error: Field422,stale409,denied403/invisible404,expired401 and transient429/503 are distinct; show safe message/request_id and bounded retry.; success: Render authoritative returned DTO and invalidate relevant scoped query keys.; detail: Teacher payment notification types never requested or rendered.
- **Accessibility:** Semantic headings/labels,keyboard access,visible focus,live status,error association,200%reflow; never color alone.
- **Import Boundary:** May import shared/own-surface features only; no finance feature/client imports.
- **Requirements:** ADM-022, COM-001, COM-002, COM-003, COM-004, COM-005, COM-006, COM-007, COM-008, COM-009, PAR-016, TCH-015

| Prop | Type | Required | Source |
|---|---|---|---|
| tab | events\|announcements\|notifications | True | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |

| Operation | Request schema | Response schema | Roles | Ownership / state |
|---|---|---|---|---|
| API-TEACHER-EVENTS | API_TEACHER_EVENTSRequest | EventViewPage | teacher | Active teacher assignment covers cohort/session and requested learner enrolment; purpose-limited educational projection; never finance. Audience membership rechecked at read. |
| API-TEACHER-ANNOUNCEMENTS | API_TEACHER_ANNOUNCEMENTSRequest | AnnouncementViewPage | teacher | Active teacher assignment covers cohort/session and requested learner enrolment; purpose-limited educational projection; never finance. Audience membership rechecked at read. |
| API-NOTIFICATIONS | API_NOTIFICATIONSRequest | NotificationViewPage | parent, student, teacher, admin | Authenticated principal owns this account/session/notification; server resolves subject, never trusts requested role. |
| API-NOTIFICATION-READ | API_NOTIFICATION_READRequest | NotificationView | parent, student, teacher, admin | Authenticated principal owns this account/session/notification; server resolves subject, never trusts requested role. |

## TeacherWorkQueue

- **Kind:** feature
- **Surface:** teacher
- **Responsibility:** Read assigned assignment/project definitions,submitted work queue and submitted quiz results.
- **Chunk:** ZE-P11-C02
- **Expected Module:** apps/web/src/features/teacher/TeacherWorkQueue.tsx
- **Composition:** ResourceTable, ReleasedResultView
- **Reuse:** Feature-specific orchestration using shared domain and UI components
- **Input Sources:** Teacher-students roster supplies names/student IDs for this cohort; teaching assignments definitions supply assignment identifiers. Match submitted work by scoped IDs, without identity-directory access.
- **Local State:** Assignment/student/status filters bound to cohort.
- **States:** loading: Keep structural headings and announce loading; disable duplicate dependent actions.; empty: Show a specific absence message and only permitted next action.; error: Field422,stale409,denied403/invisible404,expired401 and transient429/503 are distinct; show safe message/request_id and bounded retry.; success: Render authoritative returned DTO and invalidate relevant scoped query keys.; detail: No unrelated cohort substitution; only submitted work; quiz explanations are released result projection.
- **Accessibility:** Semantic headings/labels,keyboard access,visible focus,live status,error association,200%reflow; never color alone.
- **Import Boundary:** May import shared/own-surface features only; no finance feature/client imports.
- **Requirements:** ASM-001, ASM-002, ASM-003, ASM-004, ASM-005, CLS-005, TCH-010

| Prop | Type | Required | Source |
|---|---|---|---|
| cohortId | Uuid | True | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |

| Operation | Request schema | Response schema | Roles | Ownership / state |
|---|---|---|---|---|
| API-TEACHER-ASSIGNMENTS | API_TEACHER_ASSIGNMENTSRequest | AssignmentViewPage | teacher | Active teacher assignment covers cohort/session and requested learner enrolment; purpose-limited educational projection; never finance. |
| API-TEACHER-SUBMISSIONS | API_TEACHER_SUBMISSIONSRequest | SubmissionViewPage | teacher | Active teacher assignment covers cohort/session and requested learner enrolment; purpose-limited educational projection; never finance. |
| API-TEACHER-QUIZ-RESULTS | API_TEACHER_QUIZ_RESULTSRequest | QuizAttemptViewPage | teacher | Active teacher assignment covers cohort/session and requested learner enrolment; purpose-limited educational projection; never finance. |
| API-TEACHER-STUDENTS | API_TEACHER_STUDENTSRequest | TeachingStudentViewPage | teacher | Active teacher assignment covers cohort/session and requested learner enrolment; purpose-limited educational projection; never finance. |

## TeacherAssessmentReview

- **Kind:** feature
- **Surface:** teacher
- **Responsibility:** Review frozen learner work,save rubric marking,return revision,release or withdraw result.
- **Chunk:** ZE-P11-C02
- **Expected Module:** apps/web/src/features/teacher/TeacherAssessmentReview.tsx
- **Composition:** FormFields, ReleasedResultView, AuditReasonForm, ConfirmActionDialog
- **Reuse:** Feature-specific orchestration using shared domain and UI components
- **Input Sources:** Submitted work is fetched under cohort/submission route. Teacher-students roster supplies the learner label; teacher-assignment list supplies the referenced definition/rubric. Read AssessmentStateView: assessment=null authoritatively means no row after authorized frozen-submission validation. First save uses If-None-Match:*; otherwise use assessment.version in If-Match. Send exactly one conditional header; refetch on a creation/update race.
- **Local State:** Mark/comment draft,current assessment version and chosen deliberate transition.
- **States:** loading: Keep structural headings and announce loading; disable duplicate dependent actions.; empty: Show a specific absence message and only permitted next action.; error: Field422,stale409,denied403/invisible404,expired401 and transient429/503 are distinct; show safe message/request_id and bounded retry.; success: Render authoritative returned DTO and invalidate relevant scoped query keys.; detail: Save draft distinct from release; withdrawal reason required; submitted body/files immutable; return allows learner new version.
- **Accessibility:** Semantic headings/labels,keyboard access,visible focus,live status,error association,200%reflow; never color alone.
- **Import Boundary:** May import shared/own-surface features only; no finance feature/client imports.
- **Requirements:** ADM-023, ASM-004, ASM-005, ASM-006, ASM-007, CLS-005, FILE-001, FILE-002, FILE-003, FILE-004, FILE-005, FILE-006, FILE-007, TCH-010, TCH-011, TCH-012

| Prop | Type | Required | Source |
|---|---|---|---|
| cohortId | Uuid | True | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |
| submissionId | Uuid | True | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |

| Operation | Request schema | Response schema | Roles | Ownership / state |
|---|---|---|---|---|
| API-TEACHER-SUBMISSION | API_TEACHER_SUBMISSIONRequest | SubmissionView | teacher | Active teacher assignment covers cohort/session and requested learner enrolment; purpose-limited educational projection; never finance. |
| API-TEACHER-ASSESSMENT-GET | API_TEACHER_ASSESSMENT_GETRequest | AssessmentStateView | teacher | Active teacher assignment covers cohort/session and requested learner enrolment; purpose-limited educational projection; never finance. Return AssessmentStateView only after authorizing an existing frozen submission. assessment=null proves absence; never confuse unauthorized/missing submission with a creatable assessment. |
| API-TEACHER-ASSESSMENT | API_TEACHER_ASSESSMENTRequest | AssessmentView | teacher | Active teacher assignment covers cohort/session and requested learner enrolment; purpose-limited educational projection; never finance. First-write concurrency requires exactly one If-None-Match:* for absent Assessment, or If-Match current Assessment.version for existing row; never a definition, submission or other aggregate token. |
| API-TEACHER-RETURN | API_TEACHER_RETURNRequest | SubmissionView | teacher | Active teacher assignment covers cohort/session and requested learner enrolment; purpose-limited educational projection; never finance. |
| API-TEACHER-ASSESSMENT-RELEASE | API_TEACHER_ASSESSMENT_RELEASERequest | AssessmentView | teacher | Active teacher assignment covers cohort/session and requested learner enrolment; purpose-limited educational projection; never finance. |
| API-TEACHER-ASSESSMENT-WITHDRAW | API_TEACHER_ASSESSMENT_WITHDRAWRequest | AssessmentView | teacher | Active teacher assignment covers cohort/session and requested learner enrolment; purpose-limited educational projection; never finance. |
| API-FILE-GET | API_FILE_GETRequest | FileAssetView | parent, student, teacher, admin:education_admin, admin:operations_admin | FileAccessPolicy derives released curriculum, own submission, guardian link, teaching assignment or scoped admin purpose. Reject financial_document/financial_export purposes on this generic endpoint even for a parent; financial-specific BillingService/ReportingService grants are required. |
| API-FILE-DOWNLOAD | API_FILE_DOWNLOADRequest | DownloadTicketView | parent, student, teacher, admin:education_admin, admin:operations_admin | FileAccessPolicy validates ready state and linked resource scope; submission parents read only authorized child; internal files never learner-readable. Reject financial_document/financial_export purposes on this generic endpoint even for a parent; financial-specific BillingService/ReportingService grants are required. |
| API-TEACHER-STUDENTS | API_TEACHER_STUDENTSRequest | TeachingStudentViewPage | teacher | Active teacher assignment covers cohort/session and requested learner enrolment; purpose-limited educational projection; never finance. |
| API-TEACHER-ASSIGNMENTS | API_TEACHER_ASSIGNMENTSRequest | AssignmentViewPage | teacher | Active teacher assignment covers cohort/session and requested learner enrolment; purpose-limited educational projection; never finance. |

## TeacherFeedbackProgress

- **Kind:** feature
- **Surface:** teacher
- **Responsibility:** Read assigned progress and author,revise,release or withdraw educational feedback.
- **Chunk:** ZE-P11-C02
- **Expected Module:** apps/web/src/features/teacher/TeacherFeedbackProgress.tsx
- **Composition:** ProgressSummary, FormFields, ConfirmActionDialog
- **Reuse:** Feature-specific orchestration using shared domain and UI components
- **Input Sources:** Current cohort teacher-students roster supplies named recipient student_id for first feedback even when feedback list is empty. Existing feedback/progress reads supply their own state/version; draft remains staff-only.
- **Local State:** Feedback draft/selected learner/release confirmation.
- **States:** loading: Keep structural headings and announce loading; disable duplicate dependent actions.; empty: Show a specific absence message and only permitted next action.; error: Field422,stale409,denied403/invisible404,expired401 and transient429/503 are distinct; show safe message/request_id and bounded retry.; success: Render authoritative returned DTO and invalidate relevant scoped query keys.; detail: Released record requires withdrawal before revision; no private messaging thread; no completion override for teacher.
- **Accessibility:** Semantic headings/labels,keyboard access,visible focus,live status,error association,200%reflow; never color alone.
- **Import Boundary:** May import shared/own-surface features only; no finance feature/client imports.
- **Requirements:** ASM-008, CLS-005, LRN-007, LRN-008, TCH-013, TCH-014

| Prop | Type | Required | Source |
|---|---|---|---|
| cohortId | Uuid | True | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |
| studentId | Uuid | False | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |

| Operation | Request schema | Response schema | Roles | Ownership / state |
|---|---|---|---|---|
| API-TEACHER-PROGRESS | API_TEACHER_PROGRESSRequest | ProgressViewPage | teacher | Active teacher assignment covers cohort/session and requested learner enrolment; purpose-limited educational projection; never finance. |
| API-TEACHER-FEEDBACK-LIST | API_TEACHER_FEEDBACK_LISTRequest | FeedbackViewPage | teacher | Active teacher assignment covers cohort/session and requested learner enrolment; purpose-limited educational projection; never finance. |
| API-TEACHER-FEEDBACK-CREATE | API_TEACHER_FEEDBACK_CREATERequest | FeedbackView | teacher | Active teacher assignment covers cohort/session and requested learner enrolment; purpose-limited educational projection; never finance. |
| API-TEACHER-FEEDBACK-UPDATE | API_TEACHER_FEEDBACK_UPDATERequest | FeedbackView | teacher | Active teacher assignment covers cohort/session and requested learner enrolment; purpose-limited educational projection; never finance. |
| API-TEACHER-FEEDBACK-RELEASE | API_TEACHER_FEEDBACK_RELEASERequest | FeedbackView | teacher | Active teacher assignment covers cohort/session and requested learner enrolment; purpose-limited educational projection; never finance. |
| API-TEACHER-FEEDBACK-WITHDRAW | API_TEACHER_FEEDBACK_WITHDRAWRequest | FeedbackView | teacher | Active teacher assignment covers cohort/session and requested learner enrolment; purpose-limited educational projection; never finance. |
| API-TEACHER-STUDENTS | API_TEACHER_STUDENTSRequest | TeachingStudentViewPage | teacher | Active teacher assignment covers cohort/session and requested learner enrolment; purpose-limited educational projection; never finance. |

## AdminParentFamilyManager

- **Kind:** feature
- **Surface:** admin
- **Responsibility:** Find parent/family and manage verified guardian/billing membership links with audited evidence.
- **Chunk:** ZE-P11-C03
- **Expected Module:** apps/web/src/features/admin/AdminParentFamilyManager.tsx
- **Composition:** ResourceTable, AuditReasonForm, ConfirmActionDialog
- **Reuse:** Feature-specific orchestration using shared domain and UI components
- **Input Sources:** Refresh API-ADMIN-FAMILY for AdminFamilyRelationshipsView. Create relationship/membership using family.version; revoke using the exact matching guardian_links[].version or billing_memberships[].version and their IDs/state. Flat parent FamilyView is never used as administrative relationship authority.
- **Local State:** Search/selected verified guardian,verification reference and reason.
- **States:** loading: Keep structural headings and announce loading; disable duplicate dependent actions.; empty: Show a specific absence message and only permitted next action.; error: Field422,stale409,denied403/invisible404,expired401 and transient429/503 are distinct; show safe message/request_id and bounded retry.; success: Render authoritative returned DTO and invalidate relevant scoped query keys.; detail: identity_admin only; billing membership grant requires independent financial approval evidence; no child linking by email/name guess.
- **Accessibility:** Semantic headings/labels,keyboard access,visible focus,live status,error association,200%reflow; never color alone.
- **Import Boundary:** May import shared and declared feature dependencies; generated API subset only.
- **Requirements:** PAR-006

| Prop | Type | Required | Source |
|---|---|---|---|
| familyId | Uuid | False | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |
| studentId | Uuid | False | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |

| Operation | Request schema | Response schema | Roles | Ownership / state |
|---|---|---|---|---|
| API-ADMIN-PARENTS | API_ADMIN_PARENTSRequest | GuardianViewPage | admin:identity_admin | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| API-ADMIN-FAMILY | API_ADMIN_FAMILYRequest | AdminFamilyRelationshipsView | admin:identity_admin | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. Identity-only AdminFamilyRelationshipsView includes exact guardian/student pairs and independent billing membership states; no financial records. Parent FamilyView is unchanged. |
| API-ADMIN-GUARDIAN-LINK | API_ADMIN_GUARDIAN_LINKRequest | AdminFamilyRelationshipsView | admin:identity_admin | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. Verification evidence reference mandatory; no cross-family transfer implicit. Identity-only AdminFamilyRelationshipsView includes exact guardian/student pairs and independent billing membership states; no financial records. Parent FamilyView is unchanged. |
| API-ADMIN-GUARDIAN-REVOKE | API_ADMIN_GUARDIAN_REVOKERequest | AdminFamilyRelationshipsView | admin:identity_admin | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. At least one verified active guardian remains or safeguarding override is documented. Identity-only AdminFamilyRelationshipsView includes exact guardian/student pairs and independent billing membership states; no financial records. Parent FamilyView is unchanged. |
| API-ADMIN-BILLING-MEMBER | API_ADMIN_BILLING_MEMBERRequest | AdminFamilyRelationshipsView | admin:identity_admin | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. Separate finance approval reference required; no teacher principal. Identity-only AdminFamilyRelationshipsView includes exact guardian/student pairs and independent billing membership states; no financial records. Parent FamilyView is unchanged. |
| API-ADMIN-BILLING-MEMBER-REVOKE | API_ADMIN_BILLING_MEMBER_REVOKERequest | Empty | admin:identity_admin | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |

## AdminStudentManager

- **Kind:** feature
- **Surface:** admin
- **Responsibility:** Find/correct student profile and archive only eligible completed obligations.
- **Chunk:** ZE-P11-C03
- **Expected Module:** apps/web/src/features/admin/AdminStudentManager.tsx
- **Composition:** ResourceTable, FormFields, AuditReasonForm, ConfirmActionDialog
- **Reuse:** Feature-specific orchestration using shared domain and UI components
- **Input Sources:**
- **Local State:** Minimized profile changes and reason.
- **States:** loading: Keep structural headings and announce loading; disable duplicate dependent actions.; empty: Show a specific absence message and only permitted next action.; error: Field422,stale409,denied403/invisible404,expired401 and transient429/503 are distinct; show safe message/request_id and bounded retry.; success: Render authoritative returned DTO and invalidate relevant scoped query keys.; detail: identity_admin only; optional fields stay optional; active enrolment/guardian conflict visible.
- **Accessibility:** Semantic headings/labels,keyboard access,visible focus,live status,error association,200%reflow; never color alone.
- **Import Boundary:** May import shared and declared feature dependencies; generated API subset only.
- **Requirements:** ADM-004

| Prop | Type | Required | Source |
|---|---|---|---|
| studentId | Uuid | False | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |

| Operation | Request schema | Response schema | Roles | Ownership / state |
|---|---|---|---|---|
| API-ADMIN-STUDENTS | API_ADMIN_STUDENTSRequest | StudentProfileViewPage | admin:identity_admin | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| API-ADMIN-STUDENT | API_ADMIN_STUDENTRequest | StudentProfileView | admin:identity_admin | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| API-ADMIN-STUDENT-UPDATE | API_ADMIN_STUDENT_UPDATERequest | StudentProfileView | admin:identity_admin | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| API-ADMIN-STUDENT-ARCHIVE | API_ADMIN_STUDENT_ARCHIVERequest | StudentProfileView | admin:identity_admin | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |

## AdminTeacherManager

- **Kind:** feature
- **Surface:** admin
- **Responsibility:** Manage staff teacher profile/lifecycle and expressly approved public instructor publication.
- **Chunk:** ZE-P11-C03
- **Expected Module:** apps/web/src/features/admin/AdminTeacherManager.tsx
- **Composition:** ResourceTable, FormFields, ConfirmActionDialog
- **Reuse:** Feature-specific orchestration using shared domain and UI components
- **Input Sources:**
- **Local State:** Biography,display photo asset selection,status/reason.
- **States:** loading: Keep structural headings and announce loading; disable duplicate dependent actions.; empty: Show a specific absence message and only permitted next action.; error: Field422,stale409,denied403/invisible404,expired401 and transient429/503 are distinct; show safe message/request_id and bounded retry.; success: Render authoritative returned DTO and invalidate relevant scoped query keys.; detail: identity_admin controls these actions; public photo must be ready approved asset obtained through separately permitted asset workflow; no operational contact published.
- **Accessibility:** Semantic headings/labels,keyboard access,visible focus,live status,error association,200%reflow; never color alone.
- **Import Boundary:** May import shared and declared feature dependencies; generated API subset only.
- **Requirements:** ADM-005, ADM-015, CLS-005

| Prop | Type | Required | Source |
|---|---|---|---|
| teacherId | Uuid | False | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |

| Operation | Request schema | Response schema | Roles | Ownership / state |
|---|---|---|---|---|
| API-ADMIN-TEACHERS | API_ADMIN_TEACHERSRequest | TeacherViewPage | admin:identity_admin | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| API-ADMIN-TEACHER | API_ADMIN_TEACHERRequest | TeacherView | admin:identity_admin | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| API-ADMIN-TEACHER-UPDATE | API_ADMIN_TEACHER_UPDATERequest | TeacherView | admin:identity_admin | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| API-ADMIN-TEACHER-PUBLISH | API_ADMIN_TEACHER_PUBLISHRequest | TeacherView | admin:identity_admin | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| API-ADMIN-TEACHER-ARCHIVE | API_ADMIN_TEACHER_ARCHIVERequest | TeacherView | admin:identity_admin | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |

## AdminAccountRoleManager

- **Kind:** feature
- **Surface:** admin
- **Responsibility:** Invite staff,read compatible role grants,set allowed admin privileges and suspend/reactivate accounts.
- **Chunk:** ZE-P11-C03
- **Expected Module:** apps/web/src/features/admin/AdminAccountRoleManager.tsx
- **Composition:** FormFields, ResourceTable, AuditReasonForm, ConfirmActionDialog
- **Reuse:** Feature-specific orchestration using shared domain and UI components
- **Input Sources:** Select API-ADMIN-ACCOUNTS.items[].id; refresh API-ADMIN-ACCOUNT for current account status/version. Read API-ADMIN-ROLE for the current grant projection; its version is the owning Account.version. Use the returned aggregate token and refetch after every write; preserve self-escalation/last-admin checks.
- **Local State:** Invite identity/role,closed privilege selection,reason.
- **States:** loading: Keep structural headings and announce loading; disable duplicate dependent actions.; empty: Show a specific absence message and only permitted next action.; error: Field422,stale409,denied403/invisible404,expired401 and transient429/503 are distinct; show safe message/request_id and bounded retry.; success: Render authoritative returned DTO and invalidate relevant scoped query keys.; detail: No self-escalation,last-admin removal or teacher+admin combined principal; incompatible grant error retained; server owns grant authority.
- **Accessibility:** Semantic headings/labels,keyboard access,visible focus,live status,error association,200%reflow; never color alone.
- **Import Boundary:** May import shared and declared feature dependencies; generated API subset only.
- **Requirements:** ADM-003, ADM-006, AUTH-010, AUTH-011, NFR-012

| Prop | Type | Required | Source |
|---|---|---|---|
| accountId | Uuid | False | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |

| Operation | Request schema | Response schema | Roles | Ownership / state |
|---|---|---|---|---|
| API-ADMIN-INVITE | API_ADMIN_INVITERequest | AccountView | admin:identity_admin | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. Separate admin principal required for teacher-to-admin duties. |
| API-ADMIN-ROLE | API_ADMIN_ROLERequest | RoleGrantView | admin:identity_admin | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| API-ADMIN-ROLE-UPDATE | API_ADMIN_ROLE_UPDATERequest | RoleGrantView | admin:identity_admin | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. Cannot self-escalate; no last identity-admin removal; teacher/admin principal incompatibility. Compare If-Match against the same Account.version returned by AccountView and RoleGrantView; role and status changes each increment that counter. Under a shared identity-admin membership lock, reject any change leaving zero active identity administrators with LAST_ADMIN, including concurrent suspensions/removals. |
| API-ADMIN-ACCOUNT-STATUS | API_ADMIN_ACCOUNT_STATUSRequest | AccountView | admin:identity_admin | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. Compare If-Match against the same Account.version returned by AccountView and RoleGrantView; role and status changes each increment that counter. Under a shared identity-admin membership lock, reject any change leaving zero active identity administrators with LAST_ADMIN, including concurrent suspensions/removals. |
| API-ADMIN-ACCOUNTS | API_ADMIN_ACCOUNTSRequest | AccountViewPage | admin:identity_admin | Authenticated active administrator with identity_admin and recent MFA. Read only the existing AccountView fields (id,role,display_name,email nullable,status,mfa_enabled,version); no credentials,password hashes,session tokens,MFA seed/recovery codes,child login alias,family details or billing data. Deny public,parent,student,teacher and administrators without identity_admin. Lookup does not grant a role change or status mutation; those existing writes reauthorize and use their own required version. |
| API-ADMIN-ACCOUNT | API_ADMIN_ACCOUNTRequest | AccountView | admin:identity_admin | Authenticated active administrator with identity_admin and recent MFA. Read only the existing AccountView fields (id,role,display_name,email nullable,status,mfa_enabled,version); no credentials,password hashes,session tokens,MFA seed/recovery codes,child login alias,family details or billing data. Deny public,parent,student,teacher and administrators without identity_admin. Lookup does not grant a role change or status mutation; those existing writes reauthorize and use their own required version. Fetch current Account.version for API-ADMIN-ACCOUNT-STATUS If-Match; do not substitute RoleGrantView.version or a version from another account. |

## AdminPrivacyDesk

- **Kind:** feature
- **Surface:** admin
- **Responsibility:** Verify adult privacy requests and record retention-aware decision/hold changes.
- **Chunk:** ZE-P11-C03
- **Expected Module:** apps/web/src/features/admin/AdminPrivacyDesk.tsx
- **Composition:** ResourceTable, AuditReasonForm, ConfirmActionDialog
- **Reuse:** Feature-specific orchestration using shared domain and UI components
- **Input Sources:** Pick resource_type/resource_id from authorized hold-targets items (optional actual family filter); display_reference is safe metadata only. Read hold-state for the selected exact type/ID; use returned hold_version including server-returned zero for absence. Never use a payment/file/family version for hold mutation; no financial amount or file contents are fetched.
- **Local State:** Decision,verified authority/evidence refs,hold target/type,reason.
- **States:** loading: Keep structural headings and announce loading; disable duplicate dependent actions.; empty: Show a specific absence message and only permitted next action.; error: Field422,stale409,denied403/invisible404,expired401 and transient429/503 are distinct; show safe message/request_id and bounded retry.; success: Render authoritative returned DTO and invalidate relevant scoped query keys.; detail: identity_admin purpose; no arbitrary export of other adult finances; approve request does not bypass retention or orphaning safeguards.
- **Accessibility:** Semantic headings/labels,keyboard access,visible focus,live status,error association,200%reflow; never color alone.
- **Import Boundary:** May import shared and declared feature dependencies; generated API subset only.
- **Requirements:** AUTH-010, NFR-012, SEC-001, SEC-002, SEC-008, SEC-009, SEC-010

| Prop | Type | Required | Source |
|---|---|---|---|
| requestId | Uuid | False | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |

| Operation | Request schema | Response schema | Roles | Ownership / state |
|---|---|---|---|---|
| API-ADMIN-PRIVACY-LIST | API_ADMIN_PRIVACY_LISTRequest | PrivacyRequestViewPage | admin:identity_admin | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| API-ADMIN-PRIVACY-DECIDE | API_ADMIN_PRIVACY_DECIDERequest | PrivacyRequestView | admin:identity_admin | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. Never orphan active children or erase required finance records. |
| API-ADMIN-LEGAL-HOLD | API_ADMIN_LEGAL_HOLDRequest | Empty | admin:identity_admin | Active administrator with identity_admin and recent MFA; deny every other privilege-only principal, teacher, parent and student. Explicit identity-purpose projection only. Typed target must exist; identity-admin can decide retention only, without payment/file content reads. If-Match compares exclusively the RetentionHold state returned by API-ADMIN-LEGAL-HOLD-STATE. |
| API-ADMIN-LEGAL-HOLD-TARGETS | API_ADMIN_LEGAL_HOLD_TARGETSRequest | LegalHoldTargetViewPage | admin:identity_admin | Active administrator with identity_admin and recent MFA; deny every other privilege-only principal, teacher, parent and student. Explicit identity-purpose projection only. List only typed identity references and existing ownership links; no payment/file domain object hydration or generic finance/file read grants. Filters apply before bounded stable pagination. |
| API-ADMIN-LEGAL-HOLD-STATE | API_ADMIN_LEGAL_HOLD_STATERequest | LegalHoldStateView | admin:identity_admin | Active administrator with identity_admin and recent MFA; deny every other privilege-only principal, teacher, parent and student. Explicit identity-purpose projection only. Verify target existence via the same typed projection; do not read or expose its financial/file contents. Never reuse target aggregate version as hold version. |

## AdminPublicPageEditor

- **Kind:** feature
- **Surface:** admin
- **Responsibility:** Read public page drafts,edit fixed page content and deliberately publish.
- **Chunk:** ZE-P11-C04
- **Expected Module:** apps/web/src/features/admin/AdminPublicPageEditor.tsx
- **Composition:** FormFields, ResourceTable, ConfirmActionDialog
- **Reuse:** Feature-specific orchestration using shared domain and UI components
- **Input Sources:**
- **Local State:** Validated rich-text draft,selected page,version.
- **States:** loading: Keep structural headings and announce loading; disable duplicate dependent actions.; empty: Show a specific absence message and only permitted next action.; error: Field422,stale409,denied403/invisible404,expired401 and transient429/503 are distinct; show safe message/request_id and bounded retry.; success: Render authoritative returned DTO and invalidate relevant scoped query keys.; detail: operations_admin only; no arbitrary new public route; preview uses same sanitized semantic renderer.
- **Accessibility:** Semantic headings/labels,keyboard access,visible focus,live status,error association,200%reflow; never color alone.
- **Import Boundary:** May import shared and declared feature dependencies; generated API subset only.
- **Requirements:** ADM-007, LRN-001

| Prop | Type | Required | Source |
|---|---|---|---|
| slug | PublicPageSlug | False | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |

| Operation | Request schema | Response schema | Roles | Ownership / state |
|---|---|---|---|---|
| API-ADMIN-PAGES | API_ADMIN_PAGESRequest | PublicPageViewPage | admin:operations_admin | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| API-ADMIN-PAGE-UPDATE | API_ADMIN_PAGE_UPDATERequest | PublicPageView | admin:operations_admin | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| API-ADMIN-PAGE-PUBLISH | API_ADMIN_PAGE_PUBLISHRequest | PublicPageView | admin:operations_admin | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |

## AdminPolicyEditor

- **Kind:** feature
- **Surface:** admin
- **Responsibility:** Create versioned policy drafts and publish only verified human-approved effective versions.
- **Chunk:** ZE-P11-C04
- **Expected Module:** apps/web/src/features/admin/AdminPolicyEditor.tsx
- **Composition:** FormFields, ResourceTable, AuditReasonForm, ConfirmActionDialog
- **Reuse:** Feature-specific orchestration using shared domain and UI components
- **Input Sources:**
- **Local State:** Version,key,effective date,required acknowledgements,approval reference.
- **States:** loading: Keep structural headings and announce loading; disable duplicate dependent actions.; empty: Show a specific absence message and only permitted next action.; error: Field422,stale409,denied403/invisible404,expired401 and transient429/503 are distinct; show safe message/request_id and bounded retry.; success: Render authoritative returned DTO and invalidate relevant scoped query keys.; detail: operations_admin; published versions immutable; arbitrary reference text is not approval; no placeholder legal publication.
- **Accessibility:** Semantic headings/labels,keyboard access,visible focus,live status,error association,200%reflow; never color alone.
- **Import Boundary:** May import shared and declared feature dependencies; generated API subset only.
- **Requirements:** SEC-003

| Prop | Type | Required | Source |
|---|---|---|---|
| None | Route/session controller obtains its own authorized state | — | No implicit client identity authority |

| Operation | Request schema | Response schema | Roles | Ownership / state |
|---|---|---|---|---|
| API-ADMIN-POLICIES | API_ADMIN_POLICIESRequest | PolicyViewPage | admin:operations_admin | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| API-ADMIN-POLICY-CREATE | API_ADMIN_POLICY_CREATERequest | PolicyView | admin:operations_admin | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| API-ADMIN-POLICY-PUBLISH | API_ADMIN_POLICY_PUBLISHRequest | PolicyView | admin:operations_admin | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |

## AdminProgramCourseEditor

- **Kind:** feature
- **Surface:** admin
- **Responsibility:** Manage program grouping/course metadata,approved published revision pointer and course archive.
- **Chunk:** ZE-P11-C04
- **Expected Module:** apps/web/src/features/admin/AdminProgramCourseEditor.tsx
- **Composition:** ResourceTable, FormFields, ConfirmActionDialog
- **Reuse:** Feature-specific orchestration using shared domain and UI components
- **Input Sources:** Selected CourseView.id supplies course_id for revision list. Choose a published CurriculumRevisionView.id from that list for publication; never require an existing current_revision_id for the first publish.
- **Local State:** Selected course/program,metadata draft,selected ready published revision.
- **States:** loading: Keep structural headings and announce loading; disable duplicate dependent actions.; empty: Show a specific absence message and only permitted next action.; error: Field422,stale409,denied403/invisible404,expired401 and transient429/503 are distinct; show safe message/request_id and bounded retry.; success: Render authoritative returned DTO and invalidate relevant scoped query keys.; detail: education_admin only; separate cohort delivery; no fee configuration and no learner-data mass edit.
- **Accessibility:** Semantic headings/labels,keyboard access,visible focus,live status,error association,200%reflow; never color alone.
- **Import Boundary:** May import shared and declared feature dependencies; generated API subset only.
- **Requirements:** ADM-007, ADM-008, LRN-001, LRN-002, LRN-003, LRN-004

| Prop | Type | Required | Source |
|---|---|---|---|
| courseId | Uuid | False | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |
| programId | Uuid | False | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |

| Operation | Request schema | Response schema | Roles | Ownership / state |
|---|---|---|---|---|
| API-ADMIN-PROGRAM-LIST | API_ADMIN_PROGRAM_LISTRequest | ProgramViewPage | admin:education_admin | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| API-ADMIN-PROGRAM-CREATE | API_ADMIN_PROGRAM_CREATERequest | ProgramView | admin:education_admin | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| API-ADMIN-PROGRAM-UPDATE | API_ADMIN_PROGRAM_UPDATERequest | ProgramView | admin:education_admin | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| API-ADMIN-PROGRAM-STATUS | API_ADMIN_PROGRAM_STATUSRequest | ProgramView | admin:education_admin | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| API-ADMIN-COURSES | API_ADMIN_COURSESRequest | CourseViewPage | admin:education_admin | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| API-ADMIN-COURSE | API_ADMIN_COURSERequest | CourseView | admin:education_admin | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| API-ADMIN-COURSE-CREATE | API_ADMIN_COURSE_CREATERequest | CourseView | admin:education_admin | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| API-ADMIN-COURSE-UPDATE | API_ADMIN_COURSE_UPDATERequest | CourseView | admin:education_admin | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| API-ADMIN-COURSE-PUBLISH | API_ADMIN_COURSE_PUBLISHRequest | CourseView | admin:education_admin | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| API-ADMIN-COURSE-ARCHIVE | API_ADMIN_COURSE_ARCHIVERequest | CourseView | admin:education_admin | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| API-ADMIN-REVISION-LIST | API_ADMIN_REVISION_LISTRequest | CurriculumRevisionViewPage | admin:education_admin | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |

## CurriculumRevisionWorkspace

- **Kind:** feature
- **Surface:** admin
- **Responsibility:** Create/copy draft curriculum revision,inspect hierarchy and freeze complete validated revision.
- **Chunk:** ZE-P11-C09
- **Expected Module:** apps/web/src/features/admin/CurriculumRevisionWorkspace.tsx
- **Composition:** ResourceTable, ModuleLessonEditor, LessonBlockEditor, RevisionResourceManager, ConfirmActionDialog
- **Reuse:** Feature-specific orchestration using shared domain and UI components
- **Input Sources:**
- **Local State:** Current revision,expanded hierarchy,publication validation report.
- **States:** loading: Keep structural headings and announce loading; disable duplicate dependent actions.; empty: Show a specific absence message and only permitted next action.; error: Field422,stale409,denied403/invisible404,expired401 and transient429/503 are distinct; show safe message/request_id and bounded retry.; success: Render authoritative returned DTO and invalidate relevant scoped query keys.; detail: Published revision read-only; copy creates new draft; cohort pins unchanged; resource/readiness/accessibility errors block publish.
- **Accessibility:** Semantic headings/labels,keyboard access,visible focus,live status,error association,200%reflow; never color alone.
- **Import Boundary:** May import shared and declared feature dependencies; generated API subset only.
- **Requirements:** ADM-008, LRN-002, LRN-003, LRN-004

| Prop | Type | Required | Source |
|---|---|---|---|
| courseId | Uuid | True | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |
| revisionId | Uuid | False | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |

| Operation | Request schema | Response schema | Roles | Ownership / state |
|---|---|---|---|---|
| API-ADMIN-REVISION-LIST | API_ADMIN_REVISION_LISTRequest | CurriculumRevisionViewPage | admin:education_admin | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| API-ADMIN-REVISION-CREATE | API_ADMIN_REVISION_CREATERequest | CurriculumRevisionView | admin:education_admin | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| API-ADMIN-REVISION-GET | API_ADMIN_REVISION_GETRequest | CurriculumRevisionView | admin:education_admin | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| API-ADMIN-REVISION-PUBLISH | API_ADMIN_REVISION_PUBLISHRequest | CurriculumRevisionView | admin:education_admin | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |

## ModuleLessonEditor

- **Kind:** feature
- **Surface:** admin
- **Responsibility:** Edit ordered draft modules/lessons,release offsets and completion-required flags.
- **Chunk:** ZE-P11-C09
- **Expected Module:** apps/web/src/features/admin/ModuleLessonEditor.tsx
- **Composition:** FormFields, ResourceTable, ConfirmActionDialog
- **Reuse:** Feature-specific orchestration using shared domain and UI components
- **Input Sources:**
- **Local State:** Selected parent/entity,order,release offset,required flags and dirty version.
- **States:** loading: Keep structural headings and announce loading; disable duplicate dependent actions.; empty: Show a specific absence message and only permitted next action.; error: Field422,stale409,denied403/invisible404,expired401 and transient429/503 are distinct; show safe message/request_id and bounded retry.; success: Render authoritative returned DTO and invalidate relevant scoped query keys.; detail: Mutations only mutable draft; no copying curriculum for new cohort; referenced/in-use delete conflicts explicit.
- **Accessibility:** Keyboard reorder controls with move-up/down; do not require drag/drop; hierarchy labels.
- **Import Boundary:** May import shared and declared feature dependencies; generated API subset only.
- **Requirements:** ADM-008, LRN-002, LRN-003, LRN-004

| Prop | Type | Required | Source |
|---|---|---|---|
| revisionId | Uuid | True | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |
| moduleId | Uuid | False | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |
| lessonId | Uuid | False | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |

| Operation | Request schema | Response schema | Roles | Ownership / state |
|---|---|---|---|---|
| API-ADMIN-MODULE-CREATE | API_ADMIN_MODULE_CREATERequest | ModuleView | admin:education_admin | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. Mutable draft revision only. |
| API-ADMIN-MODULE-UPDATE | API_ADMIN_MODULE_UPDATERequest | ModuleView | admin:education_admin | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. Mutable draft revision only. |
| API-ADMIN-MODULE-DELETE | API_ADMIN_MODULE_DELETERequest | Empty | admin:education_admin | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. No published revision or active external references. |
| API-ADMIN-LESSON-CREATE | API_ADMIN_LESSON_CREATERequest | LessonView | admin:education_admin | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. Mutable draft revision only. |
| API-ADMIN-LESSON-UPDATE | API_ADMIN_LESSON_UPDATERequest | LessonView | admin:education_admin | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. Mutable draft revision only. |
| API-ADMIN-LESSON-DELETE | API_ADMIN_LESSON_DELETERequest | Empty | admin:education_admin | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. No published revision or active external references. |
| API-ADMIN-LESSON-GET | API_ADMIN_LESSON_GETRequest | LessonView | admin:education_admin | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |

## LessonBlockEditor

- **Kind:** feature
- **Surface:** admin
- **Responsibility:** Author the closed eight block variants with per-kind fields and accessible preview.
- **Chunk:** ZE-P11-C09
- **Expected Module:** apps/web/src/features/admin/LessonBlockEditor.tsx
- **Composition:** FormFields, ResourceTable, ConfirmActionDialog
- **Reuse:** Feature-specific orchestration using shared domain and UI components
- **Input Sources:** revision_id and lesson_id come from the loaded curriculum hierarchy. Quiz list and assignment list are filtered to that same revision; selected item.id becomes the reference payload. Reject cross-revision choices before save and again on server.
- **Local State:** Kind-specific draft payload and position/required flag.
- **States:** loading: Keep structural headings and announce loading; disable duplicate dependent actions.; empty: Show a specific absence message and only permitted next action.; error: Field422,stale409,denied403/invisible404,expired401 and transient429/503 are distinct; show safe message/request_id and bounded retry.; success: Render authoritative returned DTO and invalidate relevant scoped query keys.; detail: Exactly branch fields; heading/text/image/video/download/activity/quiz/assignment refs only; image alt and video captions/transcript; no arbitrary scripts/iframe.
- **Accessibility:** Type-specific labeled forms; semantic preview; keyboard reorder; accessible validation errors.
- **Import Boundary:** May import shared and declared feature dependencies; generated API subset only.
- **Requirements:** ADM-008, ADM-010, ADM-011, ASM-001, ASM-002, ASM-003, ASM-004, LRN-002, LRN-003, LRN-004

| Prop | Type | Required | Source |
|---|---|---|---|
| revisionId | Uuid | True | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |
| lessonId | Uuid | True | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |
| blockId | Uuid | False | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |

| Operation | Request schema | Response schema | Roles | Ownership / state |
|---|---|---|---|---|
| API-ADMIN-BLOCK-CREATE | API_ADMIN_BLOCK_CREATERequest | LessonBlockView | admin:education_admin | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. Mutable draft revision only. |
| API-ADMIN-BLOCK-UPDATE | API_ADMIN_BLOCK_UPDATERequest | LessonBlockView | admin:education_admin | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. Mutable draft revision only. |
| API-ADMIN-BLOCK-DELETE | API_ADMIN_BLOCK_DELETERequest | Empty | admin:education_admin | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. No published revision or active external references. |
| API-ADMIN-QUIZZES | API_ADMIN_QUIZZESRequest | QuizViewPage | admin:education_admin | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| API-ADMIN-ASSIGNMENTS-LIST | API_ADMIN_ASSIGNMENTS_LISTRequest | AssignmentViewPage | admin:education_admin | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |

## RevisionResourceManager

- **Kind:** feature
- **Surface:** admin
- **Responsibility:** Manage draft revision learning media/download sources and upload scanned assets.
- **Chunk:** ZE-P11-C09
- **Expected Module:** apps/web/src/features/admin/RevisionResourceManager.tsx
- **Composition:** UploadControl, FormFields, ResourceTable, ProtectedDownloadAction
- **Reuse:** Feature-specific orchestration using shared domain and UI components
- **Input Sources:**
- **Local State:** Asset/source/title/kind draft and scan progress.
- **States:** loading: Keep structural headings and announce loading; disable duplicate dependent actions.; empty: Show a specific absence message and only permitted next action.; error: Field422,stale409,denied403/invisible404,expired401 and transient429/503 are distinct; show safe message/request_id and bounded retry.; success: Render authoritative returned DTO and invalidate relevant scoped query keys.; detail: education_admin; same revision; exactly one ready asset or approved external URL; published refs immutable; scanner policy read from locked storage contract.
- **Accessibility:** Semantic headings/labels,keyboard access,visible focus,live status,error association,200%reflow; never color alone.
- **Import Boundary:** May import shared and declared feature dependencies; generated API subset only.
- **Requirements:** ADM-008, ADM-023, FILE-001, FILE-002, FILE-003, FILE-004, FILE-005, FILE-006, FILE-007, LRN-002, LRN-003, LRN-004

| Prop | Type | Required | Source |
|---|---|---|---|
| revisionId | Uuid | True | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |

| Operation | Request schema | Response schema | Roles | Ownership / state |
|---|---|---|---|---|
| API-ADMIN-RESOURCE-LIST | API_ADMIN_RESOURCE_LISTRequest | ResourceViewPage | admin:education_admin | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| API-ADMIN-RESOURCE-CREATE | API_ADMIN_RESOURCE_CREATERequest | ResourceView | admin:education_admin | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. Mutable draft revision only. |
| API-ADMIN-RESOURCE-UPDATE | API_ADMIN_RESOURCE_UPDATERequest | ResourceView | admin:education_admin | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. Mutable draft revision only. |
| API-ADMIN-RESOURCE-DELETE | API_ADMIN_RESOURCE_DELETERequest | Empty | admin:education_admin | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. No published revision or active external references. |
| API-FILE-UPLOAD | API_FILE_UPLOADRequest | UploadTicketView | student, admin:education_admin, admin:operations_admin | Student own draft submission only; admin matching purpose privilege. No parent upload feature. Resolve current FileUploadContext from purpose + context_id: submission -> Submission.id from owned draft submission create/detail, same authenticated student and eligible enrolment; resource -> CurriculumRevision.id from education-admin revision list/detail, must still be writable draft; internal/public_asset -> authenticated SessionView.user_id (the same Account.id as principal), current admin:operations_admin only. No caller-selected other account/context; certificate/financial_document/financial_export are server-generated and forbidden here. Recheck immutable owner/purpose/context on confirmation and deletion; publication/release or submission finalization races reject mutation. Scan promotion checks context still permits the asset before exposing it. |
| API-FILE-CONFIRM | API_FILE_CONFIRMRequest | FileAssetView | student, admin:education_admin, admin:operations_admin | Upload owner and same original scope; uploaded object metadata/checksum must match ticket. Resolve current FileUploadContext from purpose + context_id: submission -> Submission.id from owned draft submission create/detail, same authenticated student and eligible enrolment; resource -> CurriculumRevision.id from education-admin revision list/detail, must still be writable draft; internal/public_asset -> authenticated SessionView.user_id (the same Account.id as principal), current admin:operations_admin only. No caller-selected other account/context; certificate/financial_document/financial_export are server-generated and forbidden here. Recheck immutable owner/purpose/context on confirmation and deletion; publication/release or submission finalization races reject mutation. Scan promotion checks context still permits the asset before exposing it. |
| API-FILE-GET | API_FILE_GETRequest | FileAssetView | parent, student, teacher, admin:education_admin, admin:operations_admin | FileAccessPolicy derives released curriculum, own submission, guardian link, teaching assignment or scoped admin purpose. Reject financial_document/financial_export purposes on this generic endpoint even for a parent; financial-specific BillingService/ReportingService grants are required. |
| API-FILE-DOWNLOAD | API_FILE_DOWNLOADRequest | DownloadTicketView | parent, student, teacher, admin:education_admin, admin:operations_admin | FileAccessPolicy validates ready state and linked resource scope; submission parents read only authorized child; internal files never learner-readable. Reject financial_document/financial_export purposes on this generic endpoint even for a parent; financial-specific BillingService/ReportingService grants are required. |
| API-FILE-DELETE | API_FILE_DELETERequest | Empty | student, admin:education_admin, admin:operations_admin | No referenced submitted work/published resource/certificate deletion; retention and legal hold apply. Reject financial_document/financial_export purposes on this generic endpoint even for a parent; financial-specific BillingService/ReportingService grants are required. If-Match uses current FileAsset.version obtained from API-FILE-GET, upload confirmation or permitted asset listing; delete is owner-draft/purpose scoped and still checks linked resource state. Resolve current FileUploadContext from purpose + context_id: submission -> Submission.id from owned draft submission create/detail, same authenticated student and eligible enrolment; resource -> CurriculumRevision.id from education-admin revision list/detail, must still be writable draft; internal/public_asset -> authenticated SessionView.user_id (the same Account.id as principal), current admin:operations_admin only. No caller-selected other account/context; certificate/financial_document/financial_export are server-generated and forbidden here. Recheck immutable owner/purpose/context on confirmation and deletion; publication/release or submission finalization races reject mutation. Scan promotion checks context still permits the asset before exposing it. |

## QuizDefinitionEditor

- **Kind:** feature
- **Surface:** admin
- **Responsibility:** Author immutable quiz rules and ordered questions/options/keys/approved explanations in a draft revision.
- **Chunk:** ZE-P11-C10
- **Expected Module:** apps/web/src/features/admin/QuizDefinitionEditor.tsx
- **Composition:** ResourceTable, FormFields, ConfirmActionDialog
- **Reuse:** Feature-specific orchestration using shared domain and UI components
- **Input Sources:** revisionId is authorized route context; revision GET returns modules[].lessons[].id for lesson_id selection before first quiz creation. Quiz list/detail supplies quiz/question IDs and current versions for later edits.
- **Local State:** Questions/options/closed kind/key/explanation draft with version; default limits from schema.
- **States:** loading: Keep structural headings and announce loading; disable duplicate dependent actions.; empty: Show a specific absence message and only permitted next action.; error: Field422,stale409,denied403/invisible404,expired401 and transient429/503 are distinct; show safe message/request_id and bounded retry.; success: Render authoritative returned DTO and invalidate relevant scoped query keys.; detail: education_admin only; unique question/option IDs; key refers own option; published revision immutable; no learner schema import for answer-key authoring.
- **Accessibility:** Keyboard option/reorder controls,legend groups,plain explanation validation; preview clearly authoring-only.
- **Import Boundary:** May import shared and declared feature dependencies; generated API subset only.
- **Requirements:** ADM-008, ADM-010, ASM-001, ASM-002, ASM-003, LRN-002, LRN-003, LRN-004

| Prop | Type | Required | Source |
|---|---|---|---|
| revisionId | Uuid | True | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |
| lessonId | Uuid | False | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |
| quizId | Uuid | False | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |

| Operation | Request schema | Response schema | Roles | Ownership / state |
|---|---|---|---|---|
| API-ADMIN-QUIZZES | API_ADMIN_QUIZZESRequest | QuizViewPage | admin:education_admin | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| API-ADMIN-QUIZ | API_ADMIN_QUIZRequest | QuizView | admin:education_admin | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| API-ADMIN-QUIZ-CREATE | API_ADMIN_QUIZ_CREATERequest | QuizView | admin:education_admin | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. Draft revision only. |
| API-ADMIN-QUIZ-UPDATE | API_ADMIN_QUIZ_UPDATERequest | QuizView | admin:education_admin | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. Draft revision only. |
| API-ADMIN-QUESTION-PUT | API_ADMIN_QUESTION_PUTRequest | QuizView | admin:education_admin | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. Draft only; complete validated answer key; positions unique. |
| API-ADMIN-QUIZ-DELETE | API_ADMIN_QUIZ_DELETERequest | Empty | admin:education_admin | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| API-ADMIN-REVISION-GET | API_ADMIN_REVISION_GETRequest | CurriculumRevisionView | admin:education_admin | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |

## AssignmentDefinitionEditor

- **Kind:** feature
- **Surface:** admin
- **Responsibility:** Define draft assignment/project instructions,rubric,pass score,due offset and resubmission policy.
- **Chunk:** ZE-P11-C10
- **Expected Module:** apps/web/src/features/admin/AssignmentDefinitionEditor.tsx
- **Composition:** ResourceTable, FormFields, ConfirmActionDialog
- **Reuse:** Feature-specific orchestration using shared domain and UI components
- **Input Sources:** revisionId is authorized route context; revision GET modules[].lessons[].id supplies lesson_id before first definition creation. Assignment GET supplies current definition/version for edits.
- **Local State:** Instruction/rubric/score/deadline/version draft.
- **States:** loading: Keep structural headings and announce loading; disable duplicate dependent actions.; empty: Show a specific absence message and only permitted next action.; error: Field422,stale409,denied403/invisible404,expired401 and transient429/503 are distinct; show safe message/request_id and bounded retry.; success: Render authoritative returned DTO and invalidate relevant scoped query keys.; detail: education_admin; publish freezes definition; cohort-specific closure belongs delivery workspace; late acceptance from server contract.
- **Accessibility:** Semantic headings/labels,keyboard access,visible focus,live status,error association,200%reflow; never color alone.
- **Import Boundary:** May import shared and declared feature dependencies; generated API subset only.
- **Requirements:** ADM-008, ADM-011, ASM-004, LRN-002, LRN-003, LRN-004

| Prop | Type | Required | Source |
|---|---|---|---|
| revisionId | Uuid | True | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |
| lessonId | Uuid | False | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |
| assignmentId | Uuid | False | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |

| Operation | Request schema | Response schema | Roles | Ownership / state |
|---|---|---|---|---|
| API-ADMIN-ASSIGNMENTS-LIST | API_ADMIN_ASSIGNMENTS_LISTRequest | AssignmentViewPage | admin:education_admin | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| API-ADMIN-ASSIGNMENT-GET | API_ADMIN_ASSIGNMENT_GETRequest | AssignmentView | admin:education_admin | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| API-ADMIN-ASSIGNMENT-DEFINE | API_ADMIN_ASSIGNMENT_DEFINERequest | AssignmentView | admin:education_admin | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. Draft revision only. |
| API-ADMIN-ASSIGNMENT-EDIT | API_ADMIN_ASSIGNMENT_EDITRequest | AssignmentView | admin:education_admin | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. Draft revision only. |
| API-ADMIN-ASSIGNMENT-DELETE | API_ADMIN_ASSIGNMENT_DELETERequest | Empty | admin:education_admin | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| API-ADMIN-REVISION-GET | API_ADMIN_REVISION_GETRequest | CurriculumRevisionView | admin:education_admin | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |

## AdminCohortManager

- **Kind:** feature
- **Surface:** admin
- **Responsibility:** Manage pinned curriculum cohorts,capacity and lifecycle.
- **Chunk:** ZE-P11-C05
- **Expected Module:** apps/web/src/features/admin/AdminCohortManager.tsx
- **Composition:** ResourceTable, FormFields, ConfirmActionDialog
- **Reuse:** Feature-specific orchestration using shared domain and UI components
- **Input Sources:**
- **Local State:** Selected resource, cursor, validated draft, server version and mutation pending.
- **States:** loading: Keep structural headings and announce loading; disable duplicate dependent actions.; empty: Show a specific absence message and only permitted next action.; error: Field422,stale409,denied403/invisible404,expired401 and transient429/503 are distinct; show safe message/request_id and bounded retry.; success: Render authoritative returned DTO and invalidate relevant scoped query keys.; detail: Choose course and published revision from authorized lists; show capacity conflicts; deliberate cancellation requires reason; no fee changes.
- **Accessibility:** Semantic headings/labels,keyboard access,visible focus,live status,error association,200%reflow; never color alone.
- **Import Boundary:** May import shared and declared feature dependencies; generated API subset only.
- **Requirements:** ADM-007, ADM-008, ADM-013, ADM-015, CLS-001, CLS-005, LRN-001, LRN-002, LRN-003, LRN-004

| Prop | Type | Required | Source |
|---|---|---|---|
| cohortId | Uuid | False | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |

| Operation | Request schema | Response schema | Roles | Ownership / state |
|---|---|---|---|---|
| API-ADMIN-COHORTS | API_ADMIN_COHORTSRequest | CohortViewPage | admin:education_admin | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| API-ADMIN-COHORT | API_ADMIN_COHORTRequest | CohortView | admin:education_admin | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| API-ADMIN-COHORT-CREATE | API_ADMIN_COHORT_CREATERequest | CohortView | admin:education_admin | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| API-ADMIN-COHORT-UPDATE | API_ADMIN_COHORT_UPDATERequest | CohortView | admin:education_admin | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| API-ADMIN-COHORT-STATUS | API_ADMIN_COHORT_STATUSRequest | CohortView | admin:education_admin | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| API-ADMIN-COHORT-CANCEL | API_ADMIN_COHORT_CANCELRequest | Accepted | admin:education_admin | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. Education can cancel delivery but cannot execute refund. |
| API-ADMIN-COURSES | API_ADMIN_COURSESRequest | CourseViewPage | admin:education_admin | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| API-ADMIN-REVISION-LIST | API_ADMIN_REVISION_LISTRequest | CurriculumRevisionViewPage | admin:education_admin | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |

## AdminTeachingAssignments

- **Kind:** feature
- **Surface:** admin
- **Responsibility:** Choose an approved active teacher by name and assign/revoke educational responsibility.
- **Chunk:** ZE-P11-C05
- **Expected Module:** apps/web/src/features/admin/AdminTeachingAssignments.tsx
- **Composition:** ResourceTable, FormFields, ConfirmActionDialog
- **Reuse:** Feature-specific orchestration using shared domain and UI components
- **Input Sources:** Pick teacher_id from teaching-candidates items.id and optional session_id from the selected cohort session list. Existing assignment rows supply their own state/version for revoke.
- **Local State:** Selected resource, cursor, validated draft, server version and mutation pending.
- **States:** loading: Keep structural headings and announce loading; disable duplicate dependent actions.; empty: Show a specific absence message and only permitted next action.; error: Field422,stale409,denied403/invisible404,expired401 and transient429/503 are distinct; show safe message/request_id and bounded retry.; success: Render authoritative returned DTO and invalidate relevant scoped query keys.; detail: Candidate lookup returns only id/display_name; never call identity directory or ask for opaque IDs. Server rechecks teacher approval, dates and assignment constraints.
- **Accessibility:** Semantic headings/labels,keyboard access,visible focus,live status,error association,200%reflow; never color alone.
- **Import Boundary:** May import shared and declared feature dependencies; generated API subset only.
- **Requirements:** ADM-013, ADM-014, ADM-015, CLS-001, CLS-002, CLS-003, CLS-004, CLS-005, CLS-011

| Prop | Type | Required | Source |
|---|---|---|---|
| cohortId | Uuid | True | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |

| Operation | Request schema | Response schema | Roles | Ownership / state |
|---|---|---|---|---|
| API-ADMIN-ASSIGNMENTS | API_ADMIN_ASSIGNMENTSRequest | TeacherAssignmentViewPage | admin:education_admin | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| API-ADMIN-ASSIGNMENT-CREATE | API_ADMIN_ASSIGNMENT_CREATERequest | TeacherAssignmentView | admin:education_admin | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| API-ADMIN-ASSIGNMENT-REVOKE | API_ADMIN_ASSIGNMENT_REVOKERequest | Empty | admin:education_admin | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| API-ADMIN-TEACHING-CANDIDATES | API_ADMIN_TEACHING_CANDIDATESRequest | TeachingCandidateViewPage | admin:education_admin | Active education_admin with recent MFA. Return only active teacher accounts/profiles with required staff activation approval; no identity directory, contacts, credentials, financial data or role administration. Candidate selection grants no assignment and write-time availability/status checks still apply. |
| API-ADMIN-SESSIONS | API_ADMIN_SESSIONSRequest | ClassSessionViewPage | admin:education_admin | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |

## AdminSessionPlanner

- **Kind:** feature
- **Surface:** admin
- **Responsibility:** Plan finite sessions and recurrence,preview conflicts and administer reschedule/cancel/completion.
- **Chunk:** ZE-P11-C05
- **Expected Module:** apps/web/src/features/admin/AdminSessionPlanner.tsx
- **Composition:** ScheduleView, FormFields, AuditReasonForm, ConfirmActionDialog
- **Reuse:** Feature-specific orchestration using shared domain and UI components
- **Input Sources:** cohortId is selected CohortView.id; cohort GET.revision_id supplies revision GET, whose modules[].lessons[].id supplies optional lesson_id. Session list supplies exact current session version for edit/cancel.
- **Local State:** Selected resource, cursor, validated draft, server version and mutation pending.
- **States:** loading: Keep structural headings and announce loading; disable duplicate dependent actions.; empty: Show a specific absence message and only permitted next action.; error: Field422,stale409,denied403/invisible404,expired401 and transient429/503 are distinct; show safe message/request_id and bounded retry.; success: Render authoritative returned DTO and invalidate relevant scoped query keys.; detail: Explicit IANA timezone and ambiguous offset; returned validation distinguishes DST/conflict/notice. Recurrence preview and commit use the documented request mode; no invisible bulk edits.
- **Accessibility:** Semantic headings/labels,keyboard access,visible focus,live status,error association,200%reflow; never color alone.
- **Import Boundary:** May import shared and declared feature dependencies; generated API subset only.
- **Requirements:** ADM-008, ADM-013, ADM-014, ADM-015, CLS-001, CLS-002, CLS-003, CLS-004, CLS-005, CLS-011, LRN-002, LRN-003, LRN-004

| Prop | Type | Required | Source |
|---|---|---|---|
| cohortId | Uuid | True | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |

| Operation | Request schema | Response schema | Roles | Ownership / state |
|---|---|---|---|---|
| API-ADMIN-SESSIONS | API_ADMIN_SESSIONSRequest | ClassSessionViewPage | admin:education_admin | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| API-ADMIN-SESSION-CREATE | API_ADMIN_SESSION_CREATERequest | ClassSessionView | admin:education_admin | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| API-ADMIN-RECURRENCE | API_ADMIN_RECURRENCERequest | ClassSessionViewPage | admin:education_admin | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| API-ADMIN-SESSION-UPDATE | API_ADMIN_SESSION_UPDATERequest | ClassSessionView | admin:education_admin | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| API-ADMIN-RESCHEDULE | API_ADMIN_RESCHEDULERequest | ClassSessionView | admin:education_admin | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. Override short notice requires reason; overlaps still rejected. |
| API-ADMIN-SESSION-CANCEL | API_ADMIN_SESSION_CANCELRequest | ClassSessionView | admin:education_admin | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| API-ADMIN-SESSION-COMPLETE | API_ADMIN_SESSION_COMPLETERequest | ClassSessionView | admin:education_admin | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| API-ADMIN-COHORT | API_ADMIN_COHORTRequest | CohortView | admin:education_admin | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| API-ADMIN-REVISION-GET | API_ADMIN_REVISION_GETRequest | CurriculumRevisionView | admin:education_admin | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |

## AdminEnrolmentManager

- **Kind:** feature
- **Surface:** admin
- **Responsibility:** Review educational enrolment and deliberate cancellation without financial ledger access.
- **Chunk:** ZE-P11-C05
- **Expected Module:** apps/web/src/features/admin/AdminEnrolmentManager.tsx
- **Composition:** ResourceTable, FormFields, ConfirmActionDialog
- **Reuse:** Feature-specific orchestration using shared domain and UI components
- **Input Sources:** Cohort learners items joins student_id/display_name/enrolment_id to educational enrolment rows. Identity, family contact and payment data are neither requested nor synthesized.
- **Local State:** Selected resource, cursor, validated draft, server version and mutation pending.
- **States:** loading: Keep structural headings and announce loading; disable duplicate dependent actions.; empty: Show a specific absence message and only permitted next action.; error: Field422,stale409,denied403/invisible404,expired401 and transient429/503 are distinct; show safe message/request_id and bounded retry.; success: Render authoritative returned DTO and invalidate relevant scoped query keys.; detail: Education projection only; cancellation does not pretend refund succeeded; payment management is separate finance authority.
- **Accessibility:** Semantic headings/labels,keyboard access,visible focus,live status,error association,200%reflow; never color alone.
- **Import Boundary:** May import shared and declared feature dependencies; generated API subset only.
- **Requirements:** ADM-016, ADM-017, ADM-018, ADM-019, AUTH-010, ENR-001, ENR-002, ENR-003, ENR-004, ENR-005, ENR-006, ENR-007, NFR-012

| Prop | Type | Required | Source |
|---|---|---|---|
| cohortId | Uuid | True | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |
| enrolmentId | Uuid | False | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |

| Operation | Request schema | Response schema | Roles | Ownership / state |
|---|---|---|---|---|
| API-ADMIN-ENROLMENTS | API_ADMIN_ENROLMENTSRequest | EnrolmentViewPage | admin:education_admin | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| API-ADMIN-ENROLMENT | API_ADMIN_ENROLMENTRequest | EnrolmentView | admin:education_admin | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| API-ADMIN-ENROLMENT-CANCEL | API_ADMIN_ENROLMENT_CANCELRequest | EnrolmentView | admin:education_admin | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. Any money movement requires finance workflow. |
| API-ADMIN-COHORT-LEARNERS | API_ADMIN_COHORT_LEARNERSRequest | EducationLearnerViewPage | admin:education_admin | Active administrator with education_admin and recent MFA; deny every other privilege-only principal, teacher, parent and student. Cohort-scoped educational projection only. Join only enrolments in path cohort to current first/preferred name; never access the identity directory or project contact/financial data. Downstream writes independently verify learner/enrolment/cohort match and actionable state. Empty feedback/assessment lists do not constrain the selector. |

## AdminAttendanceClosure

- **Kind:** feature
- **Surface:** admin
- **Responsibility:** Review/correct attendance and close assignment delivery with audited reasons.
- **Chunk:** ZE-P11-C05
- **Expected Module:** apps/web/src/features/admin/AdminAttendanceClosure.tsx
- **Composition:** ResourceTable, FormFields, AuditReasonForm, ConfirmActionDialog
- **Reuse:** Feature-specific orchestration using shared domain and UI components
- **Input Sources:** Selected session.id comes from cohort sessions; cohort GET.revision_id supplies assignment-list revision context. Cohort learners maps student_id/display_name/enrolment_id. Exact-student attendance GET validates membership and empty result means no row. Assignment-closure GET returns rule_exists and nullable version; use If-None-Match:* only for absence, otherwise If-Match with its positive row version. Exactly one conditional header is required for each attendance/closure PUT. Never use AssignmentView.version for delivery closure.
- **Local State:** Selected resource, cursor, validated draft, server version and mutation pending.
- **States:** loading: Keep structural headings and announce loading; disable duplicate dependent actions.; empty: Show a specific absence message and only permitted next action.; error: Field422,stale409,denied403/invisible404,expired401 and transient429/503 are distinct; show safe message/request_id and bounded retry.; success: Render authoritative returned DTO and invalidate relevant scoped query keys.; detail: Attendance and closure controls share selected delivery context; immutable corrections and release/late-state consequences shown before confirmation.
- **Accessibility:** Semantic headings/labels,keyboard access,visible focus,live status,error association,200%reflow; never color alone.
- **Import Boundary:** May import shared and declared feature dependencies; generated API subset only.
- **Requirements:** ADM-011, ADM-013, ADM-014, ADM-015, ADM-016, ADM-017, ADM-018, ADM-019, ASM-004, AUTH-010, CLS-001, CLS-002, CLS-003, CLS-004, CLS-005, CLS-010, CLS-011, NFR-012

| Prop | Type | Required | Source |
|---|---|---|---|
| cohortId | Uuid | True | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |
| sessionId | Uuid | False | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |

| Operation | Request schema | Response schema | Roles | Ownership / state |
|---|---|---|---|---|
| API-ADMIN-ATTENDANCE | API_ADMIN_ATTENDANCERequest | AttendanceViewPage | admin:education_admin | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. With exact student_id filter, first authorize that student in the session cohort, then return one persisted row or an empty items array. Empty items means no record yet, not permission to infer a version. Read never creates virtual AttendanceRecord IDs/versions; UI shows unrecorded from absence. |
| API-ADMIN-ATTENDANCE-RECORD | API_ADMIN_ATTENDANCE_RECORDRequest | AttendanceView | admin:education_admin | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. Student enrolled in this session cohort. First-write concurrency requires exactly one If-None-Match:* for absent AttendanceRecord, or If-Match current AttendanceRecord.version for existing row; never a definition, submission or other aggregate token. |
| API-ADMIN-ASSIGNMENT-CLOSE | API_ADMIN_ASSIGNMENT_CLOSERequest | AssignmentClosureView | admin:education_admin | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. First-write concurrency requires exactly one If-None-Match:* for absent AssignmentDeliveryRule, or If-Match current AssignmentDeliveryRule.version for existing row; never a definition, submission or other aggregate token. |
| API-ADMIN-ASSIGNMENTS-LIST | API_ADMIN_ASSIGNMENTS_LISTRequest | AssignmentViewPage | admin:education_admin | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| API-ADMIN-COHORT | API_ADMIN_COHORTRequest | CohortView | admin:education_admin | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| API-ADMIN-SESSIONS | API_ADMIN_SESSIONSRequest | ClassSessionViewPage | admin:education_admin | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| API-ADMIN-COHORT-LEARNERS | API_ADMIN_COHORT_LEARNERSRequest | EducationLearnerViewPage | admin:education_admin | Active administrator with education_admin and recent MFA; deny every other privilege-only principal, teacher, parent and student. Cohort-scoped educational projection only. Join only enrolments in path cohort to current first/preferred name; never access the identity directory or project contact/financial data. Downstream writes independently verify learner/enrolment/cohort match and actionable state. Empty feedback/assessment lists do not constrain the selector. |
| API-ADMIN-ASSIGNMENT-CLOSURE | API_ADMIN_ASSIGNMENT_CLOSURERequest | AssignmentClosureView | admin:education_admin | Active administrator with education_admin and recent MFA; deny every other privilege-only principal, teacher, parent and student. Cohort-scoped educational projection only. Assignment must belong to the selected cohort pinned curriculum revision; no curriculum mutation or definition token substitution. |

## AdminAssessmentOversight

- **Kind:** feature
- **Surface:** admin
- **Responsibility:** Inspect submitted work and quiz attempts,mark,return,release or withdraw educational results.
- **Chunk:** ZE-P11-C06
- **Expected Module:** apps/web/src/features/admin/AdminAssessmentOversight.tsx
- **Composition:** ResourceTable, FormFields, ReleasedResultView, AuditReasonForm, ConfirmActionDialog
- **Reuse:** Feature-specific orchestration using shared domain and UI components
- **Input Sources:** Cohort learners supplies named learner references; selected SubmissionView.assignment_id loads assignment GET/rubric. AssessmentStateView.assessment=null authoritatively means no row for an authorized frozen submission. First save uses If-None-Match:*; existing save uses assessment.version in If-Match, exactly one conditional header. Never guess a version.
- **Local State:** Selected resource, cursor, validated draft, server version and mutation pending.
- **States:** loading: Keep structural headings and announce loading; disable duplicate dependent actions.; empty: Show a specific absence message and only permitted next action.; error: Field422,stale409,denied403/invisible404,expired401 and transient429/503 are distinct; show safe message/request_id and bounded retry.; success: Render authoritative returned DTO and invalidate relevant scoped query keys.; detail: Education-admin scope, exact submission version; draft/released state prominent; opening a resource does not publish it.
- **Accessibility:** Semantic headings/labels,keyboard access,visible focus,live status,error association,200%reflow; never color alone.
- **Import Boundary:** May import shared and declared feature dependencies; generated API subset only.
- **Requirements:** ADM-010, ADM-011, ADM-012, ADM-016, ADM-017, ADM-018, ADM-019, ADM-023, ASM-001, ASM-002, ASM-003, ASM-004, ASM-005, ASM-006, ASM-007, AUTH-010, FILE-001, FILE-002, FILE-003, FILE-004, FILE-005, FILE-006, FILE-007, NFR-012

| Prop | Type | Required | Source |
|---|---|---|---|
| cohortId | Uuid | True | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |
| submissionId | Uuid | False | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |

| Operation | Request schema | Response schema | Roles | Ownership / state |
|---|---|---|---|---|
| API-ADMIN-QUIZ-RESULTS | API_ADMIN_QUIZ_RESULTSRequest | QuizAttemptViewPage | admin:education_admin | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| API-ADMIN-SUBMISSIONS | API_ADMIN_SUBMISSIONSRequest | SubmissionViewPage | admin:education_admin | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| API-ADMIN-SUBMISSION | API_ADMIN_SUBMISSIONRequest | SubmissionView | admin:education_admin | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| API-ADMIN-RETURN | API_ADMIN_RETURNRequest | SubmissionView | admin:education_admin | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| API-ADMIN-ASSESSMENT | API_ADMIN_ASSESSMENTRequest | AssessmentView | admin:education_admin | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. First-write concurrency requires exactly one If-None-Match:* for absent Assessment, or If-Match current Assessment.version for existing row; never a definition, submission or other aggregate token. |
| API-ADMIN-ASSESSMENT-GET | API_ADMIN_ASSESSMENT_GETRequest | AssessmentStateView | admin:education_admin | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. Return AssessmentStateView only after authorizing an existing frozen submission. assessment=null proves absence; never confuse unauthorized/missing submission with a creatable assessment. |
| API-ADMIN-ASSESSMENT-RELEASE | API_ADMIN_ASSESSMENT_RELEASERequest | AssessmentView | admin:education_admin | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| API-ADMIN-ASSESSMENT-WITHDRAW | API_ADMIN_ASSESSMENT_WITHDRAWRequest | AssessmentView | admin:education_admin | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| API-FILE-GET | API_FILE_GETRequest | FileAssetView | parent, student, teacher, admin:education_admin, admin:operations_admin | FileAccessPolicy derives released curriculum, own submission, guardian link, teaching assignment or scoped admin purpose. Reject financial_document/financial_export purposes on this generic endpoint even for a parent; financial-specific BillingService/ReportingService grants are required. |
| API-FILE-DOWNLOAD | API_FILE_DOWNLOADRequest | DownloadTicketView | parent, student, teacher, admin:education_admin, admin:operations_admin | FileAccessPolicy validates ready state and linked resource scope; submission parents read only authorized child; internal files never learner-readable. Reject financial_document/financial_export purposes on this generic endpoint even for a parent; financial-specific BillingService/ReportingService grants are required. |
| API-ADMIN-ASSIGNMENT-GET | API_ADMIN_ASSIGNMENT_GETRequest | AssignmentView | admin:education_admin | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| API-ADMIN-COHORT-LEARNERS | API_ADMIN_COHORT_LEARNERSRequest | EducationLearnerViewPage | admin:education_admin | Active administrator with education_admin and recent MFA; deny every other privilege-only principal, teacher, parent and student. Cohort-scoped educational projection only. Join only enrolments in path cohort to current first/preferred name; never access the identity directory or project contact/financial data. Downstream writes independently verify learner/enrolment/cohort match and actionable state. Empty feedback/assessment lists do not constrain the selector. |

## AdminFeedbackOversight

- **Kind:** feature
- **Surface:** admin
- **Responsibility:** Manage educational feedback drafts,corrections and release history.
- **Chunk:** ZE-P11-C06
- **Expected Module:** apps/web/src/features/admin/AdminFeedbackOversight.tsx
- **Composition:** ResourceTable, FormFields, ConfirmActionDialog
- **Reuse:** Feature-specific orchestration using shared domain and UI components
- **Input Sources:** Cohort learners supplies student_id/display_name for first feedback selection even if feedback list is empty. Feedback rows supply exact current feedback IDs/versions and publication state.
- **Local State:** Selected resource, cursor, validated draft, server version and mutation pending.
- **States:** loading: Keep structural headings and announce loading; disable duplicate dependent actions.; empty: Show a specific absence message and only permitted next action.; error: Field422,stale409,denied403/invisible404,expired401 and transient429/503 are distinct; show safe message/request_id and bounded retry.; success: Render authoritative returned DTO and invalidate relevant scoped query keys.; detail: Draft text remains staff-only; release is a separate explicit action; withdrawal refetches learner-safe projections.
- **Accessibility:** Semantic headings/labels,keyboard access,visible focus,live status,error association,200%reflow; never color alone.
- **Import Boundary:** May import shared and declared feature dependencies; generated API subset only.
- **Requirements:** ADM-016, ADM-017, ADM-018, ADM-019, ASM-008, AUTH-010, NFR-012

| Prop | Type | Required | Source |
|---|---|---|---|
| cohortId | Uuid | True | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |
| studentId | Uuid | False | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |

| Operation | Request schema | Response schema | Roles | Ownership / state |
|---|---|---|---|---|
| API-ADMIN-FEEDBACK-LIST | API_ADMIN_FEEDBACK_LISTRequest | FeedbackViewPage | admin:education_admin | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| API-ADMIN-FEEDBACK-CREATE | API_ADMIN_FEEDBACK_CREATERequest | FeedbackView | admin:education_admin | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| API-ADMIN-FEEDBACK-UPDATE | API_ADMIN_FEEDBACK_UPDATERequest | FeedbackView | admin:education_admin | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| API-ADMIN-FEEDBACK-RELEASE | API_ADMIN_FEEDBACK_RELEASERequest | FeedbackView | admin:education_admin | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| API-ADMIN-FEEDBACK-WITHDRAW | API_ADMIN_FEEDBACK_WITHDRAWRequest | FeedbackView | admin:education_admin | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| API-ADMIN-COHORT-LEARNERS | API_ADMIN_COHORT_LEARNERSRequest | EducationLearnerViewPage | admin:education_admin | Active administrator with education_admin and recent MFA; deny every other privilege-only principal, teacher, parent and student. Cohort-scoped educational projection only. Join only enrolments in path cohort to current first/preferred name; never access the identity directory or project contact/financial data. Downstream writes independently verify learner/enrolment/cohort match and actionable state. Empty feedback/assessment lists do not constrain the selector. |

## AdminCompletionCertificates

- **Kind:** feature
- **Surface:** admin
- **Responsibility:** Review progress,record evidenced completion override and administer certificates.
- **Chunk:** ZE-P11-C06
- **Expected Module:** apps/web/src/features/admin/AdminCompletionCertificates.tsx
- **Composition:** ProgressSummary, CertificateCard, ResourceTable, AuditReasonForm, ConfirmActionDialog
- **Reuse:** Feature-specific orchestration using shared domain and UI components
- **Input Sources:** Cohort learners supplies named enrolment_id. Completion history for that enrolment supplies progress_version and active_override_id; REVOKE_OVERRIDE sends that active ID only. All review decisions use progress_version. No learner/parent access to override evidence.
- **Local State:** Selected resource, cursor, validated draft, server version and mutation pending.
- **States:** loading: Keep structural headings and announce loading; disable duplicate dependent actions.; empty: Show a specific absence message and only permitted next action.; error: Field422,stale409,denied403/invisible404,expired401 and transient429/503 are distinct; show safe message/request_id and bounded retry.; success: Render authoritative returned DTO and invalidate relevant scoped query keys.; detail: RECOMPUTE differs from GRANT_OVERRIDE/REVOKE_OVERRIDE; reason/evidence required. Pending generation has no ready download; revocation/reissue linkage remains visible.
- **Accessibility:** Semantic headings/labels,keyboard access,visible focus,live status,error association,200%reflow; never color alone.
- **Import Boundary:** May import shared and declared feature dependencies; generated API subset only.
- **Requirements:** ADM-016, ADM-017, ADM-018, ADM-019, ADM-020, ADM-023, AUTH-010, FILE-001, FILE-002, FILE-003, FILE-004, FILE-005, FILE-006, FILE-007, LRN-007, LRN-008, LRN-009, LRN-010, NFR-012

| Prop | Type | Required | Source |
|---|---|---|---|
| cohortId | Uuid | True | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |
| enrolmentId | Uuid | False | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |

| Operation | Request schema | Response schema | Roles | Ownership / state |
|---|---|---|---|---|
| API-ADMIN-PROGRESS | API_ADMIN_PROGRESSRequest | ProgressViewPage | admin:education_admin | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| API-ADMIN-COMPLETION-REVIEW | API_ADMIN_COMPLETION_REVIEWRequest | ProgressView | admin:education_admin | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. education_admin may recompute standard eligibility, grant override with verified evidence and reason, or revoke prior override. Source learning records and attendance remain immutable. If-Match is StudentProgress.version from API-ADMIN-COMPLETION-HISTORY. REVOKE_OVERRIDE must name the same enrolment current active override; reject foreign, inactive or stale state. |
| API-ADMIN-CERTIFICATES | API_ADMIN_CERTIFICATESRequest | CertificateViewPage | admin:education_admin | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| API-ADMIN-CERTIFICATE-ISSUE | API_ADMIN_CERTIFICATE_ISSUERequest | CertificateView | admin:education_admin | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| API-ADMIN-CERTIFICATE-REVOKE | API_ADMIN_CERTIFICATE_REVOKERequest | CertificateView | admin:education_admin | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| API-ADMIN-CERTIFICATE-REISSUE | API_ADMIN_CERTIFICATE_REISSUERequest | CertificateView | admin:education_admin | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| API-FILE-GET | API_FILE_GETRequest | FileAssetView | parent, student, teacher, admin:education_admin, admin:operations_admin | FileAccessPolicy derives released curriculum, own submission, guardian link, teaching assignment or scoped admin purpose. Reject financial_document/financial_export purposes on this generic endpoint even for a parent; financial-specific BillingService/ReportingService grants are required. |
| API-FILE-DOWNLOAD | API_FILE_DOWNLOADRequest | DownloadTicketView | parent, student, teacher, admin:education_admin, admin:operations_admin | FileAccessPolicy validates ready state and linked resource scope; submission parents read only authorized child; internal files never learner-readable. Reject financial_document/financial_export purposes on this generic endpoint even for a parent; financial-specific BillingService/ReportingService grants are required. |
| API-ADMIN-COMPLETION-HISTORY | API_ADMIN_COMPLETION_HISTORYRequest | CompletionReviewView | admin:education_admin | Active administrator with education_admin and recent MFA; deny every other privilege-only principal, teacher, parent and student. Cohort-scoped educational projection only. Enrolment must belong to an accessible existing cohort. Excludes identity/contact, payment and file content. Parent/student/teacher progress projections never contain override evidence. Completion review requires active/completed enrolment and initialized persisted StudentProgress; pending initialization returns INVALID_STATE and no guessed token. |
| API-ADMIN-COHORT-LEARNERS | API_ADMIN_COHORT_LEARNERSRequest | EducationLearnerViewPage | admin:education_admin | Active administrator with education_admin and recent MFA; deny every other privilege-only principal, teacher, parent and student. Cohort-scoped educational projection only. Join only enrolments in path cohort to current first/preferred name; never access the identity directory or project contact/financial data. Downstream writes independently verify learner/enrolment/cohort match and actionable state. Empty feedback/assessment lists do not constrain the selector. |

## AdminPriceSettings

- **Kind:** feature
- **Surface:** admin
- **Responsibility:** Configure approved fees and immutable merchant/tax settings.
- **Chunk:** ZE-P11-C07
- **Expected Module:** apps/web/src/features/admin/AdminPriceSettings.tsx
- **Composition:** MoneyText, ResourceTable, FormFields, AuditReasonForm, ConfirmActionDialog
- **Reuse:** Feature-specific orchestration using shared domain and UI components
- **Input Sources:** Select API-ADMIN-PRICE-TARGETS eligible named course/cohort target, including draft/unpriced targets; use its course_id and nullable cohort_id. Existing prices are not the selector and education directories are not requested.
- **Local State:** Selected resource, cursor, validated draft, server version and mutation pending.
- **States:** loading: Keep structural headings and announce loading; disable duplicate dependent actions.; empty: Show a specific absence message and only permitted next action.; error: Field422,stale409,denied403/invisible404,expired401 and transient429/503 are distinct; show safe message/request_id and bounded retry.; success: Render authoritative returned DTO and invalidate relevant scoped query keys.; detail: Finance only; integer minor units; immutable effective ranges and purchase snapshots; no secret values. Required human merchant approval remains explicit.
- **Accessibility:** Semantic headings/labels,keyboard access,visible focus,live status,error association,200%reflow; never color alone.
- **Import Boundary:** May import shared and declared feature dependencies; generated API subset only.
- **Requirements:** ADM-024, ADM-025, AUTH-010, NFR-012, PAY-001, PAY-002, PAY-003, PAY-006, PAY-007, PAY-009, PAY-011, PAY-012

| Prop | Type | Required | Source |
|---|---|---|---|
| courseId | Uuid | False | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |
| cohortId | Uuid | False | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |

| Operation | Request schema | Response schema | Roles | Ownership / state |
|---|---|---|---|---|
| API-ADMIN-PRICES | API_ADMIN_PRICESRequest | PriceConfigViewPage | admin:finance_admin | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| API-ADMIN-PRICE-CREATE | API_ADMIN_PRICE_CREATERequest | PriceConfigView | admin:finance_admin | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| API-ADMIN-PRICE-RETIRE | API_ADMIN_PRICE_RETIRERequest | PriceConfigView | admin:finance_admin | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| API-ADMIN-FINANCE-SETTINGS | API_ADMIN_FINANCE_SETTINGSRequest | SettingViewPage | admin:finance_admin | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| API-ADMIN-FINANCE-SETTING-PUT | API_ADMIN_FINANCE_SETTING_PUTRequest | SettingView | admin:finance_admin | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| API-ADMIN-PRICE-TARGETS | API_ADMIN_PRICE_TARGETSRequest | PriceTargetViewPage | admin:finance_admin | Authenticated active administrator with finance_admin and recent MFA. Return only target kind,course/cohort IDs,titles and lifecycle labels, including unpublished and unpriced courses/cohorts. Deny public,parent,student,teacher and non-finance administrators. Do not join or return curriculum revisions/modules/lessons/resources/answer keys,learner rosters,staff identity,private sessions or financial transactions. No education-admin capability is inferred or granted. Subsequent price creation validates selected course/cohort correspondence and existing pricing rules again. |

## AdminPaymentExceptions

- **Kind:** feature
- **Surface:** admin
- **Responsibility:** Inspect payments,reconcile provider truth and resolve late paid-seat exceptions.
- **Chunk:** ZE-P11-C07
- **Expected Module:** apps/web/src/features/admin/AdminPaymentExceptions.tsx
- **Composition:** MoneyText, ResourceTable, AuditReasonForm, ConfirmActionDialog
- **Reuse:** Feature-specific orchestration using shared domain and UI components
- **Input Sources:**
- **Local State:** Selected resource, cursor, validated draft, server version and mutation pending.
- **States:** loading: Keep structural headings and announce loading; disable duplicate dependent actions.; empty: Show a specific absence message and only permitted next action.; error: Field422,stale409,denied403/invisible404,expired401 and transient429/503 are distinct; show safe message/request_id and bounded retry.; success: Render authoritative returned DTO and invalidate relevant scoped query keys.; detail: Finance only; ALLOCATE/REFUND explicit and serialized; stable idempotency key plus version; no optimistic paid/seat success. Document link issuance uses the operation-provided financial grant.
- **Accessibility:** Semantic headings/labels,keyboard access,visible focus,live status,error association,200%reflow; never color alone.
- **Import Boundary:** May import shared and declared feature dependencies; generated API subset only.
- **Requirements:** ADM-025, ENR-007, PAR-017, PAR-018, PAR-019, PAR-020, PAY-002, PAY-003, PAY-006, PAY-007, PAY-009, PAY-011, PAY-012

| Prop | Type | Required | Source |
|---|---|---|---|
| paymentId | Uuid | False | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |

| Operation | Request schema | Response schema | Roles | Ownership / state |
|---|---|---|---|---|
| API-ADMIN-PAYMENTS | API_ADMIN_PAYMENTSRequest | AdminPaymentViewPage | admin:finance_admin | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| API-ADMIN-PAYMENT | API_ADMIN_PAYMENTRequest | AdminPaymentView | admin:finance_admin | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| API-ADMIN-PAYMENT-RECONCILE | API_ADMIN_PAYMENT_RECONCILERequest | Accepted | admin:finance_admin | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| API-ADMIN-DOCUMENTS | API_ADMIN_DOCUMENTSRequest | ReceiptViewPage | admin:finance_admin | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| API-ADMIN-PAID-EXCEPTION | API_ADMIN_PAID_EXCEPTIONRequest | AdminPaymentView | admin:finance_admin | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. Lock Payment+Enrolment+Cohort; ALLOCATE requires available seat and no pending refund; REFUND reserves refundable balance and prevents activation. |
| API-ADMIN-RECONCILIATION-EXCEPTIONS | API_ADMIN_RECONCILIATION_EXCEPTIONSRequest | ReconciliationExceptionViewPage | admin:finance_admin | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| API-ADMIN-RECONCILIATION-EXCEPTION-RETRY | API_ADMIN_RECONCILIATION_EXCEPTION_RETRYRequest | Accepted | admin:finance_admin | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. No manual invented payment ownership; unresolved cases remain open for documented operational repair. |

## AdminRefundManager

- **Kind:** feature
- **Surface:** admin
- **Responsibility:** Reserve full/partial refunds and review provider outcome with explicit access disposition.
- **Chunk:** ZE-P11-C07
- **Expected Module:** apps/web/src/features/admin/AdminRefundManager.tsx
- **Composition:** MoneyText, ResourceTable, FormFields, AuditReasonForm, ConfirmActionDialog
- **Reuse:** Feature-specific orchestration using shared domain and UI components
- **Input Sources:** paymentId is selected from finance payment list/route, then payment GET loads authoritative payment state/balance context before the first refund. Existing refund list alone is insufficient. Backend recomputes available amount under lock; client display never authorizes a refund.
- **Local State:** Selected resource, cursor, validated draft, server version and mutation pending.
- **States:** loading: Keep structural headings and announce loading; disable duplicate dependent actions.; empty: Show a specific absence message and only permitted next action.; error: Field422,stale409,denied403/invisible404,expired401 and transient429/503 are distinct; show safe message/request_id and bounded retry.; success: Render authoritative returned DTO and invalidate relevant scoped query keys.; detail: KEEP/CANCEL is a required business choice; pending balance displayed, overbalance409 refetches, failed provider retry uses existing reservation identity.
- **Accessibility:** Semantic headings/labels,keyboard access,visible focus,live status,error association,200%reflow; never color alone.
- **Import Boundary:** May import shared and declared feature dependencies; generated API subset only.
- **Requirements:** ADM-025, ADM-026, PAY-002, PAY-003, PAY-006, PAY-007, PAY-008, PAY-009, PAY-011, PAY-012

| Prop | Type | Required | Source |
|---|---|---|---|
| paymentId | Uuid | True | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |

| Operation | Request schema | Response schema | Roles | Ownership / state |
|---|---|---|---|---|
| API-ADMIN-REFUNDS | API_ADMIN_REFUNDSRequest | RefundViewPage | admin:finance_admin | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| API-ADMIN-REFUND-CREATE | API_ADMIN_REFUND_CREATERequest | RefundView | admin:finance_admin | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| API-ADMIN-REFUND-RETRY | API_ADMIN_REFUND_RETRYRequest | RefundView | admin:finance_admin | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| API-ADMIN-PAYMENT | API_ADMIN_PAYMENTRequest | AdminPaymentView | admin:finance_admin | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |

## AdminFinanceReports

- **Kind:** feature
- **Surface:** admin
- **Responsibility:** Read bounded finance reports and create,retrieve,download private CSV exports.
- **Chunk:** ZE-P11-C07
- **Expected Module:** apps/web/src/features/admin/AdminFinanceReports.tsx
- **Composition:** MoneyText, ResourceTable, ProtectedDownloadAction
- **Reuse:** Feature-specific orchestration using shared domain and UI components
- **Input Sources:**
- **Local State:** Selected resource, cursor, validated draft, server version and mutation pending.
- **States:** loading: Keep structural headings and announce loading; disable duplicate dependent actions.; empty: Show a specific absence message and only permitted next action.; error: Field422,stale409,denied403/invisible404,expired401 and transient429/503 are distinct; show safe message/request_id and bounded retry.; success: Render authoritative returned DTO and invalidate relevant scoped query keys.; detail: Report range<=366days; show requested/processing/ready/failed/expired. Poll authorized status, download ready/unexpired only, sanitized failure reason; replacement request uses new idempotency key. Never use generic file API for financial exports.
- **Accessibility:** Semantic headings/labels,keyboard access,visible focus,live status,error association,200%reflow; never color alone.
- **Import Boundary:** May import shared and declared feature dependencies; generated API subset only.
- **Requirements:** ADM-027, PAY-010

| Prop | Type | Required | Source |
|---|---|---|---|
| exportId | Uuid | False | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |

| Operation | Request schema | Response schema | Roles | Ownership / state |
|---|---|---|---|---|
| API-ADMIN-REPORT | API_ADMIN_REPORTRequest | FinanceReportView | admin:finance_admin | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| API-ADMIN-REPORT-EXPORT | API_ADMIN_REPORT_EXPORTRequest | ExportView | admin:finance_admin | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| API-ADMIN-REPORT-EXPORT-STATUS | API_ADMIN_REPORT_EXPORT_STATUSRequest | ExportView | admin:finance_admin | Authenticated finance_admin with active account and recent MFA, requesting the export or explicitly authorized finance oversight; status read permits every defined ExportView state and never requires a ready asset. Deny parent, student, teacher and non-finance admin. |
| API-ADMIN-REPORT-EXPORT-DOWNLOAD | API_ADMIN_REPORT_EXPORT_DOWNLOADRequest | DownloadTicketView | admin:finance_admin | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. Ready generated financial_export; initiated by this principal or explicitly privileged finance oversight; no generic teaching file grant. |

## AdminEventsAnnouncements

- **Kind:** feature
- **Surface:** admin
- **Responsibility:** Create and deliberately publish audience-scoped events and announcements.
- **Chunk:** ZE-P11-C08
- **Expected Module:** apps/web/src/features/admin/AdminEventsAnnouncements.tsx
- **Composition:** ResourceTable, FormFields, ConfirmActionDialog
- **Reuse:** Feature-specific orchestration using shared domain and UI components
- **Input Sources:** Public audience has no target ID. Closed role audience uses the allowed role enum. Course audience selects CourseView.id/title from education course list; cohort audience selects CohortView.id/title from cohort list. Never promise recipient counts.
- **Local State:** Selected resource, cursor, validated draft, server version and mutation pending.
- **States:** loading: Keep structural headings and announce loading; disable duplicate dependent actions.; empty: Show a specific absence message and only permitted next action.; error: Field422,stale409,denied403/invisible404,expired401 and transient429/503 are distinct; show safe message/request_id and bounded retry.; success: Render authoritative returned DTO and invalidate relevant scoped query keys.; detail: Education-admin grant; closed public/role/course/cohort audience rules. Preview selected authorized role/course/cohort labels only; no recipient counts or arbitrary user directory. Publish/withdraw is explicit.
- **Accessibility:** Semantic headings/labels,keyboard access,visible focus,live status,error association,200%reflow; never color alone.
- **Import Boundary:** May import shared and declared feature dependencies; generated API subset only.
- **Requirements:** ADM-007, ADM-013, ADM-015, ADM-021, CLS-001, CLS-005, COM-001, COM-002, COM-003, COM-004, COM-005, COM-006, COM-008, COM-009, LRN-001

| Prop | Type | Required | Source |
|---|---|---|---|
| kind | event\|announcement | True | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |

| Operation | Request schema | Response schema | Roles | Ownership / state |
|---|---|---|---|---|
| API-ADMIN-EVENT-LIST | API_ADMIN_EVENT_LISTRequest | EventViewPage | admin:education_admin | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| API-ADMIN-EVENT-CREATE | API_ADMIN_EVENT_CREATERequest | EventView | admin:education_admin | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| API-ADMIN-EVENT-UPDATE | API_ADMIN_EVENT_UPDATERequest | EventView | admin:education_admin | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| API-ADMIN-EVENT-PUBLISH | API_ADMIN_EVENT_PUBLISHRequest | EventView | admin:education_admin | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| API-ADMIN-EVENT-WITHDRAW | API_ADMIN_EVENT_WITHDRAWRequest | EventView | admin:education_admin | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| API-ADMIN-ANNOUNCEMENT-LIST | API_ADMIN_ANNOUNCEMENT_LISTRequest | AnnouncementViewPage | admin:education_admin | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| API-ADMIN-ANNOUNCEMENT-CREATE | API_ADMIN_ANNOUNCEMENT_CREATERequest | AnnouncementView | admin:education_admin | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| API-ADMIN-ANNOUNCEMENT-UPDATE | API_ADMIN_ANNOUNCEMENT_UPDATERequest | AnnouncementView | admin:education_admin | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| API-ADMIN-ANNOUNCEMENT-PUBLISH | API_ADMIN_ANNOUNCEMENT_PUBLISHRequest | AnnouncementView | admin:education_admin | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| API-ADMIN-ANNOUNCEMENT-WITHDRAW | API_ADMIN_ANNOUNCEMENT_WITHDRAWRequest | AnnouncementView | admin:education_admin | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| API-ADMIN-COURSES | API_ADMIN_COURSESRequest | CourseViewPage | admin:education_admin | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| API-ADMIN-COHORTS | API_ADMIN_COHORTSRequest | CohortViewPage | admin:education_admin | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |

## AdminDeliveryDesk

- **Kind:** feature
- **Surface:** admin
- **Responsibility:** Inspect safe notification delivery state and retry authorized failures.
- **Chunk:** ZE-P11-C08
- **Expected Module:** apps/web/src/features/admin/AdminDeliveryDesk.tsx
- **Composition:** ResourceTable, FormFields, ConfirmActionDialog
- **Reuse:** Feature-specific orchestration using shared domain and UI components
- **Input Sources:**
- **Local State:** Selected resource, cursor, validated draft, server version and mutation pending.
- **States:** loading: Keep structural headings and announce loading; disable duplicate dependent actions.; empty: Show a specific absence message and only permitted next action.; error: Field422,stale409,denied403/invisible404,expired401 and transient429/503 are distinct; show safe message/request_id and bounded retry.; success: Render authoritative returned DTO and invalidate relevant scoped query keys.; detail: Operations-admin only; no raw message bodies, child work, host credentials or payment ledger; ambiguous outcomes reconcile before resend.
- **Accessibility:** Semantic headings/labels,keyboard access,visible focus,live status,error association,200%reflow; never color alone.
- **Import Boundary:** May import shared and declared feature dependencies; generated API subset only.
- **Requirements:** ADM-022, COM-007

| Prop | Type | Required | Source |
|---|---|---|---|
| deliveryId | Uuid | False | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |

| Operation | Request schema | Response schema | Roles | Ownership / state |
|---|---|---|---|---|
| API-ADMIN-DELIVERIES | API_ADMIN_DELIVERIESRequest | DeliveryViewPage | admin:operations_admin | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| API-ADMIN-DELIVERY-RETRY | API_ADMIN_DELIVERY_RETRYRequest | Accepted | admin:operations_admin | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |

## AdminAssetDesk

- **Kind:** feature
- **Surface:** admin
- **Responsibility:** Inspect and manage permitted private educational or operational assets.
- **Chunk:** ZE-P11-C08
- **Expected Module:** apps/web/src/features/admin/AdminAssetDesk.tsx
- **Composition:** UploadControl, ResourceTable, ProtectedDownloadAction, ConfirmActionDialog
- **Reuse:** Feature-specific orchestration using shared domain and UI components
- **Input Sources:** Standalone new upload permits only internal/public_asset with current authenticated SessionView.user_id == Account.id, rechecked by server and capability. Curriculum resource creation occurs only through RevisionResourceManager with its loaded writable revision. This admin desk never creates submission uploads. Existing authorized asset inspect/delete uses FileAssetView.id/version; no typed arbitrary context IDs.
- **Local State:** Selected resource, cursor, validated draft, server version and mutation pending.
- **States:** loading: Keep structural headings and announce loading; disable duplicate dependent actions.; empty: Show a specific absence message and only permitted next action.; error: Field422,stale409,denied403/invisible404,expired401 and transient429/503 are distinct; show safe message/request_id and bounded retry.; success: Render authoritative returned DTO and invalidate relevant scoped query keys.; detail: Purpose-scoped permissions; quarantine never downloadable; references/holds block delete; generic list/grants exclude generated financial documents/exports.
- **Accessibility:** Semantic headings/labels,keyboard access,visible focus,live status,error association,200%reflow; never color alone.
- **Import Boundary:** May import shared and declared feature dependencies; generated API subset only.
- **Requirements:** ADM-023, FILE-001, FILE-002, FILE-003, FILE-004, FILE-005, FILE-006, FILE-007

| Prop | Type | Required | Source |
|---|---|---|---|
| purpose | PermittedFilePurpose | True | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |

| Operation | Request schema | Response schema | Roles | Ownership / state |
|---|---|---|---|---|
| API-ADMIN-FILES | API_ADMIN_FILESRequest | FileAssetViewPage | admin:education_admin, admin:operations_admin | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| API-FILE-UPLOAD | API_FILE_UPLOADRequest | UploadTicketView | student, admin:education_admin, admin:operations_admin | Student own draft submission only; admin matching purpose privilege. No parent upload feature. Resolve current FileUploadContext from purpose + context_id: submission -> Submission.id from owned draft submission create/detail, same authenticated student and eligible enrolment; resource -> CurriculumRevision.id from education-admin revision list/detail, must still be writable draft; internal/public_asset -> authenticated SessionView.user_id (the same Account.id as principal), current admin:operations_admin only. No caller-selected other account/context; certificate/financial_document/financial_export are server-generated and forbidden here. Recheck immutable owner/purpose/context on confirmation and deletion; publication/release or submission finalization races reject mutation. Scan promotion checks context still permits the asset before exposing it. |
| API-FILE-CONFIRM | API_FILE_CONFIRMRequest | FileAssetView | student, admin:education_admin, admin:operations_admin | Upload owner and same original scope; uploaded object metadata/checksum must match ticket. Resolve current FileUploadContext from purpose + context_id: submission -> Submission.id from owned draft submission create/detail, same authenticated student and eligible enrolment; resource -> CurriculumRevision.id from education-admin revision list/detail, must still be writable draft; internal/public_asset -> authenticated SessionView.user_id (the same Account.id as principal), current admin:operations_admin only. No caller-selected other account/context; certificate/financial_document/financial_export are server-generated and forbidden here. Recheck immutable owner/purpose/context on confirmation and deletion; publication/release or submission finalization races reject mutation. Scan promotion checks context still permits the asset before exposing it. |
| API-FILE-GET | API_FILE_GETRequest | FileAssetView | parent, student, teacher, admin:education_admin, admin:operations_admin | FileAccessPolicy derives released curriculum, own submission, guardian link, teaching assignment or scoped admin purpose. Reject financial_document/financial_export purposes on this generic endpoint even for a parent; financial-specific BillingService/ReportingService grants are required. |
| API-FILE-DOWNLOAD | API_FILE_DOWNLOADRequest | DownloadTicketView | parent, student, teacher, admin:education_admin, admin:operations_admin | FileAccessPolicy validates ready state and linked resource scope; submission parents read only authorized child; internal files never learner-readable. Reject financial_document/financial_export purposes on this generic endpoint even for a parent; financial-specific BillingService/ReportingService grants are required. |
| API-FILE-DELETE | API_FILE_DELETERequest | Empty | student, admin:education_admin, admin:operations_admin | No referenced submitted work/published resource/certificate deletion; retention and legal hold apply. Reject financial_document/financial_export purposes on this generic endpoint even for a parent; financial-specific BillingService/ReportingService grants are required. If-Match uses current FileAsset.version obtained from API-FILE-GET, upload confirmation or permitted asset listing; delete is owner-draft/purpose scoped and still checks linked resource state. Resolve current FileUploadContext from purpose + context_id: submission -> Submission.id from owned draft submission create/detail, same authenticated student and eligible enrolment; resource -> CurriculumRevision.id from education-admin revision list/detail, must still be writable draft; internal/public_asset -> authenticated SessionView.user_id (the same Account.id as principal), current admin:operations_admin only. No caller-selected other account/context; certificate/financial_document/financial_export are server-generated and forbidden here. Recheck immutable owner/purpose/context on confirmation and deletion; publication/release or submission finalization races reject mutation. Scan promotion checks context still permits the asset before exposing it. |

## AdminSettingsIntegrations

- **Kind:** feature
- **Surface:** admin
- **Responsibility:** Manage typed approved operational settings and masked provider configuration.
- **Chunk:** ZE-P11-C08
- **Expected Module:** apps/web/src/features/admin/AdminSettingsIntegrations.tsx
- **Composition:** FormFields, ResourceTable, AuditReasonForm, ConfirmActionDialog
- **Reuse:** Feature-specific orchestration using shared domain and UI components
- **Input Sources:**
- **Local State:** Selected resource, cursor, validated draft, server version and mutation pending.
- **States:** loading: Keep structural headings and announce loading; disable duplicate dependent actions.; empty: Show a specific absence message and only permitted next action.; error: Field422,stale409,denied403/invisible404,expired401 and transient429/503 are distinct; show safe message/request_id and bounded retry.; success: Render authoritative returned DTO and invalidate relevant scoped query keys.; detail: Closed setting keys/types and five canonical human gates; no raw secret inputs/values, only approved secret references for operators. Stripe config requires additional finance authority; masked status and safe error code.
- **Accessibility:** Semantic headings/labels,keyboard access,visible focus,live status,error association,200%reflow; never color alone.
- **Import Boundary:** May import shared and declared feature dependencies; generated API subset only.
- **Requirements:** ADM-028, OPS-003, OPS-005, OPS-008

| Prop | Type | Required | Source |
|---|---|---|---|
| None | Route/session controller obtains its own authorized state | — | No implicit client identity authority |

| Operation | Request schema | Response schema | Roles | Ownership / state |
|---|---|---|---|---|
| API-ADMIN-SETTINGS | API_ADMIN_SETTINGSRequest | SettingViewPage | admin:operations_admin | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| API-ADMIN-SETTING-PUT | API_ADMIN_SETTING_PUTRequest | SettingView | admin:operations_admin | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| API-ADMIN-INTEGRATIONS | API_ADMIN_INTEGRATIONSRequest | IntegrationStatusViewPage | admin:operations_admin | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| API-ADMIN-INTEGRATION-UPDATE | API_ADMIN_INTEGRATION_UPDATERequest | IntegrationStatusView | admin:operations_admin | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. Stripe credential/configuration additionally requires finance privilege. |
| API-ADMIN-INTEGRATION-CHECK | API_ADMIN_INTEGRATION_CHECKRequest | Accepted | admin:operations_admin | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| API-ADMIN-INTEGRATION-RESYNC | API_ADMIN_INTEGRATION_RESYNCRequest | Accepted | admin:operations_admin | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. Stripe resync requires finance privilege. |

## AdminJobOperations

- **Kind:** feature
- **Surface:** admin
- **Responsibility:** Inspect safe operational health and bounded job state,retry only authorized work.
- **Chunk:** ZE-P11-C08
- **Expected Module:** apps/web/src/features/admin/AdminJobOperations.tsx
- **Composition:** ResourceTable, FormFields, ConfirmActionDialog
- **Reuse:** Feature-specific orchestration using shared domain and UI components
- **Input Sources:**
- **Local State:** Selected resource, cursor, validated draft, server version and mutation pending.
- **States:** loading: Keep structural headings and announce loading; disable duplicate dependent actions.; empty: Show a specific absence message and only permitted next action.; error: Field422,stale409,denied403/invisible404,expired401 and transient429/503 are distinct; show safe message/request_id and bounded retry.; success: Render authoritative returned DTO and invalidate relevant scoped query keys.; detail: Filter by permitted purpose; no raw provider/job payload; recent MFA; exhausted retry remains failed and explicit retry is audited.
- **Accessibility:** Semantic headings/labels,keyboard access,visible focus,live status,error association,200%reflow; never color alone.
- **Import Boundary:** May import shared and declared feature dependencies; generated API subset only.
- **Requirements:** ADM-028, OPS-003, OPS-005, OPS-008

| Prop | Type | Required | Source |
|---|---|---|---|
| jobId | Uuid | False | Generated backend DTO, trusted route context or explicit presentation callback; no independent authorization authority |

| Operation | Request schema | Response schema | Roles | Ownership / state |
|---|---|---|---|---|
| API-ADMIN-JOBS | API_ADMIN_JOBSRequest | JobViewPage | admin:operations_admin | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| API-ADMIN-JOB | API_ADMIN_JOBRequest | JobView | admin:operations_admin, admin:finance_admin, admin:education_admin | Match job capability and initiating admin purpose; arbitrary job IDs denied. |
| API-ADMIN-JOB-RETRY | API_ADMIN_JOB_RETRYRequest | Accepted | admin:operations_admin | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. Finance jobs additionally require finance privilege; immutable original payload. |
| API-ADMIN-OPERATIONS | API_ADMIN_OPERATIONSRequest | OperationsSummaryView | admin:operations_admin | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |

## AdminAuditLog

- **Kind:** feature
- **Surface:** admin
- **Responsibility:** Read least-data append-only audit records with dedicated audit authority.
- **Chunk:** ZE-P11-C08
- **Expected Module:** apps/web/src/features/admin/AdminAuditLog.tsx
- **Composition:** ResourceTable, AsyncBoundary
- **Reuse:** Feature-specific orchestration using shared domain and UI components
- **Input Sources:**
- **Local State:** Selected resource, cursor, validated draft, server version and mutation pending.
- **States:** loading: Keep structural headings and announce loading; disable duplicate dependent actions.; empty: Show a specific absence message and only permitted next action.; error: Field422,stale409,denied403/invisible404,expired401 and transient429/503 are distinct; show safe message/request_id and bounded retry.; success: Render authoritative returned DTO and invalidate relevant scoped query keys.; detail: audit_admin only; immutable read view with bounded filters and cursor; no secrets or editable audit entries.
- **Accessibility:** Semantic headings/labels,keyboard access,visible focus,live status,error association,200%reflow; never color alone.
- **Import Boundary:** May import shared and declared feature dependencies; generated API subset only.
- **Requirements:** ADM-029, SEC-007

| Prop | Type | Required | Source |
|---|---|---|---|
| None | Route/session controller obtains its own authorized state | — | No implicit client identity authority |

| Operation | Request schema | Response schema | Roles | Ownership / state |
|---|---|---|---|---|
| API-ADMIN-AUDIT | API_ADMIN_AUDITRequest | AuditViewPage | admin:audit_admin | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |

## AdminEnquiryDesk

- **Kind:** feature
- **Surface:** admin
- **Responsibility:** Read restricted public support enquiries and record triage status.
- **Chunk:** ZE-P11-C08
- **Expected Module:** apps/web/src/features/admin/AdminEnquiryDesk.tsx
- **Composition:** ResourceTable, FormFields
- **Reuse:** Feature-specific orchestration using shared domain and UI components
- **Input Sources:**
- **Local State:** Selected resource, cursor, validated draft, server version and mutation pending.
- **States:** loading: Keep structural headings and announce loading; disable duplicate dependent actions.; empty: Show a specific absence message and only permitted next action.; error: Field422,stale409,denied403/invisible404,expired401 and transient429/503 are distinct; show safe message/request_id and bounded retry.; success: Render authoritative returned DTO and invalidate relevant scoped query keys.; detail: Operations-only contact projection; no automatic child/family matching and no new messaging feature.
- **Accessibility:** Semantic headings/labels,keyboard access,visible focus,live status,error association,200%reflow; never color alone.
- **Import Boundary:** May import shared and declared feature dependencies; generated API subset only.
- **Requirements:** WEB-009

| Prop | Type | Required | Source |
|---|---|---|---|
| None | Route/session controller obtains its own authorized state | — | No implicit client identity authority |

| Operation | Request schema | Response schema | Roles | Ownership / state |
|---|---|---|---|---|
| API-ADMIN-ENQUIRIES | API_ADMIN_ENQUIRIESRequest | ContactEnquiryViewPage | admin:operations_admin | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| API-ADMIN-ENQUIRY-STATUS | API_ADMIN_ENQUIRY_STATUSRequest | ContactEnquiryView | admin:operations_admin | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |

## AdminDashboard

- **Kind:** feature
- **Surface:** admin
- **Responsibility:** Display only the dashboard portions authorized for the current admin capabilities.
- **Chunk:** ZE-P11-C08
- **Expected Module:** apps/web/src/features/admin/AdminDashboard.tsx
- **Composition:** PageHeader, ResourceTable, NotificationList
- **Reuse:** Feature-specific orchestration using shared domain and UI components
- **Input Sources:**
- **Local State:** Selected resource, cursor, validated draft, server version and mutation pending.
- **States:** loading: Keep structural headings and announce loading; disable duplicate dependent actions.; empty: Show a specific absence message and only permitted next action.; error: Field422,stale409,denied403/invisible404,expired401 and transient429/503 are distinct; show safe message/request_id and bounded retry.; success: Render authoritative returned DTO and invalidate relevant scoped query keys.; detail: Use server-projected sections. Missing finance section remains absent for education/identity/operations principals; no client-side total assembly.
- **Accessibility:** Semantic headings/labels,keyboard access,visible focus,live status,error association,200%reflow; never color alone.
- **Import Boundary:** May import shared and declared feature dependencies; generated API subset only.
- **Requirements:** ADM-022, ADM-028, COM-007, OPS-003, OPS-005, OPS-008, PAR-016, TCH-015

| Prop | Type | Required | Source |
|---|---|---|---|
| None | Route/session controller obtains its own authorized state | — | No implicit client identity authority |

| Operation | Request schema | Response schema | Roles | Ownership / state |
|---|---|---|---|---|
| API-ADMIN-DASHBOARD | API_ADMIN_DASHBOARDRequest | DashboardView | admin:education_admin, admin:finance_admin, admin:identity_admin, admin:operations_admin | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| API-NOTIFICATIONS | API_NOTIFICATIONSRequest | NotificationViewPage | parent, student, teacher, admin | Authenticated principal owns this account/session/notification; server resolves subject, never trusts requested role. |
| API-NOTIFICATION-READ | API_NOTIFICATION_READRequest | NotificationView | parent, student, teacher, admin | Authenticated principal owns this account/session/notification; server resolves subject, never trusts requested role. |
