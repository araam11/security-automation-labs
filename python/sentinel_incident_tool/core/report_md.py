from typing import Dict, Any


def render_markdown(incident: Dict[str, Any]) -> str:
    lines = [
        f"# Incident Report: {incident['title']}",
        "",
        f"- **Incident ID:** {incident['id']}",
        f"- **Severity:** {incident['severity']}",
        f"- **Status:** {incident['status']}",
        f"- **Created:** {incident['created']}",
        f"- **Alert Count:** {incident['alertCount']}",
        "",
        "## Timeline",
        ""
    ]

    for item in incident["timeline"]:
        lines.append(
            f"- `{item['time']}` | **{item['source']}** "
            f"({item['severity']}) → {', '.join(item['entities'])}"
        )

    return "\n".join(lines)
