from typing import Dict, Any


def render_response_plan(result: Dict[str, Any]) -> str:
    d = result["decisions"]

    lines = [
        f"# SOAR Response Plan for Incident {result['incidentId']}",
        "",
        f"**Title:** {result['title']}",
        "",
        "## Proposed Actions",
        f"- Notify SOC: {'Yes' if d['notify'] else 'No'}",
        f"- Tag devices for triage: {'Yes' if d['tag'] else 'No'}",
        f"- Propose isolation: {'Yes' if d['propose_isolation'] else 'No'}",
        f"- Approval required: {'Yes' if d['require_approval'] else 'No'}",
        "",
        "## Decision Rationale",
        ""
    ]

    for r in d["reasoning"]:
        lines.append(f"- {r}")

    return "\n".join(lines)
