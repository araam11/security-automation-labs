from typing import Dict, Any
from rules.decision_rules import evaluate_incident


def simulate_soar(incident: Dict[str, Any]) -> Dict[str, Any]:
    decisions = evaluate_incident(incident)

    return {
        "incidentId": incident["id"],
        "title": incident["title"],
        "decisions": decisions
    }
