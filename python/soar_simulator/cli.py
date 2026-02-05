import json
from pathlib import Path

from core.simulator import simulate_soar
from core.response_md import render_response_plan


def main():
    input_path = Path("samples/normalized_incident.json")
    output_md = Path("outputs/response_plan.md")
    output_trace = Path("outputs/decision_trace.json")

    incident = json.loads(input_path.read_text())
    result = simulate_soar(incident)

    output_md.write_text(render_response_plan(result))
    output_trace.write_text(json.dumps(result, indent=2))

    print("SOAR simulation complete.")
    print(f"- Response plan: {output_md}")
    print(f"- Decision trace: {output_trace}")


if __name__ == "__main__":
    main()
