import json
from pathlib import Path

from core.normalizer import normalize_incident
from core.report_md import render_markdown


def main():
    sample_path = Path("samples/incident_sample.json")
    output_path = Path("outputs/incident_report.md")

    raw = json.loads(sample_path.read_text())
    normalized = normalize_incident(raw)

    md = render_markdown(normalized)
    output_path.write_text(md)

    print(f"Report written to {output_path}")


if __name__ == "__main__":
    main()
