# ADR 0002 — Bounded launch business decisions
Status: PROPOSED. See product requirements and DESIGN_INPUTS.md.

Capture declared integer age and age_as_of rather than requiring full date of birth. This satisfies mandatory age capture while minimizing child data. Guardian reconfirms age when the declaration is stale at enrolment; never derive a fictitious exact DOB. Single required given/display name accommodates real naming patterns; family name, preferred name and school remain optional.

Use one-time AUD cohort billing with server-authoritative payments, seat holds and explicit refund/access decisions. Do not introduce subscriptions or discounts. Completion certificate is the launch achievement, not a points system. Parent requests for administrative schedule changes use contact; parents cannot mutate schedule. Teachers may reschedule under explicit notice, assignment and conflict policy. Administration handles exceptions with reason.

No live recording by default, no direct student messaging, no diagnosis collection, no exact child location. Public pages publish explicit sanitized projections. Administrative privileges are separated; teacher principals cannot also carry finance privilege. Human-approved merchant tax settings, child age bands, policies and provider accounts gate production activity without leaving software operations undefined.
