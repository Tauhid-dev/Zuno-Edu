# Backend standards

Use typed Python, FastAPI transport schemas, explicit constructor-injected use cases and an application composition root. Routers authenticate, validate, invoke one use case and map responses/errors; they do not query ORM sessions or call providers. SQLAlchemy data mappers implement repository protocols; Alembic owns migrations. Background handlers reuse application operations, actor/system context and audit rules.

Use UTC aware datetimes and Clock injection for time-sensitive policy tests. Money is integer cents with AUD currency; no floats. Bounded pagination and explicit query filters avoid data overfetch. Versioned optimistic writes or row locks address competing state changes. Async/cancellation boundaries must not leave untracked remote side effects. Structured errors expose safe codes, not stack traces. Verify domain, service, real PostgreSQL repository and API integration layers as relevant.

Authority: approved scope and architecture precede this standard. Apply only to the selected chunk; verify against its acceptance criteria and record evidence in its handoff.
