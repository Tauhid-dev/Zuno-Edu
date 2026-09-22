# Persistence foundation (ZE-P01-C02)

PostgreSQL is authoritative. `Database` composes a transaction-scoped data mapper;
construction and API startup never create tables. Use `with db.unit_of_work() as tx`,
make aggregate writes through repositories sharing that transaction, then explicitly
`tx.commit(events, audit)`. An exception, failed commit, or exit without commit rolls
back everything. Audit batches require an explicitly composed writer using the same
SQLAlchemy session and fail closed when that writer is absent. The audit aggregate,
account references and grants arrive in their owning chunk; no audit route is enabled.

`VersionConflict` is the shared conflict signal for future transport mapping to 409.
IDs are opaque UUIDs; versions are positive integers; Clock uses aware UTC instants
and IANA zones (the pinned tzdata package also supplies zones on Windows).

## Durable work

Only trusted worker composition calls `OperationsService.dispatch_outbox`. The API
has no worker route. A worker identity is constructed in the bootstrap factory and
checked by object identity, so a role string in request data cannot grant authority.
Batch sizes are limited to 1–100. The returned JobView names a persisted dispatch
summary and never includes payloads or provider errors.

Dispatch claims outbox rows using `FOR UPDATE SKIP LOCKED`, then atomically creates
one unique job per event kind/aggregate/version and marks that event published.
Redis receives only a wakeup UUID **after commit**. An expired outbox lease is
reclaimable. Crashing after job creation or losing Redis cannot erase the job.

`DurableWorker.recover()` is a bounded PostgreSQL sweep independent of Redis. Run it
on each worker polling cycle, using `RedisWakeup.wait()` only to reduce latency.
Each concrete handler is explicitly registered for its allowed event kind; unrelated
jobs cannot be claimed. Provider chunks must implement `reconcile(event)`: reload
latest desired aggregate state, deduplicate using the event's aggregate/version,
and reconcile ambiguous provider outcomes before repeating an effect. There are no
production provider handlers in this foundation. Claims do not promise exactly-once
external calls; durable identity plus provider-specific reconciliation protects effects.

No database transaction remains open during handler/provider calls. Lease tokens and
versions fence stale acknowledgements. Leases last at most 15 minutes (worker default:
2 minutes); handlers must finish within their lease or leave reconciliation to recovery.
Retry delays are 1m, 5m, 15m, 1h, then 6h with 20% jitter and Retry-After as a floor;
eight attempts or 24 hours dead-letters the job. Configuration/ambiguous errors are
quarantined immediately. Safe-code logs alert after five failures. Manual retries,
operational views, provider binding and closed application settings belong to their
owning feature chunks. No pending work is automatically deleted.

Webhook adapters must verify signatures and encrypt bounded payloads **before**
constructing `VerifiedWebhook`. The unique provider/event constraint preserves the
original record on replay. Only verified records can be leased; lease tokens fence
completion, including safely ignored signed events. This chunk adds no public webhook.

## Migrations and rollback

Set `ZUNO_DATABASE_URL` explicitly to a PostgreSQL+psycopg URL, then run
`uv run alembic upgrade head` as a single controlled migration job. Revision `0001`
creates outbox, inbox and jobs with named constraints, indexes, immutable payload
triggers and lease fencing. It imports no mutable application metadata. It is an
additive expansion compatible with the previous health-only application release.

Rollback the **application**, leaving these tables and durable work intact. SQL
downgrade intentionally fails rather than drop accepted work. If a migration defect
occurs, preserve a backup, review a forward-fix migration and test it on a restored
copy; never delete live work to make a migration pass. Production rollout still
requires the later deployment gates and backup/restore evidence.

## Isolated PostgreSQL/Redis verification

The following PowerShell commands are also valid with the absolute Docker CLI path
on Windows/WSL-backed Docker Desktop. Use dedicated disposable containers only:

```powershell
docker run -d --name zuno-c02-postgres -e POSTGRES_USER=zuno_test -e POSTGRES_PASSWORD=zuno_disposable_test -e POSTGRES_DB=zuno_c02_test -p 127.0.0.1:55432:5432 postgres:16
docker run -d --name zuno-c02-redis-test -p 127.0.0.1:16379:6379 redis:7-alpine
$env:ZUNO_TEST_DATABASE_URL='postgresql+psycopg://zuno_test:zuno_disposable_test@127.0.0.1:55432/zuno_c02_test'
$env:ZUNO_TEST_REDIS_URL='redis://127.0.0.1:16379/15'
uv sync --locked
uv run pytest tests/chunks/ZE-P01-C02
```

On macOS/Linux use `export NAME=value` instead of `$env:NAME='value'`. Tests require
the explicitly named localhost database, create/migrate a unique test database for
each test and remove only that database afterwards. The Redis loss test flushes only
database 15 on the fixed isolated localhost test endpoint. Missing services fail the
suite rather than silently skip acceptance. Stop/remove these dedicated containers
after testing. Credentials above are disposable test values, never deployment secrets.
