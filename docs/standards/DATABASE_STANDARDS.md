# Database standards

PostgreSQL is source of truth. UUID keys, timestamptz audit fields, explicit foreign keys, check/unique constraints and indexes support invariants. SQLAlchemy maps domain objects; models do not become active-record business entities. Use family/assignment-aware scoped repository methods. Reference both student and cohort consistently so joins cannot authorize an unrelated submission by checking only one ID.

Use transactional row locks for scarce seat allocation and refund totals; version columns for competing edits. Commit outbox with business data. Migrations are forward-versioned with upgrade and rollback/compatibility tests against PostgreSQL, not SQLite. Expand-contract changes preserve previous release compatibility. Do not cascade-delete issued financial/assessment records. Deletion uses governed tombstones/anonymization; legal hold overrides purge. Explain query plans for family/student/teacher list paths and bound all list queries.

Authority: approved scope and architecture precede this standard. Apply only to the selected chunk; verify against its acceptance criteria and record evidence in its handoff.
