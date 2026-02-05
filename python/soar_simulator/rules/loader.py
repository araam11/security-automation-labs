from pathlib import Path
from typing import Dict, Any
import yaml


def load_rules() -> Dict[str, Any]:
    rules_path = Path(__file__).parent / "rules.yaml"
    return yaml.safe_load(rules_path.read_text(encoding="utf-8"))
