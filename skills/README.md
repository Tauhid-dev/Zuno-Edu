# Repository skills

Skills are reusable operational instructions. Each entry lives at `skills/<category>/<name>/SKILL.md` with a named trigger. This valid skill-folder layout refines the request's illustrative flat `.md` paths; ADR 0001 records the decision. They are repository-local and loaded by AGENTS.md/manifest routing, not installed globally by bootstrap.

Read [skill-router.md](skill-router.md) and only the selected manifest's required skills. Optional skills load only for objectively relevant changed boundaries. A skill cannot override approved scope, architecture or the current user's explicit instructions. Skill improvements may accompany a chunk when generic, necessary and reviewed; no temporary notes or duplicate skills.
