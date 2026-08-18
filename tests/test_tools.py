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

    # Check that we have the expected transport and device tools
    expected_core_names = {
        # Basic transport and track tools
        "transport_play",
        "set_tempo",
        "set_track_volume",
        "set_track_pan",
        "toggle_track_mute",
        "set_device_parameter",
        # Device tools
        "toggle_device_bypass",
        "select_device_sibling",
        "navigate_device",
        "enter_device_layer",
        "exit_device_layer",
        "toggle_device_window",
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
async def test_execute_tool_transport_play():
    """Test execute_tool with transport_play tool."""
    # Create mock controller
    controller = MagicMock()
    controller.client = MagicMock()

    # Execute the tool
    result = await execute_tool(controller, "transport_play", {})

    # Check that the expected client method was called
    controller.client.play.assert_called_once()

    # Check the result
    assert len(result) == 1
    assert result[0].type == "text"
    assert "toggled" in result[0].text


@pytest.mark.asyncio
async def test_execute_tool_set_tempo():
    """Test execute_tool with set_tempo tool."""
    # Create mock controller
    controller = MagicMock()
    controller.client = MagicMock()

    # Execute the tool
    result = await execute_tool(controller, "set_tempo", {"bpm": 120})

    # Check that the expected client method was called with correct arguments
    controller.client.set_tempo.assert_called_once_with(120)

    # Check the result
    assert len(result) == 1
    assert result[0].type == "text"
    assert "120 BPM" in result[0].text


@pytest.mark.asyncio
async def test_execute_tool_set_tempo_missing_arg():
    """Test execute_tool with set_tempo tool and missing argument."""
    # Create mock controller
    controller = MagicMock()

    # Execute the tool with missing argument
    result = await execute_tool(controller, "set_tempo", {})

    # Check that the result indicates an error
    assert len(result) == 1
    assert result[0].type == "text"
    assert "Error" in result[0].text
    assert "Missing required argument: bpm" in result[0].text


@pytest.mark.asyncio
async def test_execute_tool_set_track_volume():
    """Test execute_tool with set_track_volume tool."""
    # Create mock controller
    controller = MagicMock()
    controller.client = MagicMock()

    # Execute the tool
    result = await execute_tool(
        controller, "set_track_volume", {"track_index": 1, "volume": 64}
    )

    # Check that the expected client method was called with correct arguments
    controller.client.set_track_volume.assert_called_once_with(1, 64)

    # Check the result
    assert len(result) == 1
    assert result[0].type == "text"
    assert "Track 1 volume set to 64" in result[0].text


@pytest.mark.asyncio
async def test_execute_tool_invalid_arguments():
    """Test execute_tool with invalid arguments."""
    # Create mock controller
    controller = MagicMock()

    # Test cases for various invalid arguments
    test_cases = [
        (
            "set_track_volume",
            {"track_index": "not-a-number", "volume": 64},
            "Invalid track_index",
        ),
        (
            "set_track_volume",
            {"track_index": 0, "volume": 64},
            "must be a positive integer",
        ),
        ("set_track_volume", {"track_index": 1, "volume": 200}, "Invalid volume"),
        ("set_device_parameter", {"param_index": 1, "value": -10}, "Invalid value"),
    ]

    for tool_name, args, expected_error in test_cases:
        result = await execute_tool(controller, tool_name, args)

        # Check that the result indicates the expected error
        assert len(result) == 1
        assert result[0].type == "text"
        assert "Error" in result[0].text
        assert expected_error in result[0].text


@pytest.mark.asyncio
async def test_execute_tool_unknown():
    """Test execute_tool with unknown tool."""
    # Create mock controller
    controller = MagicMock()

    # Execute with unknown tool name
    result = await execute_tool(controller, "unknown_tool", {})

    # Check that the result indicates the expected error
    assert len(result) == 1
    assert result[0].type == "text"
    assert "Error" in result[0].text
    assert "Unknown tool" in result[0].text


@pytest.mark.asyncio
async def test_execute_tool_toggle_device_bypass():
    """Test execute_tool with toggle_device_bypass tool."""
    # Create a mock controller
    controller = MagicMock()
    controller.client.toggle_device_bypass = MagicMock()

    # Execute the tool
    result = await execute_tool(controller, "toggle_device_bypass", {})

    # Check that the controller method was called
    controller.client.toggle_device_bypass.assert_called_once()

    # Check the result
    assert len(result) == 1
    assert result[0].type == "text"
    assert result[0].text == "Device bypass toggled"


@pytest.mark.asyncio
async def test_execute_tool_select_device_sibling():
    """Test execute_tool with select_device_sibling tool."""
    # Create a mock controller
    controller = MagicMock()
    controller.client.select_device_sibling = MagicMock()

    # Execute the tool
    result = await execute_tool(
        controller, "select_device_sibling", {"sibling_index": 3}
    )

    # Check that the controller method was called
    controller.client.select_device_sibling.assert_called_once_with(3)

    # Check the result
    assert len(result) == 1
    assert result[0].type == "text"
    assert result[0].text == "Selected sibling device 3"


@pytest.mark.asyncio
async def test_execute_tool_select_device_sibling_invalid_arg():
    """Test execute_tool with select_device_sibling tool and invalid arguments."""
    # Create a mock controller
    controller = MagicMock()

    # Test missing required argument
    result = await execute_tool(controller, "select_device_sibling", {})
    assert "Missing required argument" in result[0].text

    # Test invalid argument value
    result = await execute_tool(
        controller, "select_device_sibling", {"sibling_index": 0}
    )
    assert "Invalid sibling_index" in result[0].text

    result = await execute_tool(
        controller, "select_device_sibling", {"sibling_index": 9}
    )
    assert "Invalid sibling_index" in result[0].text


@pytest.mark.asyncio
async def test_execute_tool_navigate_device():
    """Test execute_tool with navigate_device tool."""
    # Create a mock controller
    controller = MagicMock()
    controller.client.navigate_device = MagicMock()

    # Execute the tool with "next" direction
    result = await execute_tool(controller, "navigate_device", {"direction": "next"})
    controller.client.navigate_device.assert_called_with("next")
    assert result[0].text == "Navigated to next device"

    # Execute the tool with "previous" direction
    result = await execute_tool(
        controller, "navigate_device", {"direction": "previous"}
    )
    controller.client.navigate_device.assert_called_with("previous")
    assert result[0].text == "Navigated to previous device"

    # Test invalid direction
    result = await execute_tool(controller, "navigate_device", {"direction": "invalid"})
    assert "Invalid direction" in result[0].text


@pytest.mark.asyncio
async def test_execute_tool_device_layer_operations():
    """Test execute_tool with device layer operations."""
    # Create a mock controller
    controller = MagicMock()
    controller.client.enter_device_layer = MagicMock()
    controller.client.exit_device_layer = MagicMock()

    # Test enter_device_layer
    result = await execute_tool(controller, "enter_device_layer", {"layer_index": 2})
    controller.client.enter_device_layer.assert_called_once_with(2)
    assert result[0].text == "Entered device layer 2"

    # Test exit_device_layer
    result = await execute_tool(controller, "exit_device_layer", {})
    controller.client.exit_device_layer.assert_called_once()
    assert result[0].text == "Exited device layer"

    # Test invalid layer index
    result = await execute_tool(controller, "enter_device_layer", {"layer_index": 0})
    assert "Invalid layer_index" in result[0].text


@pytest.mark.asyncio
async def test_execute_tool_toggle_device_window():
    """Test execute_tool with toggle_device_window tool."""
    # Create a mock controller
    controller = MagicMock()
    controller.client.toggle_device_window = MagicMock()

    # Execute the tool
    result = await execute_tool(controller, "toggle_device_window", {})

    # Check that the controller method was called
    controller.client.toggle_device_window.assert_called_once()

    # Check the result
    assert len(result) == 1
    assert result[0].type == "text"
    assert result[0].text == "Device window toggled"


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
