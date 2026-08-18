from copy import deepcopy

import pytest

from bitwig_mcp_server.grid_workflow import GridShapeManager


class FakeController:
    def __init__(self):
        self.state = {
            "available": True,
            "properties": {"name": "Poly Grid", "device_type": "instrument"},
            "parameters": [
                {"index": 1, "name": "Pulse %", "exists": True, "value": 0.0},
                {"index": 2, "name": "PW", "exists": True, "value": 64.0},
                {"index": 3, "name": "Saw %", "exists": True, "value": 128.0},
                {"index": 4, "name": "Tri %", "exists": True, "value": 0.0},
                {"index": 5, "name": "Num", "exists": True, "value": 64.0},
                {"index": 6, "name": "Den", "exists": True, "value": 32.0},
                {"index": 7, "name": "Pitch", "exists": True, "value": 64.0},
                {"index": 8, "name": "Detune", "exists": True, "value": 64.0},
            ],
        }
        self.writes = []

    def get_selected_device_state(self):
        return deepcopy(self.state)

    def set_selected_device_parameters(self, parameters):
        self.writes.append(parameters)
        for index, value in parameters.items():
            self.state["parameters"][index - 1]["value"] = value
        return list(parameters)


class DelayedController(FakeController):
    """Model Bitwig's host-thread write/readback delay."""

    def __init__(self):
        super().__init__()
        self.read_count = 0
        self.pending = None
        self.pending_at = 0

    def get_selected_device_state(self):
        self.read_count += 1
        if self.pending is not None and self.read_count >= self.pending_at:
            for index, value in self.pending.items():
                self.state["parameters"][index - 1]["value"] = value
            self.pending = None
        return deepcopy(self.state)

    def set_selected_device_parameters(self, parameters):
        self.writes.append(parameters)
        self.pending = parameters.copy()
        self.pending_at = self.read_count + 2
        return list(parameters)


def test_start_and_compose_are_preview_only():
    controller = FakeController()
    manager = GridShapeManager()

    preview = manager.start(controller, "crystalline but restrained", "glass", 0.5)

    assert preview["preview"]["mutates"] is False
    assert preview["preview"]["change_count"] == 8
    assert controller.writes == []

    revised = manager.compose(controller, preview["session_id"], controls={"PW": 0.2})

    assert revised["revision"] == 2
    assert revised["controls"] == {"PW": 0.2}
    assert controller.writes == []


def test_apply_requires_confirmation_and_undo_restores_values():
    controller = FakeController()
    manager = GridShapeManager()
    preview = manager.start(controller, "warm pulse", "ember", 1.0)

    with pytest.raises(ValueError, match="confirm must be true"):
        manager.apply(controller, preview["session_id"], preview["revision"], False)

    applied = manager.apply(controller, preview["session_id"], preview["revision"], True)
    assert applied["applied"]["changed"] == list(range(1, 9))
    assert len(controller.writes) == 1

    undone = manager.undo(controller, preview["session_id"])
    assert undone["undone"]["changed"] == list(range(1, 9))
    assert len(controller.writes) == 2
    assert controller.state["parameters"][1]["value"] == 64.0


def test_apply_waits_for_host_thread_readback():
    controller = DelayedController()
    manager = GridShapeManager()
    preview = manager.start(controller, "delayed host write", "ember", 1.0)

    applied = manager.apply(controller, preview["session_id"], preview["revision"], True)

    assert applied["applied"]["after"]["1"] != applied["applied"]["before"]["1"]
    assert controller.read_count >= 4


def test_style_profile_selects_conservative_style_profile():
    preview = GridShapeManager().start(
        FakeController(),
        "slow evolving air",
        style="slow-air",
    )

    assert preview["style"] == "slow-air"
    assert preview["preset"] == "glass"
    assert preview["intensity"] == 0.35
    assert "defined scale" in preview["principles"]


def test_apply_rejects_external_parameter_changes():
    controller = FakeController()
    manager = GridShapeManager()
    preview = manager.start(controller, "slow movement", "hollow", 0.8)
    controller.state["parameters"][0]["value"] = 32.0

    with pytest.raises(ValueError, match="changed outside this session"):
        manager.apply(controller, preview["session_id"], preview["revision"], True)


def test_unknown_explicit_control_is_rejected():
    with pytest.raises(ValueError, match="not exposed"):
        GridShapeManager().start(
            FakeController(),
            "test",
            controls={"Imaginary Module": 0.5},
        )
