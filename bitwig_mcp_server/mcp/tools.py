"""
Bitwig MCP Tools

This module provides MCP tools for controlling Bitwig Studio.
"""

import json
import logging
import math
from typing import Any

from mcp.types import TextContent, Tool

from bitwig_mcp_server.osc.controller import BitwigOSCController

# Set up logging
logger = logging.getLogger(__name__)


def _mutation_is_authorized(arguments: dict[str, Any]) -> bool:
    """Allow explicit confirmation or prompt/skill-authorized cooperation."""
    return arguments.get("confirm") is True or arguments.get("cooperative") is True


def get_bitwig_tools() -> list[Tool]:
    """Get all available Bitwig tools

    Returns:
        List of Tool objects
    """
    return [
        Tool(
            name="get_selected_device_state",
            description=(
                "Read the currently selected device, including Grid graph topology "
                "and editable module parameters when the Grid bridge is available."
            ),
            inputSchema={"type": "object", "properties": {}},
        ),
        Tool(
            name="get_grid_capabilities",
            description=(
                "Inspect bridge capabilities and selected-device container flags. "
                "Use this before attempting automated Grid reconstruction."
            ),
            inputSchema={"type": "object", "properties": {}},
        ),
        Tool(
            name="get_grid_graph",
            description=(
                "Read the selected Grid's module instances, ports, connections, "
                "coordinates, and editable module parameters."
            ),
            inputSchema={"type": "object", "properties": {}},
        ),
        Tool(
            name="search_grid_modules",
            description="Search installed Bitwig Grid modules by name or package UUID.",
            inputSchema={
                "type": "object",
                "properties": {"query": {"type": "string"}},
            },
        ),
        Tool(
            name="search_grid_modulators",
            description=(
                "Search the installed Grid modulation catalog. Results include "
                "semantic roles, input/output hints, and tuning parameters."
            ),
            inputSchema={
                "type": "object",
                "properties": {"query": {"type": "string"}},
            },
        ),
        Tool(
            name="grid_soundscape_plan",
            description=(
                "Create a generic, non-mutating Grid soundscape recipe from an "
                "artistic brief. The result names live-resolvable module roles, "
                "routing order, tuning targets, and safety guardrails; it never "
                "contains a preset payload."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "brief": {"type": "string"},
                    "style": {"type": "string"},
                    "density": {"type": "number", "minimum": 0, "maximum": 1},
                    "motion": {"type": "number", "minimum": 0, "maximum": 1},
                    "contrast": {"type": "number", "minimum": 0, "maximum": 1},
                    "temperature": {"type": "number", "minimum": 0, "maximum": 1},
                },
                "required": ["brief"],
            },
        ),
        Tool(
            name="grid_list_soundscape_styles",
            description=(
                "List the internal generic Grid soundscape style vocabulary "
                "without exposing external patch or preset content."
            ),
            inputSchema={"type": "object", "properties": {}},
        ),
        Tool(
            name="get_grid_host_modulators",
            description=(
                "Inspect host-level modulation sources exposed by the selected "
                "Grid device, including names and mapping state. This is "
                "read-only; resolve module parameters from the live graph."
            ),
            inputSchema={"type": "object", "properties": {}},
        ),
        Tool(
            name="grid_insert_modulator",
            description=(
                "Insert a cataloged Grid modulator or Modulator Out at graph "
                "coordinates. This mutates the project and requires confirmation "
                "unless the prompt or active skill explicitly requests cooperative work."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "package_id": {"type": "string"},
                    "x": {"type": "integer", "minimum": -4096, "maximum": 4096},
                    "y": {"type": "integer", "minimum": -4096, "maximum": 4096},
                    "confirm": {"type": "boolean"},
                    "cooperative": {"type": "boolean"},
                },
                "required": ["package_id", "x", "y"],
            },
        ),
        Tool(
            name="grid_connect_modulator",
            description=(
                "Connect a cataloged Grid modulator output to a Grid input. "
                "This mutates the project and requires confirmation unless the "
                "prompt or active skill explicitly requests cooperative work."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "source_module_id": {"type": "string"},
                    "source_port": {"type": "integer", "minimum": 0},
                    "target_module_id": {"type": "string"},
                    "target_port": {"type": "integer", "minimum": 0},
                    "confirm": {"type": "boolean"},
                    "cooperative": {"type": "boolean"},
                },
                "required": [
                    "source_module_id",
                    "source_port",
                    "target_module_id",
                    "target_port",
                ],
            },
        ),
        Tool(
            name="grid_set_modulator_parameter",
            description=(
                "Tune one parameter on a cataloged Grid modulator. Use the "
                "catalog and live graph metadata for valid ranges and options. "
                "This mutates the project and requires confirmation unless the "
                "prompt or active skill explicitly requests cooperative work."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "module_id": {"type": "string"},
                    "parameter_id": {"type": "string"},
                    "value": {"anyOf": [{"type": "number"}, {"type": "boolean"}]},
                    "confirm": {"type": "boolean"},
                    "cooperative": {"type": "boolean"},
                },
                "required": ["module_id", "parameter_id", "value"],
            },
        ),
        Tool(
            name="grid_insert_module",
            description=(
                "Insert a known Grid module at graph coordinates. This mutates the "
                "project and requires confirmation unless the prompt or active skill "
                "explicitly requests cooperative work."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "package_id": {"type": "string"},
                    "x": {"type": "integer", "minimum": -4096, "maximum": 4096},
                    "y": {"type": "integer", "minimum": -4096, "maximum": 4096},
                    "confirm": {"type": "boolean"},
                    "cooperative": {"type": "boolean"},
                },
                "required": ["package_id", "x", "y"],
            },
        ),
        Tool(
            name="grid_set_module_parameter",
            description=(
                "Set one editable Grid module parameter. Use get_grid_graph for "
                "the parameter's native range or discrete options; toggles use booleans. "
                "This mutates the project and requires confirmation unless the "
                "prompt or active skill explicitly requests cooperative work."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "module_id": {"type": "string"},
                    "parameter_id": {"type": "string"},
                    "value": {"anyOf": [{"type": "number"}, {"type": "boolean"}]},
                    "confirm": {"type": "boolean"},
                    "cooperative": {"type": "boolean"},
                },
                "required": ["module_id", "parameter_id", "value"],
            },
        ),
        Tool(
            name="grid_connect_modules",
            description=(
                "Connect a Grid module output to an input port. This mutates the "
                "project and requires confirmation unless the prompt or active "
                "skill explicitly requests cooperative work."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "source_module_id": {"type": "string"},
                    "source_port": {"type": "integer", "minimum": 0},
                    "target_module_id": {"type": "string"},
                    "target_port": {"type": "integer", "minimum": 0},
                    "confirm": {"type": "boolean"},
                    "cooperative": {"type": "boolean"},
                },
                "required": [
                    "source_module_id",
                    "source_port",
                    "target_module_id",
                    "target_port",
                ],
            },
        ),
        Tool(
            name="grid_disconnect_module",
            description=(
                "Disconnect a Grid input port. This mutates the project and "
                "requires confirmation unless the prompt or active skill "
                "explicitly requests cooperative work."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "target_module_id": {"type": "string"},
                    "target_port": {"type": "integer", "minimum": 0},
                    "confirm": {"type": "boolean"},
                    "cooperative": {"type": "boolean"},
                },
                "required": ["target_module_id", "target_port"],
            },
        ),
        Tool(
            name="grid_list_style_presets",
            description=(
                "List the repository's authored Grid style profiles and their "
                "behavioral principles."
            ),
            inputSchema={"type": "object", "properties": {}},
        ),
        Tool(
            name="grid_shape_start",
            description=(
                "Start a preview-first Bitwig Grid shaping session. "
                "Compose a style draft without mutating Bitwig."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "brief": {
                        "type": "string",
                        "description": "Human intent for the Grid sound and interaction.",
                    },
                    "preset": {
                        "type": "string",
                        "enum": ["acid", "ember", "glass", "hollow"],
                        "description": "Optional parameter scaffold; style profiles choose one when omitted.",
                    },
                    "style": {
                        "type": "string",
                        "enum": [
                            "slow-air",
                            "deep-bed",
                            "distant-events",
                            "soft-drift",
                            "night-motion",
                            "layered-motion",
                            "pulse-lab",
                        ],
                        "description": "Optional authored style profile for motion, density, and space.",
                    },
                    "intensity": {
                        "type": "number",
                        "minimum": 0,
                        "maximum": 1,
                        "description": "Blend amount; style profiles provide a conservative default.",
                    },
                    "controls": {
                        "type": "object",
                        "description": "Optional exposed parameter names or indexes mapped to 0-1 values.",
                        "additionalProperties": {
                            "type": "number",
                            "minimum": 0,
                            "maximum": 1,
                        },
                    },
                },
                "required": ["brief"],
            },
        ),
        Tool(
            name="grid_shape_compose",
            description=(
                "Revise a Grid shaping draft. This is a non-mutating preview step; "
                "apply only after reviewing the returned changes."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "session_id": {"type": "string"},
                    "preset": {
                        "type": "string",
                        "enum": ["acid", "ember", "glass", "hollow"],
                    },
                    "style": {
                        "type": "string",
                        "enum": [
                            "slow-air",
                            "deep-bed",
                            "distant-events",
                            "soft-drift",
                            "night-motion",
                            "layered-motion",
                            "pulse-lab",
                        ],
                    },
                    "intensity": {"type": "number", "minimum": 0, "maximum": 1},
                    "controls": {
                        "type": "object",
                        "additionalProperties": {
                            "type": "number",
                            "minimum": 0,
                            "maximum": 1,
                        },
                    },
                },
                "required": ["session_id"],
            },
        ),
        Tool(
            name="grid_shape_status",
            description="Return the live state and current preview for a Grid shaping session.",
            inputSchema={
                "type": "object",
                "properties": {"session_id": {"type": "string"}},
                "required": ["session_id"],
            },
        ),
        Tool(
            name="grid_shape_apply",
            description=(
                "Apply an exact reviewed Grid shaping revision. Requires confirmation "
                "unless the prompt or active skill explicitly requests cooperative work; "
                "stale or externally changed state is always rejected."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "session_id": {"type": "string"},
                    "revision": {"type": "integer", "minimum": 1},
                    "confirm": {"type": "boolean"},
                    "cooperative": {"type": "boolean"},
                },
                "required": ["session_id", "revision"],
            },
        ),
        Tool(
            name="grid_shape_undo",
            description="Restore the previous parameter state for a Grid shaping session.",
            inputSchema={
                "type": "object",
                "properties": {"session_id": {"type": "string"}},
                "required": ["session_id"],
            },
        ),
        Tool(
            name="grid_insert_device",
            description=(
                "Insert one known Bitwig device by UUID at the selected device. "
                "This mutates the project and requires confirmation unless the "
                "prompt or active skill explicitly requests cooperative work."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "position": {"type": "string", "enum": ["before", "after"]},
                    "device_id": {"type": "string"},
                    "confirm": {"type": "boolean"},
                    "cooperative": {"type": "boolean"},
                },
                "required": ["position", "device_id"],
            },
        ),
        Tool(
            name="grid_project_undo",
            description="Undo the latest Bitwig host operation through the Grid bridge.",
            inputSchema={"type": "object", "properties": {}},
        ),
        Tool(
            name="grid_project_redo",
            description="Redo the latest Bitwig host operation through the Grid bridge.",
            inputSchema={"type": "object", "properties": {}},
        ),
        Tool(
            name="grid_navigate_device",
            description="Navigate the selected device to its next, previous, or parent device.",
            inputSchema={
                "type": "object",
                "properties": {
                    "direction": {
                        "type": "string",
                        "enum": ["next", "previous", "parent"],
                    }
                },
                "required": ["direction"],
            },
        ),
        Tool(
            name="grid_list_tracks",
            description=(
                "List existing main tracks and their zero-based live bank indexes."
            ),
            inputSchema={"type": "object", "properties": {}},
        ),
        Tool(
            name="grid_select_track",
            description=(
                "Select a main track by the zero-based index returned by grid_list_tracks."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "track_index": {
                        "type": "integer",
                        "minimum": 0,
                        "maximum": 15,
                    }
                },
                "required": ["track_index"],
            },
        ),
        Tool(
            name="set_selected_device_parameters",
            description="Set multiple parameters on the currently selected device.",
            inputSchema={
                "type": "object",
                "properties": {
                    "parameters": {
                        "type": "object",
                        "description": "Map exposed parameter indexes to values in the 0-128 bridge range.",
                        "additionalProperties": {"type": "number"},
                    }
                },
                "required": ["parameters"],
            },
        ),
        Tool(
            name="save_parameter_snapshot",
            description="Save observable parameters of the selected device in memory.",
            inputSchema={
                "type": "object",
                "properties": {"name": {"type": "string"}},
                "required": ["name"],
            },
        ),
        Tool(
            name="compare_parameter_snapshots",
            description="Compare two in-memory selected-device parameter snapshots.",
            inputSchema={
                "type": "object",
                "properties": {
                    "first": {"type": "string"},
                    "second": {"type": "string"},
                },
                "required": ["first", "second"],
            },
        ),
        Tool(
            name="apply_parameter_snapshot",
            description="Apply an in-memory parameter snapshot to the selected device.",
            inputSchema={
                "type": "object",
                "properties": {"name": {"type": "string"}},
                "required": ["name"],
            },
        ),

    ]

async def execute_tool(
    controller: BitwigOSCController, name: str, arguments: dict[str, Any]
) -> list[TextContent]:
    """Execute a Bitwig tool

    Args:
        controller: BitwigOSCController instance
        name: Tool name to execute
        arguments: Tool arguments

    Returns:
        List of TextContent with results

    Raises:
        ValueError: If tool name is unknown or arguments are invalid
    """
    try:
        if name == "get_selected_device_state":
            state = controller.get_selected_device_state()
            return [TextContent(type="text", text=json.dumps(state, sort_keys=True))]

        elif name == "get_grid_capabilities":
            capabilities = controller.get_grid_capabilities()
            return [
                TextContent(type="text", text=json.dumps(capabilities, sort_keys=True))
            ]
        elif name == "get_grid_graph":
            graph = controller.get_grid_graph()
            return [TextContent(type="text", text=json.dumps(graph, sort_keys=True))]

        elif name == "get_grid_host_modulators":
            result = controller.get_grid_host_modulators()
            return [TextContent(type="text", text=json.dumps(result, sort_keys=True))]

        elif name == "search_grid_modules":
            query = arguments.get("query", "")
            if not isinstance(query, str):
                raise ValueError("query must be a string")
            result = controller.search_grid_modules(query)
            return [TextContent(type="text", text=json.dumps(result, sort_keys=True))]
        elif name == "search_grid_modulators":
            query = arguments.get("query", "")
            if not isinstance(query, str):
                raise ValueError("query must be a string")
            result = controller.search_grid_modulators(query)
            return [TextContent(type="text", text=json.dumps(result, sort_keys=True))]

        elif name == "grid_soundscape_plan":
            from bitwig_mcp_server.grid_soundscaping import plan_soundscape

            result = plan_soundscape(
                arguments.get("brief", ""),
                style=arguments.get("style"),
                density=arguments.get("density", 0.3),
                motion=arguments.get("motion", 0.35),
                contrast=arguments.get("contrast", 0.3),
                temperature=arguments.get("temperature", 0.5),
            )
            return [TextContent(type="text", text=json.dumps(result, sort_keys=True))]

        elif name == "grid_insert_modulator":
            if not _mutation_is_authorized(arguments):
                raise ValueError(
                    "confirm must be true unless cooperative work is authorized"
                )
            package_id = arguments.get("package_id")
            x = arguments.get("x")
            y = arguments.get("y")
            if not isinstance(package_id, str) or not package_id.strip():
                raise ValueError("package_id must be a non-empty UUID string")
            if isinstance(x, bool) or not isinstance(x, int) or not -4096 <= x <= 4096:
                raise ValueError("x must be an integer between -4096 and 4096")
            if isinstance(y, bool) or not isinstance(y, int) or not -4096 <= y <= 4096:
                raise ValueError("y must be an integer between -4096 and 4096")
            result = controller.grid_insert_modulator(package_id, x, y)
            return [TextContent(type="text", text=json.dumps(result, sort_keys=True))]

        elif name == "grid_connect_modulator":
            if not _mutation_is_authorized(arguments):
                raise ValueError(
                    "confirm must be true unless cooperative work is authorized"
                )
            source_module_id = arguments.get("source_module_id")
            target_module_id = arguments.get("target_module_id")
            source_port = arguments.get("source_port")
            target_port = arguments.get("target_port")
            if not isinstance(source_module_id, str) or not source_module_id.strip():
                raise ValueError("source_module_id must be a non-empty string")
            if not isinstance(target_module_id, str) or not target_module_id.strip():
                raise ValueError("target_module_id must be a non-empty string")
            if (
                isinstance(source_port, bool)
                or not isinstance(source_port, int)
                or source_port < 0
            ):
                raise ValueError("source_port must be a non-negative integer")
            if (
                isinstance(target_port, bool)
                or not isinstance(target_port, int)
                or target_port < 0
            ):
                raise ValueError("target_port must be a non-negative integer")
            result = controller.grid_connect_modulator(
                source_module_id,
                source_port,
                target_module_id,
                target_port,
            )
            return [TextContent(type="text", text=json.dumps(result, sort_keys=True))]
        elif name == "grid_set_modulator_parameter":
            if not _mutation_is_authorized(arguments):
                raise ValueError(
                    "confirm must be true unless cooperative work is authorized"
                )
            module_id = arguments.get("module_id")
            parameter_id = arguments.get("parameter_id")
            value = arguments.get("value")
            if not isinstance(module_id, str) or not module_id.strip():
                raise ValueError("module_id must be a non-empty string")
            if not isinstance(parameter_id, str) or not parameter_id.strip():
                raise ValueError("parameter_id must be a non-empty string")
            normalized_value: float | bool
            if isinstance(value, bool):
                normalized_value = value
            elif isinstance(value, (int, float)) and not isinstance(value, bool):
                if not math.isfinite(float(value)):
                    raise ValueError("numeric Grid parameter values must be finite")
                normalized_value = float(value)
            else:
                raise ValueError("value must be a boolean or number")
            result = controller.grid_set_modulator_parameter(
                module_id, parameter_id, normalized_value
            )
            return [TextContent(type="text", text=json.dumps(result, sort_keys=True))]

        elif name == "grid_insert_module":
            if not _mutation_is_authorized(arguments):
                raise ValueError(
                    "confirm must be true unless cooperative work is authorized"
                )
            package_id = arguments.get("package_id")
            x = arguments.get("x")
            y = arguments.get("y")
            if not isinstance(package_id, str) or not package_id.strip():
                raise ValueError("package_id must be a non-empty UUID string")
            if isinstance(x, bool) or not isinstance(x, int) or not -4096 <= x <= 4096:
                raise ValueError("x must be an integer between -4096 and 4096")
            if isinstance(y, bool) or not isinstance(y, int) or not -4096 <= y <= 4096:
                raise ValueError("y must be an integer between -4096 and 4096")
            result = controller.grid_insert_module(package_id, x, y)
            return [TextContent(type="text", text=json.dumps(result, sort_keys=True))]

        elif name == "grid_set_module_parameter":
            if not _mutation_is_authorized(arguments):
                raise ValueError(
                    "confirm must be true unless cooperative work is authorized"
                )
            module_id = arguments.get("module_id")
            parameter_id = arguments.get("parameter_id")
            value = arguments.get("value")
            if not isinstance(module_id, str) or not module_id.strip():
                raise ValueError("module_id must be a non-empty string")
            if not isinstance(parameter_id, str) or not parameter_id.strip():
                raise ValueError("parameter_id must be a non-empty string")
            if isinstance(value, bool):
                normalized_value = value
            elif isinstance(value, (int, float)) and not isinstance(value, bool):
                if not math.isfinite(float(value)):
                    raise ValueError("numeric Grid parameter values must be finite")
                normalized_value = float(value)
            else:
                raise ValueError("value must be a boolean or number")
            result = controller.grid_set_module_parameter(
                module_id, parameter_id, normalized_value
            )
            return [TextContent(type="text", text=json.dumps(result, sort_keys=True))]

        elif name == "grid_connect_modules":
            if not _mutation_is_authorized(arguments):
                raise ValueError(
                    "confirm must be true unless cooperative work is authorized"
                )
            source_module_id = arguments.get("source_module_id")
            target_module_id = arguments.get("target_module_id")
            source_port = arguments.get("source_port")
            target_port = arguments.get("target_port")
            if not isinstance(source_module_id, str) or not source_module_id.strip():
                raise ValueError("source_module_id must be a non-empty string")
            if not isinstance(target_module_id, str) or not target_module_id.strip():
                raise ValueError("target_module_id must be a non-empty string")
            if (
                isinstance(source_port, bool)
                or not isinstance(source_port, int)
                or source_port < 0
            ):
                raise ValueError("source_port must be a non-negative integer")
            if (
                isinstance(target_port, bool)
                or not isinstance(target_port, int)
                or target_port < 0
            ):
                raise ValueError("target_port must be a non-negative integer")
            result = controller.grid_connect_modules(
                source_module_id, source_port, target_module_id, target_port
            )
            return [TextContent(type="text", text=json.dumps(result, sort_keys=True))]

        elif name == "grid_disconnect_module":
            if not _mutation_is_authorized(arguments):
                raise ValueError(
                    "confirm must be true unless cooperative work is authorized"
                )
            target_module_id = arguments.get("target_module_id")
            target_port = arguments.get("target_port")
            if not isinstance(target_module_id, str) or not target_module_id.strip():
                raise ValueError("target_module_id must be a non-empty string")
            if (
                isinstance(target_port, bool)
                or not isinstance(target_port, int)
                or target_port < 0
            ):
                raise ValueError("target_port must be a non-negative integer")
            result = controller.grid_disconnect_module(target_module_id, target_port)
            return [TextContent(type="text", text=json.dumps(result, sort_keys=True))]

        elif name == "grid_list_style_presets":
            from bitwig_mcp_server.grid_workflow import GridShapeManager

            return [
                TextContent(
                    type="text",
                    text=json.dumps(GridShapeManager.list_styles(), sort_keys=True),
                )
            ]

        elif name == "grid_list_soundscape_styles":
            from bitwig_mcp_server.grid_soundscaping import list_soundscape_styles

            return [
                TextContent(
                    type="text",
                    text=json.dumps(list_soundscape_styles(), sort_keys=True),
                )
            ]

        elif name in {
            "grid_shape_start",
            "grid_shape_compose",
            "grid_shape_status",
            "grid_shape_apply",
            "grid_shape_undo",
        }:
            from bitwig_mcp_server.grid_workflow import get_grid_shape_manager

            manager = get_grid_shape_manager(controller)
            if name == "grid_shape_start":
                result = manager.start(
                    controller,
                    brief=arguments.get("brief", ""),
                    preset=arguments.get("preset"),
                    intensity=arguments.get("intensity"),
                    controls=arguments.get("controls"),
                    style=arguments.get("style"),
                )
            elif name == "grid_shape_compose":
                result = manager.compose(
                    controller,
                    arguments.get("session_id", ""),
                    preset=arguments.get("preset"),
                    intensity=arguments.get("intensity"),
                    controls=arguments.get("controls"),
                    style=arguments.get("style"),
                )
            elif name == "grid_shape_status":
                result = manager.status(controller, arguments.get("session_id", ""))
            elif name == "grid_shape_apply":
                result = manager.apply(
                    controller,
                    arguments.get("session_id", ""),
                    arguments.get("revision"),
                    arguments.get("confirm") is True
                    or arguments.get("cooperative") is True,
                )
            else:
                result = manager.undo(controller, arguments.get("session_id", ""))
            return [TextContent(type="text", text=json.dumps(result, sort_keys=True))]

        elif name == "grid_insert_device":
            if not _mutation_is_authorized(arguments):
                raise ValueError(
                    "confirm must be true unless cooperative work is authorized"
                )
            position = arguments.get("position")
            device_id = arguments.get("device_id")
            if position not in {"before", "after"}:
                raise ValueError("position must be before or after")
            if not isinstance(device_id, str) or not device_id.strip():
                raise ValueError("device_id must be a non-empty UUID string")
            result = controller.grid_insert_device(position, device_id)
            return [TextContent(type="text", text=json.dumps(result, sort_keys=True))]

        elif name == "grid_project_undo":
            result = controller.grid_undo()
            return [TextContent(type="text", text=json.dumps(result, sort_keys=True))]

        elif name == "grid_project_redo":
            result = controller.grid_redo()
            return [TextContent(type="text", text=json.dumps(result, sort_keys=True))]

        elif name == "grid_navigate_device":
            direction = arguments.get("direction")
            if direction not in {"next", "previous", "parent"}:
                raise ValueError("direction must be next, previous, or parent")
            result = controller.grid_navigate(direction)
            return [TextContent(type="text", text=json.dumps(result, sort_keys=True))]

        elif name == "grid_list_tracks":
            result = controller.grid_tracks()
            return [TextContent(type="text", text=json.dumps(result, sort_keys=True))]

        elif name == "grid_select_track":
            track_index = arguments.get("track_index")
            if (
                isinstance(track_index, bool)
                or not isinstance(track_index, int)
                or not 0 <= track_index <= 15
            ):
                raise ValueError("track_index must be an integer between 0 and 15")
            result = controller.grid_select_track(track_index)
            return [TextContent(type="text", text=json.dumps(result, sort_keys=True))]

        elif name == "set_selected_device_parameters":
            parameters = arguments.get("parameters")
            if not isinstance(parameters, dict) or not parameters:
                raise ValueError("parameters must be a non-empty object")
            normalized = {}
            for index, value in parameters.items():
                try:
                    normalized[int(index)] = value
                except (TypeError, ValueError) as exc:
                    raise ValueError("Parameter indexes must be integers") from exc
            changed = controller.set_selected_device_parameters(normalized)
            return [
                TextContent(
                    type="text",
                    text=json.dumps({"changed": changed}, sort_keys=True),
                )
            ]

        elif name == "save_parameter_snapshot":
            snapshot = controller.save_parameter_snapshot(arguments.get("name", ""))
            return [TextContent(type="text", text=json.dumps(snapshot, sort_keys=True))]

        elif name == "compare_parameter_snapshots":
            comparison = controller.compare_parameter_snapshots(
                arguments.get("first", ""), arguments.get("second", "")
            )
            return [
                TextContent(type="text", text=json.dumps(comparison, sort_keys=True))
            ]

        elif name == "apply_parameter_snapshot":
            changed = controller.apply_parameter_snapshot(arguments.get("name", ""))
            return [
                TextContent(
                    type="text",
                    text=json.dumps({"changed": changed}, sort_keys=True),
                )
            ]


        else:
            raise ValueError(f"Unknown tool: {name}")

    except Exception as e:
        logger.exception(f"Error executing tool {name}: {e}")
        return [TextContent(type="text", text=f"Error: {e!s}")]
