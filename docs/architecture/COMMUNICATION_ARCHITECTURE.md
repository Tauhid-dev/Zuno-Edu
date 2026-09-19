# Communication architecture

NotificationService records an in-app Notification and per-recipient delivery intent; EmailProvider uses Resend in the worker. In-app messages target explicitly materialized authorized audiences (family, enrolled student, assigned teacher or admin privilege); an audience change is rechecked when reading or sending. No global teacher mailing list receives family data. Parents are the email recipients for child learning notices; student credentials need no email address.

| Trigger | Recipient | Email | In-app | Idempotency identity |
|---|---|---|---|---|
| Account registration/verify/reset/security change | account's verified address, guardian for child recovery | required | where authenticated | account + event + token generation |
| Paid enrolment confirmed | linked guardian | required | parent/student | enrolment + activation version |
| Payment/refund/document available | purchasing family | required | parent | payment/refund + status version |
| Class 24h and 1h reminder | guardian, assigned teacher | preference-aware | parent/student/teacher | session + schedule version + reminder offset |
| Schedule update/cancellation | affected guardians and teachers | required operational | affected roles | session + version |
| Assignment published/due reminder | guardian | learning preference | student/parent | assignment + enrolment + release version |
| Result/feedback released | guardian | learning preference | student/parent | release + version |
| Completion/certificate issued/revoked | guardian | required | student/parent | certificate + status version |
| Published announcement/event | authorized audience | opted-in category | authorized roles | announcement + recipient + version |
| Integration failure/action | permitted operations staff | required | admin/assigned teacher when relevant | incident + escalation level |

Outbox insert shares transaction with business change. Delivery ledger has unique event/recipient/channel/version; worker checks eligibility, suppression/category preferences and current state. Required security/financial/essential operational notices are not disabled by marketing preferences. No marketing system is planned. Emails contain minimal information and portal links, never marks, uploaded child work, passwords, host URLs or private attachment URLs.

Templates are versioned, escaped and accessible; sender/reply-to configured from verified domain. Store provider ID and attempt outcome. Retry transient failures; hard bounce/complaint suppresses nonessential email and flags guardian contact correction. Process signed provider delivery events if enabled; otherwise delivery status is accepted/failed, never falsely claims read/delivered. Provider acceptance ambiguity after timeout is resolved within provider idempotency window. Resend deduplicates for 24h; beyond that, unknown send outcome requires operator review rather than an automatic duplicate. [Resend idempotency](https://resend.com/docs/dashboard/emails/idempotency-keys).

Tests: rollback emits no notification, replay emits one, late assignment release doesn't notify unrelated learners, revoked guardian never receives new content, schedule-version replacement, bounce and preferences, provider timeout, safe HTML and unsubscribe category behavior.
