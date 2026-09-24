# Database schema plan

Status: DRAFT. Architecture version1.0. This is a complete proposed launch blueprint for human review. No application code is implemented. Canonical machine-readable details: [backend-catalog.json](backend-catalog.json). Requirement authority: [requirements.json](../product/requirements.json). Implementing chunk IDs are assigned by the consolidated Code Blueprint and requirement-to-chunk traceability; no catalog entry may be implemented without that assignment.

PostgreSQL16+ with Alembic-reviewed migrations and SQLAlchemy data mappers. All non-composite entity tables additionally have `created_at timestamptz NOT NULL DEFAULT now()` and mutable tables have `updated_at timestamptz NOT NULL`, maintained within the transaction; immutable audit/event/revision rows have created time only. Unless stated otherwise `id` is opaque UUID, mutable root `version bigint NOT NULL DEFAULT1`, foreign-key deletion is RESTRICT, text enums use named CHECK constraints and amounts are integer minor units. `?` below is nullable; all other listed columns are NOT NULL. Mutable counters must be nonnegative. No child optional field acquires a NOT NULL constraint by accident.

Every FK receives the listed lookup/index or a covering composite index. The mapper selects explicit columns by purpose; no `SELECT *` entity serialization. Same-family and same-revision candidate keys plus composite foreign keys enforce security-sensitive correspondence. Polymorphic operational references use closed resource kinds, explicit service validation and foreign-key link tables where educational access depends on them. API request fields are not blindly written into a table.

## accounts

| Aspect | Plan |
| --- | --- |
| Columns | id uuid PK;role text;email citext?;display_name varchar(200);status text;admin_privileges text[];mfa_enabled boolean;version bigint |
| Constraints / keys | UNIQUE(email) WHERE email IS NOT NULL; role/status CHECK; student email nullable; privilege CHECK role=admin iff nonempty allowed grants; no teacher/admin combined principal |
| Indexes | status,id; email partial unique |
| Lifecycle / deletion | Suspend/revoke immediately; close retains required records and anonymizes by approved retention decision |

## credentials

| Aspect | Plan |
| --- | --- |
| Columns | account_id uuid PK FK accounts;password_hash text;changed_at timestamptz;failed_attempts integer;locked_until timestamptz? |
| Constraints / keys | CHECK failed_attempts>=0; no plaintext field |
| Indexes | account_id |
| Lifecycle / deletion | Delete credential on final closure; account/audit history retained |

## sessions

| Aspect | Plan |
| --- | --- |
| Columns | id uuid PK;account_id uuid FK accounts;token_hash bytea;created_at timestamptz;last_seen_at timestamptz;expires_at timestamptz;revoked_at timestamptz?;mfa_verified_at timestamptz?;device_label varchar(200) |
| Constraints / keys | UNIQUE(token_hash); expiry>created |
| Indexes | account_id,revoked_at; expires_at |
| Lifecycle / deletion | Purge expired session hashes30d after expiry; security incident hold overrides |

## one_time_tokens

| Aspect | Plan |
| --- | --- |
| Columns | id uuid PK;account_id uuid FK accounts;purpose text;token_hash bytea;expires_at timestamptz;consumed_at timestamptz?;payload_ciphertext bytea? |
| Constraints / keys | UNIQUE(token_hash); purpose allowlist; consume locked exactly once |
| Indexes | expires_at; account_id,purpose |
| Lifecycle / deletion | Verification24h, recovery30m, MFA challenge5m, setup10m; hash cleanup30d |

## families

| Aspect | Plan |
| --- | --- |
| Columns | id uuid PK;status text;version bigint |
| Constraints / keys | CHECK status active/closed |
| Indexes | status,id |
| Lifecycle / deletion | No hard delete while educational or finance records retained |

## guardians

| Aspect | Plan |
| --- | --- |
| Columns | id uuid PK;account_id uuid FK accounts;family_id uuid FK families;first_name varchar(100);last_name varchar(100)?;phone varchar(32)?;optional_email boolean;version bigint |
| Constraints / keys | UNIQUE(account_id); parent role constraint through transaction validation |
| Indexes | family_id,id |
| Lifecycle / deletion | Archive contact under approved retention; do not orphan active children |

## students

| Aspect | Plan |
| --- | --- |
| Columns | id uuid PK;family_id uuid FK families;account_id uuid? FK accounts;first_name varchar(80);preferred_name varchar(80)?;last_name varchar(80)?;age_years smallint;age_recorded_on date;school_name varchar(160)?;school_year varchar(40)?;interests text[];prior_experience text?;status text;version bigint |
| Constraints / keys | Name nonempty; age technical4–18; optional school nullable; UNIQUE(account_id) WHERE not null; age_recorded_on<=current date enforced service; school_year Foundation/Year1–12/other/not_specified enum; interests approved topic array<=10 unique; prior_experience includes prefer-not-to-say |
| Indexes | family_id,status,id |
| Lifecycle / deletion | Archive only after active enrolments resolved; retention-approved anonymization; no DOB inferred |

## guardian_students

| Aspect | Plan |
| --- | --- |
| Columns | guardian_id uuid FK guardians;student_id uuid FK students;family_id uuid FK families;verified_at timestamptz;revoked_at timestamptz?;verification_reference text;version bigint |
| Constraints / keys | PK(guardian_id,student_id); composite same-family FK enforced with parent candidate keys; active child must retain guardian |
| Indexes | student_id,revoked_at; guardian_id,revoked_at |
| Lifecycle / deletion | Retain relationship evidence; revoke access immediately |

## billing_memberships

| Aspect | Plan |
| --- | --- |
| Columns | family_id uuid FK families;guardian_id uuid FK guardians;granted_at timestamptz;revoked_at timestamptz?;approval_reference text;version bigint |
| Constraints / keys | PK(family_id,guardian_id); same-family composite FK; independent of child link |
| Indexes | guardian_id,revoked_at |
| Lifecycle / deletion | Revocation immediate; retain audit evidence |

## teacher_profiles

| Aspect | Plan |
| --- | --- |
| Columns | id uuid PK;account_id uuid FK accounts;display_name varchar(200);biography text?;photo_asset_id uuid? FK file_assets;published boolean;status text;version bigint |
| Constraints / keys | UNIQUE(account_id); published requires approved biography/photo |
| Indexes | status,id; published |
| Lifecycle / deletion | Archive when no active assignments; published projection explicitly withdrawn |

## policy_documents

| Aspect | Plan |
| --- | --- |
| Columns | id uuid PK;key text;version_label varchar(80);title text;sanitized_html text;effective_at timestamptz;published_at timestamptz?;approval_reference text?;requires_acknowledgement boolean;version bigint |
| Constraints / keys | UNIQUE(key,version_label); published implies approval; published content immutable |
| Indexes | key,effective_at DESC |
| Lifecycle / deletion | Retain immutable legal versions supporting acknowledgements |

## policy_acknowledgements

| Aspect | Plan |
| --- | --- |
| Columns | id uuid PK;policy_id uuid FK policy_documents;guardian_id uuid FK guardians;family_id uuid FK families;student_id uuid? FK students;acknowledged_at timestamptz |
| Constraints / keys | UNIQUE NULLS NOT DISTINCT(policy_id,guardian_id,student_id); version-specific relation |
| Indexes | guardian_id,acknowledged_at; student_id |
| Lifecycle / deletion | Append-only evidence; retention legal approval gate |

## public_pages

| Aspect | Plan |
| --- | --- |
| Columns | id uuid PK;slug varchar(80);published_revision_id uuid? FK public_page_revisions;version bigint |
| Constraints / keys | UNIQUE(slug); fixed allowlist |
| Indexes | slug |
| Lifecycle / deletion | Keep publication history; fixed page records |

## public_page_revisions

| Aspect | Plan |
| --- | --- |
| Columns | id uuid PK;page_id uuid FK public_pages;title text;sanitized_html text;created_by uuid FK accounts;published_at timestamptz? |
| Constraints / keys | Published revision immutable; cyclic FK deferrable for initial page insert |
| Indexes | page_id,created_at DESC |
| Lifecycle / deletion | Archive superseded versions, never expose drafts publicly |

## contact_enquiries

| Aspect | Plan |
| --- | --- |
| Columns | id uuid PK;name varchar(200);email citext;message text;status text;version bigint |
| Constraints / keys | CHECK length(message)<=2000; status new/handled |
| Indexes | status,created_at |
| Lifecycle / deletion | Purge90d after closure unless approved support/legal hold |

## programs

| Aspect | Plan |
| --- | --- |
| Columns | id uuid PK;slug varchar(80);title text;summary text;status text;version bigint |
| Constraints / keys | UNIQUE(slug); draft/published/archived |
| Indexes | status,slug |
| Lifecycle / deletion | Archive referenced offering grouping |

## courses

| Aspect | Plan |
| --- | --- |
| Columns | id uuid PK;program_id uuid? FK programs;slug varchar(80);title text;summary text;learning_outcomes text[];min_age smallint;max_age smallint;duration_weeks smallint;delivery_method text;status text;current_revision_id uuid? FK curriculum_revisions;version bigint |
| Constraints / keys | UNIQUE(slug); max_age>=min_age; duration1–52; live_online only; same-course revision constraint |
| Indexes | program_id,status; status,slug |
| Lifecycle / deletion | Archive acquisition; preserve existing learning entitlements |

## curriculum_revisions

| Aspect | Plan |
| --- | --- |
| Columns | id uuid PK;course_id uuid FK courses;revision_number integer;status text;published_at timestamptz?;version bigint |
| Constraints / keys | UNIQUE(course_id,revision_number); draft/published/retired; published immutable DB write guard |
| Indexes | course_id,status |
| Lifecycle / deletion | Published revisions retained while any cohort/learning record references |

## course_modules

| Aspect | Plan |
| --- | --- |
| Columns | id uuid PK;revision_id uuid FK curriculum_revisions;title text;position integer;release_offset_days integer |
| Constraints / keys | UNIQUE(revision_id,position) DEFERRABLE; offset>=0; candidate key id,revision_id |
| Indexes | revision_id,position |
| Lifecycle / deletion | Delete only draft via aggregate; published immutable |

## lessons

| Aspect | Plan |
| --- | --- |
| Columns | id uuid PK;module_id uuid FK course_modules;revision_id uuid FK curriculum_revisions;title text;position integer;release_offset_days integer;required_for_completion boolean;version bigint |
| Constraints / keys | UNIQUE(module_id,position) DEFERRABLE; same revision composite FK; release>=module release validated |
| Indexes | revision_id; module_id,position |
| Lifecycle / deletion | Delete draft only; published retained |

## lesson_blocks

| Aspect | Plan |
| --- | --- |
| Columns | id uuid PK;lesson_id uuid FK lessons;revision_id uuid FK curriculum_revisions;kind text;position integer;content jsonb;required_for_completion boolean;version bigint |
| Constraints / keys | UNIQUE(lesson_id,position) DEFERRABLE; kind CHECK; JSON schema checked service; normalized asset/quiz/assignment refs in explicit link tables |
| Indexes | lesson_id,position; revision_id |
| Lifecycle / deletion | Draft mutable; immutable after revision publication |

## learning_resources

| Aspect | Plan |
| --- | --- |
| Columns | id uuid PK;revision_id uuid FK curriculum_revisions;title text;kind text;asset_id uuid? FK file_assets;external_url text?;status text;accessibility_metadata jsonb;version bigint |
| Constraints / keys | CHECK exactly one asset_id/external_url; ready asset; approved HTTPS URL |
| Indexes | revision_id,status |
| Lifecycle / deletion | Draft deletion only; retained while published referenced |

## cohorts

| Aspect | Plan |
| --- | --- |
| Columns | id uuid PK;course_id uuid FK courses;revision_id uuid FK curriculum_revisions;title text;capacity integer;starts_at timestamptz;ends_at timestamptz;timezone text;enrolment_opens_at timestamptz;enrolment_closes_at timestamptz;status text;version bigint |
| Constraints / keys | capacity1–100; end>start; closes<=starts; same course/revision composite FK; committed<=capacity under lock |
| Indexes | course_id,status,starts_at; status,starts_at |
| Lifecycle / deletion | No deletion after reservation; cancel lifecycle, retain records |

## class_sessions

| Aspect | Plan |
| --- | --- |
| Columns | id uuid PK;cohort_id uuid FK cohorts;lesson_id uuid? FK lessons;title text;starts_at timestamptz;ends_at timestamptz;timezone text;local_start timestamp;utc_offset_minutes integer;status text;version bigint |
| Constraints / keys | end>start; session lesson in cohort pinned revision; EXCLUDE overlapping cohort active tstzrange USING gist |
| Indexes | cohort_id,starts_at; starts_at,status |
| Lifecycle / deletion | Cancel rather than delete; preserve attendance and provider links |

## teacher_assignments

| Aspect | Plan |
| --- | --- |
| Columns | id uuid PK;teacher_id uuid FK teacher_profiles;cohort_id uuid FK cohorts;session_id uuid? FK class_sessions;role text;active_from timestamptz;active_until timestamptz?;version bigint |
| Constraints / keys | Session same cohort; active_until>from; unique active grant per teacher/cohort/session/role |
| Indexes | teacher_id,active_from,active_until; cohort_id |
| Lifecycle / deletion | Revoke with time; retain grant history |

## enrolments

| Aspect | Plan |
| --- | --- |
| Columns | id uuid PK;student_id uuid FK students;cohort_id uuid FK cohorts;status text;hold_expires_at timestamptz?;access_ends_at timestamptz?;cancellation_reason text?;version bigint |
| Constraints / keys | Partial UNIQUE(student_id,cohort_id) for held/pending/active/completed;30m hold; paid exception separate state |
| Indexes | cohort_id,status,hold_expires_at; student_id,status |
| Lifecycle / deletion | No financial deletion; expired hold retains auditable purchase relationship |

## attendance_records

| Aspect | Plan |
| --- | --- |
| Columns | id uuid PK;session_id uuid FK class_sessions;student_id uuid FK students;enrolment_id uuid FK enrolments;status text;minutes_attended integer?;recorded_by uuid FK accounts;recorded_at timestamptz;version bigint |
| Constraints / keys | UNIQUE(session_id,student_id); enrolled same cohort; minutes0–240; enum CHECK |
| Indexes | student_id,session_id; enrolment_id |
| Lifecycle / deletion | Amend with immutable audit; required completion evidence retained |

## quizzes

| Aspect | Plan |
| --- | --- |
| Columns | id uuid PK;lesson_id uuid FK lessons;revision_id uuid FK curriculum_revisions;title text;instructions text;pass_percent integer;max_attempts integer;status text;version bigint |
| Constraints / keys | pass0–100 default70; attempts1–5 default3; immutable published parent revision |
| Indexes | revision_id; lesson_id |
| Lifecycle / deletion | Draft deletion only; published retained |

## quiz_questions

| Aspect | Plan |
| --- | --- |
| Columns | id uuid PK;quiz_id uuid FK quizzes;position integer;kind text;prompt text;explanation text;points integer |
| Constraints / keys | UNIQUE(quiz_id,position); points>0; single_choice/multiple_choice |
| Indexes | quiz_id,position |
| Lifecycle / deletion | Frozen at publication |

## quiz_options

| Aspect | Plan |
| --- | --- |
| Columns | id uuid PK;question_id uuid FK quiz_questions;text text;position integer;correct boolean |
| Constraints / keys | UNIQUE(question_id,position); >=2 options and valid key count verified publication |
| Indexes | question_id,position |
| Lifecycle / deletion | Answer-key column never selected for learner question view |

## quiz_attempts

| Aspect | Plan |
| --- | --- |
| Columns | id uuid PK;quiz_id uuid FK quizzes;student_id uuid FK students;enrolment_id uuid FK enrolments;attempt_number integer;snapshot jsonb;status text;score integer?;max_score integer;passed boolean?;submitted_at timestamptz?;released_at timestamptz?;version bigint |
| Constraints / keys | UNIQUE(enrolment_id,quiz_id,attempt_number); partial UNIQUE in_progress(enrolment_id,quiz_id); snapshot immutable; attempt limit locked |
| Indexes | student_id,quiz_id; enrolment_id,status |
| Lifecycle / deletion | Submitted evidence retained; snapshot encrypted at rest DB/storage layer |

## quiz_answers

| Aspect | Plan |
| --- | --- |
| Columns | attempt_id uuid FK quiz_attempts;question_id uuid;selected_option_ids uuid[];correct boolean?;awarded_points integer?;approved_explanation text? |
| Constraints / keys | PK(attempt_id,question_id); question IDs belong snapshot; own submitted feedback only |
| Indexes | attempt_id |
| Lifecycle / deletion | No modifications after submitted; source evidence retained |

## assignments

| Aspect | Plan |
| --- | --- |
| Columns | id uuid PK;lesson_id uuid FK lessons;revision_id uuid FK curriculum_revisions;title text;instructions text;kind text;rubric text;max_score integer;passing_score integer;due_offset_days integer?;max_files integer;allow_resubmission boolean;status text;version bigint |
| Constraints / keys | passing0–max_score; max_files1–5; offset0–365; assignment/project |
| Indexes | revision_id; lesson_id |
| Lifecycle / deletion | Definition immutable in published revision |

## assignment_delivery_rules

| Aspect | Plan |
| --- | --- |
| Columns | assignment_id uuid FK assignments;cohort_id uuid FK cohorts;due_at timestamptz?;closed boolean;reason text?;version bigint |
| Constraints / keys | PK(assignment_id,cohort_id); same pinned revision; explicit closed requires reason |
| Indexes | cohort_id,closed |
| Lifecycle / deletion | Preserve resolved due time and closure audit |

## submissions

| Aspect | Plan |
| --- | --- |
| Columns | id uuid PK;assignment_id uuid FK assignments;student_id uuid FK students;enrolment_id uuid FK enrolments;attempt_number integer;previous_submission_id uuid? FK submissions;body text?;status text;late boolean;submitted_at timestamptz?;version bigint |
| Constraints / keys | UNIQUE(enrolment_id,assignment_id,attempt_number); partial unique draft; previous same assignment/student; total files<=100MiB |
| Indexes | assignment_id,status; student_id,submitted_at; enrolment_id |
| Lifecycle / deletion | Only unsubmitted draft deletable; submitted immutable |

## submission_assets

| Aspect | Plan |
| --- | --- |
| Columns | submission_id uuid FK submissions;asset_id uuid FK file_assets;position integer |
| Constraints / keys | PK(submission_id,asset_id); unique position; owner/context same; ready only |
| Indexes | asset_id |
| Lifecycle / deletion | Retain while frozen submission retained |

## assessments

| Aspect | Plan |
| --- | --- |
| Columns | id uuid PK;submission_id uuid FK submissions;assessor_id uuid FK accounts;current_revision_id uuid? FK assessment_revisions;status text;released_at timestamptz?;version bigint |
| Constraints / keys | UNIQUE(submission_id); draft/released/withdrawn; frozen submission only |
| Indexes | status,updated_at; submission_id |
| Lifecycle / deletion | Corrections create new revision, never erase source marks |

## assessment_revisions

| Aspect | Plan |
| --- | --- |
| Columns | id uuid PK;assessment_id uuid FK assessments;score integer;max_score integer;rubric_comment text;actor_id uuid FK accounts;reason text? |
| Constraints / keys | score0–max_score; immutable row; deferrable pointer cycle |
| Indexes | assessment_id,created_at DESC |
| Lifecycle / deletion | Retain assessment evidence |

## teacher_feedback

| Aspect | Plan |
| --- | --- |
| Columns | id uuid PK;student_id uuid FK students;cohort_id uuid FK cohorts;submission_id uuid? FK submissions;author_id uuid FK accounts;current_revision_id uuid? FK feedback_revisions;status text;released_at timestamptz?;version bigint |
| Constraints / keys | Submission/student/cohort correspondence; draft/released/withdrawn |
| Indexes | cohort_id,status; student_id,released_at |
| Lifecycle / deletion | Private drafts retained only approved period; released/correction evidence retained |

## feedback_revisions

| Aspect | Plan |
| --- | --- |
| Columns | id uuid PK;feedback_id uuid FK teacher_feedback;message text;actor_id uuid FK accounts;reason text? |
| Constraints / keys | Immutable revision; sanitized plain text |
| Indexes | feedback_id,created_at DESC |
| Lifecycle / deletion | Publication/withdrawal history retained |

## activity_completions

| Aspect | Plan |
| --- | --- |
| Columns | id uuid PK;enrolment_id uuid FK enrolments;lesson_id uuid FK lessons;block_id uuid? FK lesson_blocks;completed boolean;reflection text?;completed_at timestamptz?;version bigint |
| Constraints / keys | UNIQUE NULLS NOT DISTINCT(enrolment_id,lesson_id,block_id); reflection<=2000; same revision |
| Indexes | enrolment_id,completed |
| Lifecycle / deletion | Own educational state; retained per child-learning policy |

## student_progress

| Aspect | Plan |
| --- | --- |
| Columns | enrolment_id uuid PK FK enrolments;required_counts jsonb;completed_counts jsonb;delivered_sessions integer;attended_sessions integer;completion_percent integer;status text;completion_basis text;source_version bigint;version bigint |
| Constraints / keys | Counts nonnegative; percent0–100; no arbitrary writer except recompute use case |
| Indexes | status; updated_at |
| Lifecycle / deletion | Rebuildable projection; no authoritative deletion of underlying learning evidence |

## completion_overrides

| Aspect | Plan |
| --- | --- |
| Columns | id uuid PK;enrolment_id uuid FK enrolments;actor_id uuid FK accounts;reason text;evidence_references text[];granted_at timestamptz;revoked_at timestamptz?;version bigint |
| Constraints / keys | Partial UNIQUE active override(enrolment_id); nonempty evidence and reason; source learning rows untouched |
| Indexes | enrolment_id,granted_at DESC |
| Lifecycle / deletion | Append/revoke evidence, no destructive correction |

## certificates

| Aspect | Plan |
| --- | --- |
| Columns | id uuid PK;student_id uuid FK students;enrolment_id uuid FK enrolments;verification_code varchar(80);name_snapshot text;course_title_snapshot text;issued_at timestamptz?;status text;asset_id uuid? FK file_assets;replaces_id uuid? FK certificates;version bigint |
| Constraints / keys | UNIQUE(verification_code); partial UNIQUE current issued/pending enrolment; replacement same enrolment |
| Indexes | student_id,issued_at; enrolment_id |
| Lifecycle / deletion | Revoke/reissue lineage retained; no public child directory |

## prices

| Aspect | Plan |
| --- | --- |
| Columns | id uuid PK;course_id uuid FK courses;cohort_id uuid? FK cohorts;amount_minor bigint;currency char(3);tax_treatment text;tax_rate_basis_points integer;label text;active_from timestamptz;active_until timestamptz?;version bigint |
| Constraints / keys | amount>=0; AUD only; tax0–10000; exclusion effective-range overlap per course/cohort target |
| Indexes | course_id,active_from; cohort_id,active_from |
| Lifecycle / deletion | Retire instead of altering historic purchase snapshots |

## payments

| Aspect | Plan |
| --- | --- |
| Columns | id uuid PK;family_id uuid FK families;enrolment_id uuid FK enrolments;price_snapshot jsonb;merchant_snapshot jsonb;amount_minor bigint;currency char(3);status text;provider_payment_id text?;refunded_minor bigint;exception_decision text?;version bigint |
| Constraints / keys | UNIQUE(provider_payment_id) partial;0<=refunded<=amount; one succeeded purchase/enrolment; immutable purchase snapshots |
| Indexes | family_id,created_at DESC; status,updated_at; enrolment_id |
| Lifecycle / deletion | Append financial events; retain7y proposal pending accountant/legal approval |

## checkout_attempts

| Aspect | Plan |
| --- | --- |
| Columns | id uuid PK;payment_id uuid FK payments;provider_checkout_id text;expires_at timestamptz;status text;idempotency_key uuid |
| Constraints / keys | UNIQUE(provider_checkout_id); UNIQUE(payment_id,idempotency_key); one open attempt/payment |
| Indexes | payment_id,created_at DESC; expires_at,status |
| Lifecycle / deletion | Retain provider reference history across failed/expired retries |

## payment_events

| Aspect | Plan |
| --- | --- |
| Columns | id uuid PK;payment_id uuid FK payments;provider_event_id text;event_type text;verified_status text;amount_minor bigint;occurred_at timestamptz |
| Constraints / keys | UNIQUE(provider_event_id,payment_id); append-only |
| Indexes | payment_id,occurred_at |
| Lifecycle / deletion | Retain financial truth; raw event payload separately bounded |

## refunds

| Aspect | Plan |
| --- | --- |
| Columns | id uuid PK;payment_id uuid FK payments;amount_minor bigint;reason text;access_disposition text;provider_refund_id text?;idempotency_key uuid;status text;version bigint |
| Constraints / keys | amount>0; KEEP/CANCEL only; UNIQUE(provider_refund_id) partial; UNIQUE(idempotency_key); pending+success sum<=capture under lock |
| Indexes | payment_id,status; status,updated_at |
| Lifecycle / deletion | Append outcomes; no deletion; ambiguous outcome reconciled before retry |

## purchase_documents

| Aspect | Plan |
| --- | --- |
| Columns | id uuid PK;payment_id uuid FK payments;document_type text;number text;issued_at timestamptz;merchant_snapshot jsonb;purchaser_snapshot jsonb;line_snapshot jsonb;amount_minor bigint;tax_minor bigint;currency char(3);asset_id uuid? FK file_assets |
| Constraints / keys | UNIQUE(number); immutable snapshots; receipt/invoice |
| Indexes | payment_id,document_type |
| Lifecycle / deletion | Keep immutable financial/legal evidence |

## events

| Aspect | Plan |
| --- | --- |
| Columns | id uuid PK;title text;description text;starts_at timestamptz;ends_at timestamptz;timezone text;audience_kind text;audience_roles text[];course_id uuid? FK courses;cohort_id uuid? FK cohorts;status text;version bigint |
| Constraints / keys | Audience kind public/role/course/cohort; public requires empty roles and null course/cohort; role requires nonempty allowed roles and null IDs; course requires course_id only; cohort requires cohort_id only; role filter contains only parent/student/teacher. end>start |
| Indexes | status,starts_at; cohort_id; course_id; audience_kind |
| Lifecycle / deletion | Cancel rather than deleting published occurrence |

## announcements

| Aspect | Plan |
| --- | --- |
| Columns | id uuid PK;title text;body text;audience_kind text;audience_roles text[];course_id uuid? FK courses;cohort_id uuid? FK cohorts;status text;published_at timestamptz?;version bigint |
| Constraints / keys | Audience kind public/role/course/cohort; public requires empty roles and null course/cohort; role requires nonempty allowed roles and null IDs; course requires course_id only; cohort requires cohort_id only; role filter contains only parent/student/teacher. Published body immutable until explicit withdrawal/correction |
| Indexes | status,published_at; cohort_id; course_id; audience_kind |
| Lifecycle / deletion | Withdraw published content with retained audit |

## notifications

| Aspect | Plan |
| --- | --- |
| Columns | id uuid PK;recipient_id uuid FK accounts;source_event_id uuid;kind text;title text;body text;portal_path text;read_at timestamptz?;version bigint |
| Constraints / keys | UNIQUE(recipient_id,source_event_id,kind); allowlisted role-safe portal_path |
| Indexes | recipient_id,created_at DESC; recipient_id,read_at |
| Lifecycle / deletion | Proposed inbox retention12months; essential delivery audit separate |

## notification_deliveries

| Aspect | Plan |
| --- | --- |
| Columns | id uuid PK;notification_id uuid FK notifications;channel text;dedupe_key text;provider_message_id text?;status text;attempt_count integer;next_attempt_at timestamptz?;sent_at timestamptz?;last_error_code text?;version bigint |
| Constraints / keys | UNIQUE(dedupe_key); local retention exceeds provider24h; attempts>=0 |
| Indexes | status,next_attempt_at; notification_id |
| Lifecycle / deletion | Redacted delivery metadata90d; deduplication key safe hash1year |

## file_assets

| Aspect | Plan |
| --- | --- |
| Columns | id uuid PK;owner_id uuid FK accounts;purpose text;context_id uuid;filename text;staging_key text;immutable_key text?;media_type text;size_bytes bigint;checksum_sha256 bytea;status text;scan_result_code text?;version bigint |
| Constraints / keys | UNIQUE(staging_key); UNIQUE(immutable_key) partial; size cap per purpose; ready implies immutable key+clean scan |
| Indexes | owner_id,status; status,created_at; context_id |
| Lifecycle / deletion | Unused quarantine purge24h, rejected7d; linked artifacts follow source retention/holds |

## asset_links

| Aspect | Plan |
| --- | --- |
| Columns | id uuid PK;asset_id uuid FK file_assets;resource_id uuid? FK learning_resources;submission_id uuid? FK submissions;certificate_id uuid? FK certificates;lesson_block_id uuid? FK lesson_blocks;teacher_profile_id uuid? FK teacher_profiles |
| Constraints / keys | CHECK exactly one owner FK; unique asset+owner; reverse references prevent unsafe deletion |
| Indexes | asset_id; each owner FK |
| Lifecycle / deletion | Delete link only as permitted by owning aggregate lifecycle |

## application_settings

| Aspect | Plan |
| --- | --- |
| Columns | key text PK;typed_value jsonb;approved boolean;approval_reference text?;version bigint |
| Constraints / keys | Closed setting schema; secret values forbidden; finance settings separate scope |
| Indexes | key |
| Lifecycle / deletion | Keep versioned change audit; required missing values block affected production capability |

## integration_bindings

| Aspect | Plan |
| --- | --- |
| Columns | id uuid PK;provider text;resource_type text;resource_id uuid;provider_id_ciphertext bytea;desired_version bigint;applied_version bigint;status text;last_error_code text?;version bigint |
| Constraints / keys | UNIQUE(provider,resource_type,resource_id); applied<=desired; resource kind session/event/payment |
| Indexes | provider,status; resource_type,resource_id |
| Lifecycle / deletion | Keep operational references; never persist host URLs; expired bindings archive after related records |

## webhook_inbox

| Aspect | Plan |
| --- | --- |
| Columns | id uuid PK;provider text;provider_event_id text;verified boolean;payload_ciphertext bytea;status text;lease_until timestamptz?;received_at timestamptz;processed_at timestamptz? |
| Constraints / keys | UNIQUE(provider,provider_event_id); process only verified; bounded payload |
| Indexes | status,received_at; lease_until |
| Lifecycle / deletion | Encrypted raw payload30d proposal; durable dedupe ID retained with finance ledger |

## outbox_events

| Aspect | Plan |
| --- | --- |
| Columns | id uuid PK;aggregate_type text;aggregate_id uuid;aggregate_version bigint;event_type text;payload jsonb;occurred_at timestamptz;published_at timestamptz?;lease_until timestamptz? |
| Constraints / keys | UNIQUE(aggregate_type,aggregate_id,aggregate_version,event_type); append in business transaction |
| Indexes | published_at,occurred_at; lease_until |
| Lifecycle / deletion | Published payload90d proposal; dedupe identifiers preserved for replay horizon |

## background_jobs

| Aspect | Plan |
| --- | --- |
| Columns | id uuid PK;kind text;source_event_id uuid? FK outbox_events;dedupe_key text;payload jsonb;status text;attempt_count integer;lease_until timestamptz?;next_attempt_at timestamptz?;last_error_code text?;version bigint |
| Constraints / keys | UNIQUE(kind,dedupe_key); attempts<=8 default; immutable original payload; redacted errors |
| Indexes | status,next_attempt_at; lease_until |
| Lifecycle / deletion | Dead-letter requires explicit review; no automatic deletion of pending work |

## idempotency_records

| Aspect | Plan |
| --- | --- |
| Columns | principal_scope text;operation_id text;key uuid;request_hash bytea;result_ciphertext bytea?;status text;expires_at timestamptz |
| Constraints / keys | PK(principal_scope,operation_id,key); mismatch body409; session not response replayed outside valid principal scope; ADR 0004 enrolment request_hash encodes digest-format and key version with keyed canonical-body digest; result_ciphertext IS NULL; missing digest key fails closed |
| Indexes | expires_at |
| Lifecycle / deletion | 7d general,90d financial; provider reference dedupe permanent ledger |

## audit_records

| Aspect | Plan |
| --- | --- |
| Columns | id uuid PK;actor_id uuid? FK accounts;action text;resource_type text;resource_id uuid?;occurred_at timestamptz;request_id uuid;outcome text;reason text?;metadata jsonb |
| Constraints / keys | Append-only DB grant; redacted metadata schema; no ordinary UPDATE/DELETE |
| Indexes | occurred_at; actor_id,occurred_at; resource_type,resource_id,occurred_at; request_id |
| Lifecycle / deletion | 12months security and7y finance proposals; final retention approval and hold rules apply |

## privacy_requests

| Aspect | Plan |
| --- | --- |
| Columns | id uuid PK;family_id uuid FK families;requester_id uuid FK accounts;student_id uuid? FK students;kind text;status text;verification_reference text?;decision_reason text?;version bigint |
| Constraints / keys | Verified authority before approved; kind access/correction/deletion/closure |
| Indexes | family_id,created_at; status,created_at |
| Lifecycle / deletion | Retain decision evidence while related hold/retention obligations remain |

## retention_holds

| Aspect | Plan |
| --- | --- |
| Columns | id uuid PK;resource_type text;resource_id uuid;held boolean;reason text;approval_reference text;actor_id uuid FK accounts;version bigint |
| Constraints / keys | UNIQUE(resource_type,resource_id); type-specific resource existence validated transactionally |
| Indexes | held,resource_type; resource_id |
| Lifecycle / deletion | Release audited; records under hold never purged |

## privacy_exports

| Aspect | Plan |
| --- | --- |
| Columns | id uuid PK;request_id uuid? FK privacy_requests;requested_by uuid FK accounts;purpose text;asset_id uuid? FK file_assets;status text;expires_at timestamptz?;report_from date?;report_to date?;job_id uuid? FK background_jobs;version bigint;created_at timestamptz;failure_code text? |
| Constraints / keys | Access export requires verified request; finance export requires finance scope; immutable purpose; financial_export purpose requires null privacy request, nonnull report_from/report_to/job_id, range<=366days and finance-authorized requester; ready requires asset |
| Indexes | requested_by,created_at; expires_at |
| Lifecycle / deletion | Export download expires24h, object purged7d unless decision hold |

## retention_decisions

| Aspect | Plan |
| --- | --- |
| Columns | id uuid PK;request_id uuid? FK privacy_requests;policy_version text;resource_type text;resource_id uuid;action text;reason text;approved_by uuid FK accounts;executed_at timestamptz? |
| Constraints / keys | Immutable decision; no purge without approved policy and no active hold |
| Indexes | resource_type,resource_id; executed_at |
| Lifecycle / deletion | Retain minimal execution evidence after source anonymization |

## reconciliation_exceptions

| Aspect | Plan |
| --- | --- |
| Columns | id uuid PK;provider_transaction_id text;amount_minor bigint;currency char(3);provider_status text;payment_id uuid? FK payments;status text;first_seen_at timestamptz;last_checked_at timestamptz;reason_code text;version bigint |
| Constraints / keys | UNIQUE(provider_transaction_id); open/linked/provider_reversed; nonnegative AUD amount; no invented family association |
| Indexes | status,first_seen_at; payment_id |
| Lifecycle / deletion | Retain financial reconciliation evidence with approved financial retention |

## mfa_factors

| Aspect | Plan |
| --- | --- |
| Columns | id uuid PK;account_id uuid FK accounts;secret_ciphertext bytea;encryption_key_version text;status text;last_accepted_step bigint?;activated_at timestamptz?;revoked_at timestamptz?;version bigint |
| Constraints / keys | Partial UNIQUE active factor(account_id); pending/active/revoked; last timestep monotonic under row lock; seed never plaintext |
| Indexes | account_id,status |
| Lifecycle / deletion | Revoke factor on verified compromise; erase encrypted seed on final closure while retaining safe audit |

## mfa_recovery_codes

| Aspect | Plan |
| --- | --- |
| Columns | id uuid PK;factor_id uuid FK mfa_factors;code_hash bytea;consumed_at timestamptz? |
| Constraints / keys | UNIQUE(code_hash); only high entropy random values issued; single-use consume locked |
| Indexes | factor_id,consumed_at |
| Lifecycle / deletion | Consume hash immediately; retain consumed marker without usable secret until factor rotates |

## mfa_challenges

| Aspect | Plan |
| --- | --- |
| Columns | id uuid PK;account_id uuid FK accounts;token_hash bytea;purpose text;browser_binding_hash bytea;expires_at timestamptz;attempts integer;consumed_at timestamptz?;factor_id uuid? FK mfa_factors |
| Constraints / keys | UNIQUE(token_hash); challenge/setup purpose; attempts0–5; expiry5m challenge or10m setup; consumed cannot replay |
| Indexes | account_id,purpose; expires_at |
| Lifecycle / deletion | Destroy credential hash on consumption/expiry; safe metadata30d |


## Migration and rollback plan

Build schema in dependency order: identities/families; file metadata; curriculum; delivery/enrolment; work/progress; billing; communication/integration/operations. Circular publication/revision pointers are added as deferrable foreign keys after both tables exist. The application release must work against the expanded schema before deprecated columns are removed. Use expand/backfill/validate/contract migrations; large indexes are created concurrently where safe. Production migration is a single controlled deploy job, never every web replica startup.

Every migration has forward validation, compatible rollback or documented restore/forward-fix plan, and staging upgrade from previous released schema. Validate row counts, FK integrity, uniqueness and negative scope fixtures after migration. Backfills use bounded batches with restartable checkpoints. Never drop live child/finance history to make a migration pass. Schema downgrade that would lose accepted user data is forbidden; use compatible app rollback and a reviewed forward fix. Backup/restore evidence is required before production-impacting schema changes.

Retention periods above are proposed configurable operational defaults for professional/human approval, not legal claims. Until retention approval exists the purge worker remains disabled and alerts the launch gate. Retention holds override every expiry. Backup retention/version purging must align with the approved matrix and restored data must reapply approved deletion tombstones before production access.

Export lifecycle constraint: privacy_exports.status is requested/processing/ready/failed/expired; terminal failed exposes only GENERATION_FAILED, LIMIT_EXCEEDED or STORAGE_UNAVAILABLE. failure_code is null in every other state. Bounded retry exhaustion persists failure; authorized job retry returns to processing. The created_at column supports requester/time lookup.
