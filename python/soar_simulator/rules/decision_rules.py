from typing import Dict, Any


def evaluate_incident(incident: Dict[str, Any]) -> Dict[str, Any]:
    """
    Apply SOAR decision logic to a normalized incident.
    Offline-only, deterministic.
    """

    decisions = {
        "notify": True,
        "tag": False,
        "propose_isolation": False,
        "require_approval": False,
        "reasoning": []
    }

    severity = incident["severity"]

    # Always notify
    decisions["reasoning"].append("Notification enabled for all incidents.")

    # Tagging logic
    if severity in ("Medium", "High"):
        decisions["tag"] = True
        decisions["reasoning"].append(
            f"Severity is {severity}; device tagging enabled for triage."
        )

    # Isolation logic (proposal only)
    if severity == "High":
        decisions["propose_isolation"] = True
        decisions["require_approval"] = True
        decisions["reasoning"].append(
            "High severity incident; isolation may be required but needs approval."
        )

    if severity != "High":
        decisions["reasoning"].append(
            "Severity below High; isolation not considered."
        )

    return decisions
