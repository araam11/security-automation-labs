from typing import Dict, Any
from rules.loader import load_rules
from rules.engine import evaluate_rules


def simulate_soar(incident: Dict[str, Any]) -> Dict[str, Any]:
    policy = load_rules()
    decisions = evaluate_rules(incident, policy)

    return {
        "incidentId": incident["id"],
        "title": incident["title"],
        "decisions": decisions
    }
