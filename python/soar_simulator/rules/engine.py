from typing import Dict, Any, List


def matches(condition: Dict[str, Any], incident: Dict[str, Any]) -> bool:
    for key, expected in condition.items():
        actual = incident.get(key)

        if isinstance(expected, list):
            if actual not in expected:
                return False
        else:
            if actual != expected:
                return False

    return True


def evaluate_rules(incident: Dict[str, Any], policy: Dict[str, Any]) -> Dict[str, Any]:
    decisions = policy["defaults"].copy()
    rationale: List[str] = []

    for rule in policy.get("rules", []):
        if matches(rule.get("if", {}), incident):
            decisions.update(rule.get("then", {}))
            rationale.append(rule.get("rationale", rule["name"]))

    decisions["reasoning"] = rationale
    return decisions
