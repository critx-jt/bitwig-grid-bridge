import pytest

from bitwig_mcp_server.grid_soundscaping import (
    list_soundscape_styles,
    plan_soundscape,
)


def test_weather_plan_is_layered_and_live_resolvable():
    plan = plan_soundscape(
        "Sparse rain with soft distant tonal events",
        density=0.3,
        motion=0.4,
    )

    assert plan["style"] == "weather-texture"
    assert plan["assembly_order"] == ["texture", "events", "space"]
    assert "Noise" in plan["module_queries"]
    assert "All-pass Delay" in plan["module_queries"]
    assert plan["resolution"]["step_2"].startswith("Resolve every module_queries")
    assert all("preset" not in layer for layer in plan["layers"])


def test_low_density_removes_event_layer_without_removing_bed():
    plan = plan_soundscape("deep ambient drone", density=0.1)

    assert plan["style"] == "deep-ambient"
    assert "bed" in plan["assembly_order"]
    assert "events" not in plan["assembly_order"]
    assert "space" in plan["assembly_order"]


def test_high_density_adds_optional_accent_only_to_event_styles():
    plan = plan_soundscape("distant signals", density=0.9)

    assert "accent" in plan["assembly_order"]
    assert plan["layers"][-1]["id"] == "accent"


def test_unknown_style_and_out_of_range_controls_are_rejected():
    with pytest.raises(ValueError, match="unknown soundscape style"):
        plan_soundscape("test", style="unknown")
    with pytest.raises(ValueError, match="between 0 and 1"):
        plan_soundscape("test", density=1.1)


def test_style_listing_is_provenance_free():
    styles = list_soundscape_styles()

    assert {style["id"] for style in styles} >= {
        "deep-ambient",
        "weather-texture",
        "distant-events",
        "harmonic-drift",
        "artifact-bed",
        "generative-percussion",
    }
    assert all("source" not in style for style in styles)
