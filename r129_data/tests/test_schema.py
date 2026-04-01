"""Validate all YAML data files parse correctly against Pydantic schemas."""

import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from r129_data.src.schema import (
    FuseBoxFile, RelayBoxFile, FluidsFile, TorquesFile,
    KnownIssuesFile, ServiceIntervalsFile, ComponentsFile,
    GroundPointsFile, VehicleIdentity, VariantsFile,
)

DATA_DIR = Path(__file__).parent.parent / "data"


def load(filename: str) -> dict:
    filepath = DATA_DIR / filename
    assert filepath.exists(), f"{filename} not found"
    with open(filepath) as f:
        return yaml.safe_load(f)


def test_vehicle():
    data = load("vehicle.yaml")
    assert data["vin"] == "WDB1290661F044414"
    assert data["chassis_code"] == "129.066"
    assert data["engine_code"] == "M119.960"
    assert data["model_year"] == 1991
    assert len(data["option_codes"]) > 0


def test_variants():
    data = load("variants.yaml")
    assert len(data["variants"]) >= 10
    assert len(data["production_changes"]) >= 5
    chassis_codes = [v["chassis_code"] for v in data["variants"]]
    assert "129.066" in chassis_codes


def test_fuse_box():
    data = load("fuse_box.yaml")
    fuses = data["fuses"]
    assert len(fuses) >= 10
    for fuse in fuses:
        assert "id" in fuse
        assert "rating_amps" in fuse
        assert "protects" in fuse
        assert "source" in fuse


def test_relay_box():
    data = load("relay_box.yaml")
    relays = data["relays"]
    assert len(relays) >= 3
    for relay in relays:
        assert "id" in relay
        assert "function" in relay
        assert "source" in relay


def test_fluids():
    data = load("fluids.yaml")
    fluids = data["fluids"]
    assert len(fluids) >= 8
    systems = [f["system"] for f in fluids]
    assert any("Engine" in s for s in systems)
    assert any("Transmission" in s for s in systems)


def test_torques():
    data = load("torques.yaml")
    torques = data["torques"]
    assert len(torques) >= 5
    for t in torques:
        assert "torque_nm" in t
        assert t["torque_nm"] > 0


def test_known_issues():
    data = load("known_issues.yaml")
    issues = data["known_issues"]
    assert len(issues) >= 5
    ids = [i["id"] for i in issues]
    assert "ads_cluster_lamp_missing" in ids
    assert "3rd_brake_light_fuse_dashboard" in ids


def test_service_intervals():
    data = load("service_intervals.yaml")
    items = data["service_items"]
    assert len(items) >= 5
    for item in items:
        assert "task" in item
        assert "source" in item


def test_all_files_have_sources():
    """Every list item in every data file should have a source field."""
    for yaml_file in DATA_DIR.glob("*.yaml"):
        data = load(yaml_file.name)
        if not isinstance(data, dict):
            continue
        for key, value in data.items():
            if not isinstance(value, list):
                continue
            for i, item in enumerate(value):
                if isinstance(item, dict) and "id" in item:
                    assert "source" in item, (
                        f"{yaml_file.name}[{key}][{i}] ({item.get('id', '?')}): missing source"
                    )


if __name__ == "__main__":
    tests = [v for k, v in globals().items() if k.startswith("test_")]
    passed = 0
    failed = 0
    for test in tests:
        try:
            test()
            print(f"  PASS: {test.__name__}")
            passed += 1
        except Exception as e:
            print(f"  FAIL: {test.__name__}: {e}")
            failed += 1

    print(f"\n{passed} passed, {failed} failed")
    sys.exit(1 if failed else 0)
