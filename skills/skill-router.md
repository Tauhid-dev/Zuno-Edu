# Automatic skill routing

After fresh master synchronization and deterministic chunk selection, read every `required_skills` path in that manifest. A missing required skill is a blocker; never silently skip it. Read optional skills only if the selected work touches the named boundary, and note why in the handoff. Paths are repository-relative `SKILL.md` entrypoints. Do not preload the whole skills directory.

| Changed boundary | Skill categories/names |
|---|---|
| Route/layout/server rendering | frontend/nextjs, typescript, component-architecture |
| Forms, API queries/cache | frontend/frontend-api-integration, frontend-testing |
| Shared primitives and interaction | frontend/design-system, accessibility |
| Domain entity/policy/value object | backend/oop-domain-modeling, python, backend-testing |
| Public use case/transaction | backend/application-services, repository-pattern |
| HTTP schema/handler | backend/fastapi, api-design, validation |
| Mapping/migration | backend/sqlalchemy-alembic, repository-pattern |
| Login/session/recovery | security/authentication |
| Role or resource access | security/authorization-rbac, resource-ownership, child-family-data-boundaries |
| Upload/download | security/secure-file-handling, integrations/object-storage |
| External payment callback | security/webhook-security, integrations/stripe |
| Provider adapter | matching integrations skill plus security/secrets-and-integrations |
| Runtime/release/operations | matching infrastructure skills |
| Every chunk | workflow/chunk-execution, state-reconciliation, scope-control, review-agent |
| Handoff and state persistence | workflow/git-workflow, memory-maintenance, pr-handoff |
| Independent planning review | workflow/planning-review plus relevant security/domain/frontend skill |

Each abbreviated category/name above resolves to `skills/<category>/<name>/SKILL.md`. Manifests use full paths. Selected skills point to exact architecture context. Use domain/service/API indexes to load only the relevant entries in larger catalogs. Optional skills cannot introduce a new feature or change a locked contract. Reuse an existing rule when possible; add a generic missing rule only with the chunk review.
