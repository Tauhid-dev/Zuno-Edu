# ADR 0001 — Complete launch baseline and implementation freeze
Status: PROPOSED until human planning PR merge. Scope 1.0, architecture 1.

The source request defines five surfaces sharing one backend. Adopt a modular monolith, explicit OO domain/application interfaces, immutable course publication revisions and cohort-pinned curriculum. The alternative of separate role systems would duplicate data/rules; microservices add distribution without a launch need. The bootstrap creates no business code. Future implementation must follow the reviewed catalogs; material changes require the explicit scope/architecture conflict process.

Use feature-oriented bounded modules inside each backend layer to keep ownership visible; frontend follows route → feature → domain component → shared UI. Package contracts contain generated API types, not another manually written business schema. Repository skills use category/name/SKILL.md folders (rather than flat category/name.md) so each is a valid reusable Codex skill. The router names exact entrypoints. Machine-readable catalogs support deterministic coverage checks and generate parallel human-readable indexes.

Remote master and verified merge evidence outrank progress caches. Local staging while repository identity is missing is not a substitute for required fetch/master/fast-forward. No branch/base/PR may be fabricated. Scope is DRAFT during planning and becomes effectively LOCKED when the identified planning PR is human-merged; next feature branch persists the transition, never editing master during reconciliation.
