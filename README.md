# Zuno Edu

Complete launch-product blueprint for an Australian instructor-led AI education business. **Planning only: no application features have been implemented.**

Start with [launch scope](docs/product/LAUNCH_SCOPE.md), [scope lock](docs/product/SCOPE_LOCK.md), [Code Blueprint](docs/architecture/CODE_BLUEPRINT.md) and [master plan](docs/planning/MASTER_PLAN.md). Review [planning findings](docs/planning/INDEPENDENT_REVIEW.md) and [bootstrap verification](docs/planning/BOOTSTRAP_VALIDATION.md).

Future sessions receiving `next chunk` must follow [AGENTS.md](AGENTS.md): identify the expected remote, synchronize master, reconcile verified merged evidence read-only, select exactly one eligible chunk and create a fresh feature branch. Human review and merge are required; no automatic implementation starts from this draft.

`python3 scripts/validate_plan.py` checks planning coverage, contract mappings, dependencies and references. Add `--bootstrap` to prove the initial application folders contain only documentation; ordinary future validation permits implemented code. `python3 -m unittest discover -s tests/workflow -v` exercises reconciliation safeguards. These are bootstrap-tooling checks, not product test results.

Repository identity and synchronization status are in `memory/repository.json` and `memory/PROJECT_STATE.md`.
