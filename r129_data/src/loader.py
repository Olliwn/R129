"""Load and validate all YAML data files."""

from pathlib import Path
from typing import Any

import yaml
from rich.console import Console

console = Console()

DATA_DIR = Path(__file__).parent.parent / "data"


def load_yaml(filepath: Path) -> dict | list | None:
    """Load a single YAML file, return parsed content or None on error."""
    if not filepath.exists():
        return None
    try:
        with open(filepath) as f:
            return yaml.safe_load(f)
    except yaml.YAMLError as e:
        console.print(f"[red]YAML error in {filepath}: {e}[/red]")
        return None


def load_all_data() -> dict[str, Any]:
    """Load all YAML data files into a dict keyed by filename stem."""
    data = {}
    if not DATA_DIR.exists():
        return data

    for yaml_file in sorted(DATA_DIR.glob("*.yaml")):
        content = load_yaml(yaml_file)
        if content is not None:
            data[yaml_file.stem] = content

    return data


def load_vehicle() -> dict:
    """Load vehicle identity."""
    return load_yaml(DATA_DIR / "vehicle.yaml") or {}


def load_doc_index() -> list[dict]:
    """Load all doc_index metadata files."""
    doc_index_dir = Path(__file__).parent.parent / "references" / "doc_index"
    docs = []
    if doc_index_dir.exists():
        for yaml_file in sorted(doc_index_dir.glob("*.yaml")):
            content = load_yaml(yaml_file)
            if content:
                docs.append(content)
    return docs


def check_applies_to(applies_to: dict | None, vehicle: dict) -> bool:
    """Check if an applies_to block matches the current vehicle."""
    if applies_to is None:
        return True

    chassis = applies_to.get("chassis", "all")
    if chassis != "all":
        vehicle_chassis = vehicle.get("chassis_code", "")
        if isinstance(chassis, list):
            if vehicle_chassis and vehicle_chassis not in chassis:
                return False
        elif isinstance(chassis, str) and vehicle_chassis:
            if chassis != vehicle_chassis:
                return False

    years = applies_to.get("years")
    if years and len(years) == 2:
        vehicle_year = vehicle.get("model_year", 0)
        if vehicle_year and not (years[0] <= vehicle_year <= years[1]):
            return False

    return True


def validate_all() -> list[str]:
    """Validate all YAML files and return a list of issues."""
    issues = []
    data = load_all_data()

    if not data:
        issues.append("No YAML data files found in data/")
        return issues

    if "vehicle" not in data:
        issues.append("Missing vehicle.yaml")

    for name in ["fuse_box", "relay_box", "fluids", "torques", "known_issues", "service_intervals"]:
        filepath = DATA_DIR / f"{name}.yaml"
        if not filepath.exists():
            issues.append(f"Missing {name}.yaml")
            continue
        content = data.get(name)
        if content is None:
            issues.append(f"{name}.yaml is empty or invalid")
            continue

        items_key = None
        for key in content:
            if isinstance(content[key], list):
                items_key = key
                break

        if items_key:
            items = content[items_key]
            for i, item in enumerate(items):
                if isinstance(item, dict):
                    if "source" not in item:
                        issues.append(f"{name}.yaml[{i}]: missing 'source' field")
                    source = item.get("source", {})
                    if isinstance(source, dict) and source.get("confidence") == "low":
                        issues.append(f"{name}.yaml[{i}] ({item.get('id', '?')}): low confidence -- needs verification")

                    for field, value in item.items():
                        if value == "TBD" or value == "TODO":
                            issues.append(f"{name}.yaml[{i}] ({item.get('id', '?')}): field '{field}' is TBD")

    return issues
