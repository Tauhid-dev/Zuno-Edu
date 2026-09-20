#!/usr/bin/env python3
"""Compact routing over the existing plan; previews/context reads never authorize work."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys

from reconcile_state import Blocked, Repository, reconcile, require, safe_path, validate_plan

ROOT = Path(__file__).resolve().parents[1]
RANK = {"low": 0, "medium": 1, "high": 2, "critical": 3}
CATALOGS = {
    "operation": ("backend-catalog.json", "operations", "id", "api_operations"),
    "object": ("backend-catalog.json", "objects", "name", "domain_objects"),
    "service": ("backend-catalog.json", "services", "name", "application_services"),
    "port": ("backend-catalog.json", "ports", "name", "ports"),
    "schema": ("backend-catalog.json", "schemas", "name", None),
    "component": ("frontend-catalog.json", "components", "name", "frontend_components"),
}


def read(root, path):
    return json.loads((root / path).read_text())


def load(root):
    chunks = validate_plan(read(root, "docs/planning/chunks.json"))
    router = read(root, "docs/planning/workflow-routing.json")
    require(router.get("schema_version") == 1, "Unsupported workflow router")
    return chunks, router


def resolve(root, chunk, router, raised_risk=None):
    meta = chunk["workflow"]
    risk = meta["review_risk"]
    if raised_risk:
        require(RANK[raised_risk] >= RANK[risk], "Risk cannot be downgraded")
        risk = raised_risk
    policy = router["risk"][risk]
    profile = router["profiles"][meta["route"]]
    technical = [p for p in chunk["required_skills"] if not p.startswith("skills/workflow/")]
    phases = {
        "execution": [router["instructions"] + "#Execution", *profile["instructions"],
                      "skills/workflow/chunk-execution/SKILL.md", *technical],
        "validation": [router["instructions"] + "#Validation"],
        "review": [router["instructions"] + "#Review"],
        "handoff": [router["instructions"] + "#Handoff", "docs/planning/STATE_RECONCILIATION.md#Implementation completion evidence",
                    "skills/workflow/pr-handoff/SKILL.md", "skills/workflow/memory-maintenance/SKILL.md",
                    "skills/workflow/git-workflow/SKILL.md"],
    }
    if risk != "low":
        phases["review"].append("skills/workflow/review-agent/SKILL.md")
    checks = list(dict.fromkeys(command.replace("{chunk_id}", chunk["id"])
                 for name in ["metadata", *profile["validation"], *meta.get("extra_validation", [])]
                 for command in router["validation"][name]))
    frontend = read(root, "docs/architecture/frontend-catalog.json")
    model = profile.get("model", policy) if risk == "medium" else policy
    return {"chunk": chunk["id"], "manifest": f"docs/planning/chunks/{chunk['id']}.md",
            "instructions_by_phase": phases,
            "context_budget_tokens": max(meta["context_budget_tokens"], policy["context_budget_tokens"]),
            "context_reader": f"python3 scripts/next_chunk.py --context {chunk['id']} --item <kind:identifier>",
            "context_index": {"files": chunk["required_context"], "requirements": chunk["requirements"],
                "route": [r["path"] for r in frontend["routes"] if r["component"] in chunk["frontend_components"]],
                "mapping": [c for c in chunk["frontend_components"] if any(m["component"] == c for m in frontend["mappings"])],
                **{kind: chunk[field] for kind, (_, _, _, field) in CATALOGS.items() if field}},
            "source_start": chunk["affected_areas"], "expected_files": chunk["expected_files"],
            "validation_commands": checks, "validation_parameters": router["validation_parameters"],
            "required_tests": chunk["required_tests"],
            "review": {"risk": risk, "depth": policy["depth"], "independent": policy["independent"]},
            "model": {k: model[k] for k in ("model", "reasoning", "why")}}


def section(text, heading):
    if not heading:
        return text
    lines = text.splitlines(keepends=True)
    starts = [i for i, line in enumerate(lines) if re.fullmatch(r"#{1,6} " + re.escape(heading) + r"\s*", line)]
    require(len(starts) == 1, "Context heading missing or ambiguous: " + heading)
    start = starts[0]
    level = len(lines[start]) - len(lines[start].lstrip("#"))
    end = next((i for i in range(start + 1, len(lines)) if re.match(r"#{1," + str(level) + r"} ", lines[i])), len(lines))
    return "".join(lines[start:end])


def context(root, chunk, router, item, reason=None):
    require(not reason or reason in router["expansion_reasons"], "Unknown context expansion reason")
    kind, separator, key = item.partition(":")
    require(separator and key, "Use kind:identifier or file:path#Heading")
    packet = resolve(root, chunk, router)
    if kind == "file":
        path, _, heading = key.partition("#")
        safe_path(path)
        target = (root / path).resolve()
        require(target.is_relative_to(root.resolve()), "Context path escapes repository")
        allowed = set(chunk["required_context"] + chunk["required_skills"] + chunk["optional_skills"])
        allowed.update(ref.split("#")[0] for refs in packet["instructions_by_phase"].values() for ref in refs)
        require(path in allowed or reason, "Unrouted context requires an expansion reason")
        require(not path.startswith("memory/handoffs/") or reason == "regression_audit",
                "Historical handoff requires regression_audit")
        # Catalog files are indexes, not permission to dump the entire product.
        require(not Path(path).name.endswith("catalog.json") and not Path(path).name.endswith("CATALOG.md")
                and Path(path).name not in {"FRONTEND_BACKEND_MAPPING.md", "FRONTEND_ROUTE_MAP.md"},
                "Use a named catalog entry rather than loading a whole catalog")
        text = target.read_text()
        if path.endswith("CODE_BLUEPRINT.md"):
            text = "\n".join(line for line in text.splitlines() if line.startswith("| " + chunk["id"] + " |"))
        else:
            text = section(text, heading)
        value = text
    elif kind in {"route", "mapping", "presentation_type"}:
        catalog = read(root, "docs/architecture/frontend-catalog.json")
        components = set(chunk["frontend_components"])
        if kind == "route":
            matches = [r for r in catalog["routes"] if r["path"] == key]
            require(len(matches) == 1, "Unknown frontend route")
            require(matches[0]["component"] in components or reason, "Route outside this chunk")
            value = matches[0]
        elif kind == "mapping":
            # A component is the bounded mapping unit; no unrelated page rows.
            require(key in components or reason, "Mapping outside this chunk")
            value = [m for m in catalog["mappings"] if m["component"] == key]
            require(value, "Unknown component mapping")
        else:
            require(key in catalog["presentation_types"], "Unknown presentation type")
            selected = [c for c in catalog["components"] if c["name"] in components]
            require(any(key in json.dumps(c) for c in selected) or reason, "Presentation type outside this chunk")
            value = {key: catalog["presentation_types"][key]}
    elif kind == "requirement":
        require(key in chunk["requirements"] or reason, "Requirement is outside the current chunk")
        matches = [r for r in read(root, "docs/product/requirements.json") if r["id"] == key]
        require(len(matches) == 1, "Unknown requirement")
        value = matches[0]
    else:
        require(kind in CATALOGS, "Unknown context kind")
        filename, group, field, scope = CATALOGS[kind]
        catalog = read(root, "docs/architecture/" + filename)
        if kind == "schema":
            # Schema references can nest; only names occurring in a selected API's
            # transitive request/response closure are routable without expansion.
            schemas = {s["name"]: s for s in catalog["schemas"]}
            allowed = {a[k] for a in catalog["operations"] if a["id"] in chunk["api_operations"] for k in ("request", "response")}
            pending = list(allowed)
            while pending:
                name = pending.pop()
                for f in schemas[name]["fields"]:
                    for token in re.findall(r"[A-Za-z_][A-Za-z0-9_]*", f["type"]):
                        if token in schemas and token not in allowed:
                            allowed.add(token); pending.append(token)
        else:
            allowed = set(chunk[scope])
            if kind == "service":
                allowed = {name.split(".")[0] for name in allowed}
        require(key in allowed or reason, "Catalog entry outside this chunk; supply a concrete expansion reason")
        matches = [entry for entry in catalog[group] if entry[field] == key]
        require(len(matches) == 1, "Unknown catalog entry")
        value = dict(matches[0])
        if kind == "service" and not reason:
            value["methods"] = [m for m in value["methods"] if key + "." + m["name"] in chunk["application_services"]]
        if kind == "component":
            # API contracts already own these repeated projections.
            for repeated in ("authorization", "server_state"):
                value.pop(repeated, None)
    rendered = value if isinstance(value, str) else json.dumps(value, indent=2)
    estimated = (len(rendered.encode()) + 3) // 4
    limit = min(4000, packet["context_budget_tokens"])
    require(estimated <= limit or reason, f"Context needs approximately {estimated} tokens; narrow the reference or state --reason")
    return {"reference": item, "estimated_tokens": estimated, "expansion_reason": reason,
            "budget_note": "Count cumulatively with prior reads; an expansion never authorizes scope changes", "content": value}


def forecast(chunks, current, completed):
    """Conditional recommendation, explicitly not a verified selection."""
    known = {c["id"] for c in chunks}
    require(current in known and set(completed) <= known, "Invalid forecast cache/chunk")
    assumed = set(completed) | {current}
    return next((c for c in chunks if c["id"] not in assumed and c["status"] in {"PLANNED", "READY"}
                 and not c.get("blockers") and set(c["dependencies"]) <= assumed), None)


def validate_workflow(root):
    chunks, router = load(root)
    for c in chunks:
        require(c.get("workflow", {}).get("route") in router["profiles"], "Missing workflow route " + c["id"])
        risk = c["workflow"].get("review_risk")
        require(risk in RANK, "Unknown review risk")
        budget = c["workflow"].get("context_budget_tokens")
        require(type(budget) is int and 1000 <= budget <= 30000, "Invalid context budget")
        packet = resolve(root, c, router)
        for refs in packet["instructions_by_phase"].values():
            for ref in refs:
                path, _, heading = ref.partition("#")
                require((root / safe_path(path)).is_file(), "Missing route reference " + ref)
                if heading: section((root / path).read_text(), heading)
        require(packet["validation_commands"] and c["required_tests"], "Missing deterministic checks")
        policy = router["risk"][risk]
        if RANK[risk] >= RANK["high"]:
            require(policy["depth"] == "deep" and policy["independent"] is True, "Sensitive work cannot weaken review")
    state = read(root, "memory/progress.json")
    known = {c["id"] for c in chunks}
    for field in ("active_chunk", "last_completed_chunk", "next_candidate_chunk"):
        require(state.get(field) is None or state[field] in known, "Unknown state chunk: " + field)
    require(set(state.get("completed_chunks", [])) <= known, "Unknown cached completion")
    handoff = (root / router["current_handoff"]).read_text()
    require(len(handoff.split()) <= 250, "Current handoff exceeds 250 words; move details to referenced evidence")
    for field in ("CHUNK", "STATUS", "COMMIT", "PR", "CHANGE", "VALIDATION", "BLOCKERS", "NEXT", "NEXT_MODEL", "REASONING", "WHY", "LOAD"):
        require(len(re.findall(r"^" + field + r":", handoff, re.M)) == 1, "Missing/duplicate handoff field " + field)
    return {"validation": "PASS", "routed_chunks": len(chunks), "handoff_words": len(handoff.split())}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument("--preview", metavar="CHUNK")
    modes.add_argument("--context", metavar="CHUNK")
    modes.add_argument("--recommend-after", metavar="CHUNK")
    modes.add_argument("--validate", action="store_true")
    parser.add_argument("--item")
    parser.add_argument("--reason")
    parser.add_argument("--risk", choices=RANK, help="Raise actual-change risk; never lower the manifest floor")
    args = parser.parse_args()
    try:
        if args.validate:
            result = validate_workflow(ROOT)
        else:
            chunks, router = load(ROOT)
            byid = {c["id"]: c for c in chunks}
            if args.context:
                result = context(ROOT, byid[args.context], router, args.item or "", args.reason)
            elif args.preview:
                result = {"execution_authorized": False, "status": "PREVIEW", **resolve(ROOT, byid[args.preview], router, args.risk)}
            elif args.recommend_after:
                c = forecast(chunks, args.recommend_after, read(ROOT, "memory/progress.json").get("completed_chunks", []))
                result = {"execution_authorized": False, "status": "CONDITIONAL_AFTER_MERGE", "candidate": c["id"] if c else None,
                          "warning": "Forecast only; fresh remote reconciliation chooses the real next chunk",
                          "next": resolve(ROOT, c, router) if c else None}
            else:
                evidence = reconcile(Repository(ROOT))
                cid = evidence["next_candidate_chunk"]
                allowed = evidence["scope_status"] == "LOCKED" and cid is not None
                result = {"execution_authorized": allowed, "status": "READY" if allowed else "BLOCKED",
                          "master_sha": evidence["master_sha"], "scope_status": evidence["scope_status"],
                          "blocker": evidence["scope_blocker"], "warnings": evidence["warnings"],
                          "confirmed_merged": evidence["completed_chunks"], "blocked": evidence["blocked_chunks"],
                          "routing": resolve(ROOT, byid[cid], router, args.risk) if allowed else None}
        print(json.dumps(result, indent=2))
        return 0
    except (Blocked, OSError, KeyError, TypeError, ValueError) as exc:
        print(json.dumps({"status": "BLOCKED", "execution_authorized": False, "reason": str(exc)}))
        return 2


if __name__ == "__main__":
    sys.exit(main())
