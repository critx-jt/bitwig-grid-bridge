import json
from pathlib import Path


INVENTORY_PATH = Path(__file__).parents[1] / "docs" / "grid-device-inventory.json"


def test_inventory_contains_reusable_interface_metadata_only():
    inventory = json.loads(INVENTORY_PATH.read_text())

    assert inventory["schema_version"] == "grid-device-inventory.v2"
    assert set(inventory) == {
        "schema_version",
        "inventory_revision",
        "revision_id",
        "bitwig_version",
        "source",
        "catalog",
        "devices",
    }
    assert {
        item["package_id"] for item in inventory["catalog"]
    } == {device["package_id"] for device in inventory["devices"]}

    for device in inventory["devices"]:
        assert set(device) == {"name", "package_id", "inputs", "outputs", "parameters"}
        for port in [*device["inputs"], *device["outputs"]]:
            assert set(port) == {"index", "name"}
        for parameter in device["parameters"]:
            assert set(parameter) <= {"id", "type", "range", "options"}
            assert "value" not in parameter
            assert "label" not in parameter
            assert "display" not in parameter
