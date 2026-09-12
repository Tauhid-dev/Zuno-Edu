# OOP and domain standards

Entities encapsulate identity and lifecycle transitions; value objects are immutable and compare by value. Aggregate roots guard invariants. Domain policies express authorization-independent business rules; application services enforce actor/resource authorization and orchestrate transactions. Use composition over inheritance. LessonBlock uses a closed discriminated variant set rather than arbitrary class hierarchies. Avoid anemia where setters permit invalid states, but do not invent classes for trivial formatting.

Domain imports no FastAPI, SQLAlchemy, provider SDK or cloud deployment code. ORM rows are mapped to domain objects; repositories represent aggregate boundaries, not one table per noun. Explicit domain failures map through application errors to API contracts. Services must not become god objects: transaction boundaries follow a use case. Test invalid transitions and cross-object invariants directly, then test orchestration using port fakes. Review every durable object against BACKEND_OBJECT_CATALOG and every public method against the service/port catalogs.

Authority: approved scope and architecture precede this standard. Apply only to the selected chunk; verify against its acceptance criteria and record evidence in its handoff.
