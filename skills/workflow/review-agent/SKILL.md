---
name: review-agent
description: Independently review a completed Zuno Edu chunk against its locked plan and final diff; not act as its implementer or merge authority.
---

# Focused review

Load AGENT_WORKFLOW.md#Review, active manifest, final diff, targeted contracts and concise test evidence. Medium: focused AI second pass. High/critical: independent deep review by someone who did not author the implementation. Low does not require this skill or a separate AI reviewer.

Check exact scope/acceptance; blueprint and object/service/API/UI mapping; reuse; forbidden adjacent work; no removed/deferred requirement; authorization and resource state at API/service/query layers; failure/concurrency paths and regression evidence. Expand only for a concrete ambiguity or finding.

Record actual risk, depth, reviewer identity/independence, Critical/High/Medium/Low findings and affected retests in the existing hashed review artifact. Resolve Critical/High and practical material Medium. Review the final diff; author claims and green happy paths are not evidence of boundary safety. Human merge remains required.
