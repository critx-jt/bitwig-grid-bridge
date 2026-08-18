"""
Tests for the Bitwig MCP Server tools module.
"""

from unittest.mock import MagicMock

import pytest

from bitwig_mcp_server.mcp.tools import execute_tool, get_bitwig_tools


def test_get_bitwig_tools():
    """Test that get_bitwig_tools returns the expected tools."""
    tools = get_bitwig_tools()

    # Get all tool names
    tool_names = {tool.name for tool in tools}

    # Check the supported Grid Bridge tool surface.
    expected_core_names = {
        "get_selected_device_state",
        "set_selected_device_parameters",
        "save_parameter_snapshot",
        "compare_parameter_snapshots",
        "apply_parameter_snapshot",
        "grid_list_style_presets",
        "grid_list_soundscape_styles",
        "grid_soundscape_plan",
        "get_grid_host_modulators",
        "grid_shape_start",
        "grid_shape_compose",
        "grid_shape_status",
        "grid_shape_apply",
        "grid_shape_undo",
        "grid_insert_device",
        "grid_insert_module",
        "grid_insert_modulator",
        "grid_set_modulator_parameter",
        "grid_set_module_parameter",
        "grid_connect_modules",
        "grid_connect_modulator",
        "grid_disconnect_module",
        "get_grid_graph",
        "search_grid_modules",
        "search_grid_modulators",
        "grid_project_undo",
        "grid_project_redo",
        "grid_navigate_device",
        "grid_list_tracks",
        "grid_select_track",
    }
    for tool_name in expected_core_names:
        assert tool_name in tool_names, f"Missing core tool: {tool_name}"
    assert tool_names.isdisjoint(
        {
            "transport_play",
            "set_tempo",
            "set_track_volume",
            "set_track_pan",
            "toggle_track_mute",
            "set_device_parameter",
            "toggle_device_bypass",
            "select_device_sibling",
            "navigate_device",
            "enter_device_layer",
            "exit_device_layer",
            "toggle_device_window",
        }
    )

    # Check schema structure
    for tool in tools:
        assert hasattr(tool, "inputSchema")
        assert isinstance(tool.inputSchema, dict)
        assert "type" in tool.inputSchema
        assert tool.inputSchema["type"] == "object"


@pytest.mark.asyncio
async def test_execute_tool_set_selected_device_parameters():
    """Batch parameter writes preserve integer indexes and values."""
    controller = MagicMock()
    controller.set_selected_device_parameters.return_value = [1, 2]

    result = await execute_tool(
        controller,
        "set_selected_device_parameters",
        {"parameters": {"1": 64, "2": 96}},
    )

    controller.set_selected_device_parameters.assert_called_once_with({1: 64, 2: 96})
    assert '"changed": [1, 2]' in result[0].text


@pytest.mark.asyncio
async def test_execute_tool_compare_parameter_snapshots():
    """Snapshot comparison is returned as structured JSON."""
    controller = MagicMock()
    controller.compare_parameter_snapshots.return_value = {
        "identical": False,
        "changed": [{"index": 1, "before": 64, "after": 96}],
    }

    result = await execute_tool(
        controller,
        "compare_parameter_snapshots",
        {"first": "dry", "second": "bright"},
    )

    controller.compare_parameter_snapshots.assert_called_once_with("dry", "bright")
    assert '"identical": false' in result[0].text


@pytest.mark.asyncio
async def test_execute_tool_grid_shape_style_preview():
    controller = MagicMock()
    controller.get_selected_device_state.return_value = {
        "available": True,
        "properties": {"name": "Poly Grid"},
        "parameters": [
            {"index": 2, "name": "PW", "exists": True, "value": 64.0},
        ],
    }

    result = await execute_tool(
        controller,
        "grid_shape_start",
        {"brief": "slow evolving air", "style": "slow-air"},
    )

    assert "slow-air" in result[0].text
    assert "mutates" in result[0].text
    assert controller.set_selected_device_parameters.call_count == 0


@pytest.mark.asyncio
async def test_execute_tool_lists_style_presets():
    result = await execute_tool(MagicMock(), "grid_list_style_presets", {})

    assert "slow-air" in result[0].text
    assert "percussive contrast" in result[0].text


@pytest.mark.asyncio
async def test_execute_tool_grid_graph_reads_and_module_write():
    controller = MagicMock()
    controller.get_grid_graph.return_value = {"ok": True, "modules": {"count": 0}}
    controller.grid_set_module_parameter.return_value = {"ok": True, "changed": True}

    graph = await execute_tool(controller, "get_grid_graph", {})
    assert '"modules"' in graph[0].text
    controller.get_grid_graph.assert_called_once_with()

    result = await execute_tool(
        controller,
        "grid_set_module_parameter",
        {
            "module_id": "2",
            "parameter_id": "TIMBRE",
            "value": 0.25,
            "confirm": True,
        },
    )
    assert '"changed": true' in result[0].text
    controller.grid_set_module_parameter.assert_called_once_with("2", "TIMBRE", 0.25)


@pytest.mark.asyncio
async def test_execute_tool_grid_mutations_require_confirmation():
    controller = MagicMock()
    result = await execute_tool(
        controller,
        "grid_connect_modules",
        {
            "source_module_id": "2",
            "source_port": 0,
            "target_module_id": "1",
            "target_port": 0,
            "confirm": False,
        },
    )
    assert "confirm must be true" in result[0].text
    controller.grid_connect_modules.assert_not_called()


@pytest.mark.asyncio
async def test_execute_tool_allows_cooperative_grid_mutation():
    controller = MagicMock()
    controller.grid_connect_modules.return_value = {"ok": True, "changed": True}
    result = await execute_tool(
        controller,
        "grid_connect_modules",
        {
            "source_module_id": "2",
            "source_port": 0,
            "target_module_id": "1",
            "target_port": 0,
            "cooperative": True,
        },
    )
    assert '"changed": true' in result[0].text
    controller.grid_connect_modules.assert_called_once_with("2", 0, "1", 0)


@pytest.mark.asyncio
async def test_execute_tool_modulator_catalog_and_mutations():
    controller = MagicMock()
    controller.search_grid_modulators.return_value = {
        "ok": True,
        "modulators": [{"name": "LFO", "category": "lfo"}],
    }
    controller.grid_insert_modulator.return_value = {"ok": True, "operation": "insert"}
    controller.grid_connect_modulator.return_value = {
        "ok": True,
        "operation": "connect",
    }
    controller.grid_set_modulator_parameter.return_value = {
        "ok": True,
        "operation": "set_parameter",
    }

    catalog = await execute_tool(
        controller,
        "search_grid_modulators",
        {"query": "lfo"},
    )
    assert '"LFO"' in catalog[0].text
    controller.search_grid_modulators.assert_called_once_with("lfo")

    inserted = await execute_tool(
        controller,
        "grid_insert_modulator",
        {"package_id": "uuid", "x": 2, "y": 3, "confirm": True},
    )
    assert '"insert"' in inserted[0].text
    controller.grid_insert_modulator.assert_called_once_with("uuid", 2, 3)

    connected = await execute_tool(
        controller,
        "grid_connect_modulator",
        {
            "source_module_id": "2",
            "source_port": 0,
            "target_module_id": "1",
            "target_port": 0,
            "cooperative": True,
        },
    )
    assert '"connect"' in connected[0].text
    controller.grid_connect_modulator.assert_called_once_with("2", 0, "1", 0)
    tuned = await execute_tool(
        controller,
        "grid_set_modulator_parameter",
        {
            "module_id": "2",
            "parameter_id": "RATE",
            "value": -0.25,
            "confirm": True,
        },
    )
    assert '"set_parameter"' in tuned[0].text
    controller.grid_set_modulator_parameter.assert_called_once_with("2", "RATE", -0.25)


@pytest.mark.asyncio
async def test_execute_tool_soundscape_plan_is_non_mutating():
    controller = MagicMock()

    result = await execute_tool(
        controller,
        "grid_soundscape_plan",
        {
            "brief": "A sparse rainy night with distant tonal events",
            "density": 0.2,
            "motion": 0.4,
        },
    )

    assert '"style": "weather-texture"' in result[0].text
    assert '"mutates"' not in result[0].text
    controller.assert_not_called()


@pytest.mark.asyncio
async def test_execute_tool_host_modulator_inspection():
    controller = MagicMock()
    controller.get_grid_host_modulators.return_value = {
        "available": True,
        "sources": [{"source_index": 0, "name": "Random", "mapped": False}],
    }

    result = await execute_tool(controller, "get_grid_host_modulators", {})

    assert '"Random"' in result[0].text
    controller.get_grid_host_modulators.assert_called_once_with()


@pytest.mark.asyncio
async def test_execute_tool_lists_and_selects_grid_track():
    controller = MagicMock()
    controller.grid_tracks.return_value = {
        "ok": True,
        "tracks": [{"index": 2, "name": "Poly Grid"}],
    }
    controller.grid_select_track.return_value = {
        "ok": True,
        "selection": "track",
        "index": 2,
    }

    tracks = await execute_tool(controller, "grid_list_tracks", {})
    selected = await execute_tool(
        controller, "grid_select_track", {"track_index": 2}
    )

    assert '"Poly Grid"' in tracks[0].text
    assert '"index": 2' in selected[0].text
    controller.grid_tracks.assert_called_once_with()
    controller.grid_select_track.assert_called_once_with(2)


@pytest.mark.asyncio
async def test_execute_tool_rejects_invalid_grid_track_index():
    controller = MagicMock()

    result = await execute_tool(
        controller, "grid_select_track", {"track_index": True}
    )

    assert "track_index must be an integer between 0 and 15" in result[0].text
    controller.grid_select_track.assert_not_called()
