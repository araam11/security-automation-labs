from typing import Dict, Any, List


def normalize_incident(raw: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normalize a Sentinel-style incident into a clean internal model.
    No Azure or Sentinel dependencies.
    """

    alerts = sorted(
        raw.get("alerts", []),
        key=lambda a: a.get("eventTime", "")
    )

    timeline: List[Dict[str, Any]] = []
    for alert in alerts:
        timeline.append({
            "time": alert["eventTime"],
            "source": alert["product"],
            "severity": alert["severity"],
            "entities": alert["entities"]
        })

    return {
        "id": raw["incidentId"],
        "title": raw["title"],
        "severity": raw["severity"],
        "status": raw["status"],
        "created": raw["createdTimeUtc"],
        "alertCount": len(alerts),
        "timeline": timeline
    }
