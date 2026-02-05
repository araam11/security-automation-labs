import json
import sys
from pathlib import Path


def add_tool_paths(repo_root: Path) -> None:
    """
    Make the two offline tools importable without packaging.
    Keeps everything GitHub-only and simple.
    """
    sentinel_tool = repo_root / "python" / "sentinel_incident_tool"
    soar_tool = repo_root / "python" / "soar_simulator"

    sys.path.insert(0, str(sentinel_tool))
    sys.path.insert(0, str(soar_tool))


def main() -> None:
    # Determine repo root based on this file's location
    # .../security-automation-labs/python/offline_pipeline/pipeline.py
    repo_root = Path(__file__).resolve().parents[2]
    add_tool_paths(repo_root)

    # Import from the two tools
    from core.normalizer import normalize_incident  # sentinel_incident_tool/core/normalizer.py
    from core.report_md import render_markdown      # sentinel_incident_tool/core/report_md.py

    from core.simulator import simulate_soar        # soar_simulator/core/simulator.py
    from core.response_md import render_response_plan  # soar_simulator/core/response_md.py

    # Inputs
    raw_incident_path = repo_root / "python" / "sentinel_incident_tool" / "samples" / "incident_sample.json"

    # Outputs
    out_dir = Path(__file__).resolve().parent / "outputs"
    out_dir.mkdir(parents=True, exist_ok=True)

    incident_report_path = out_dir / "incident_report.md"
    normalized_path = out_dir / "normalized_incident.json"
    response_plan_path = out_dir / "response_plan.md"
    decision_trace_path = out_dir / "decision_trace.json"

    # Run normalizer (raw -> normalized -> incident report)
    raw = json.loads(raw_incident_path.read_text(encoding="utf-8"))
    normalized = normalize_incident(raw)

    incident_report_md = render_markdown(normalized)
    incident_report_path.write_text(incident_report_md, encoding="utf-8")
    normalized_path.write_text(json.dumps(normalized, indent=2), encoding="utf-8")

    # Run SOAR simulator (normalized -> decisions -> response plan + trace)
    simulation_result = simulate_soar(normalized)

    response_md = render_response_plan(simulation_result)
    response_plan_path.write_text(response_md, encoding="utf-8")
    decision_trace_path.write_text(json.dumps(simulation_result, indent=2), encoding="utf-8")

    print("Offline pipeline complete.")
    print(f"- Incident report: {incident_report_path}")
    print(f"- Normalized JSON: {normalized_path}")
    print(f"- Response plan:   {response_plan_path}")
    print(f"- Decision trace:  {decision_trace_path}")


if __name__ == "__main__":
    main()
