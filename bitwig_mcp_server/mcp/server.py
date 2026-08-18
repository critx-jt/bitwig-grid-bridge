"""
Bitwig MCP Server

Implementation of the Model Context Protocol server for Bitwig Studio integration.
"""

import asyncio
import logging
from typing import Any, List, Optional

from mcp.server import Server as MCPServer
from mcp.server.stdio import stdio_server
from mcp.types import TextContent

from bitwig_mcp_server.osc.controller import BitwigOSCController
from bitwig_mcp_server.settings import Settings

# Set up logging
logger = logging.getLogger(__name__)


class BitwigMCPServer:
    """MCP server for Bitwig Studio integration"""

    def __init__(self, settings: Optional[Settings] = None):
        """Initialize the Bitwig MCP server

        Args:
            settings: Application settings (uses default Settings if not provided)
        """
        # Use provided settings or create default
        self.settings = settings or Settings()

        # Create the MCP server
        self.mcp_server: MCPServer = MCPServer(
            f"bitwig-grid-bridge-{self.settings.app_name}"
        )

        self.controller = BitwigOSCController(
            self.settings.bitwig_host,
            self.settings.bitwig_send_port,
            self.settings.bitwig_receive_port,
            bridge_enabled=self.settings.grid_bridge_enabled,
            bridge_host=self.settings.grid_bridge_host,
            bridge_port=self.settings.grid_bridge_port,
        )

        # Set up handlers
        self._setup_handlers()

    def _setup_handlers(self) -> None:
        """Set up MCP server handlers"""
        self.mcp_server.list_tools()(self.list_tools)
        self.mcp_server.call_tool()(self.call_tool)

    async def start(self) -> None:
        """Start the Bitwig MCP server"""
        try:
            # Start the OSC controller
            self.controller.start()

            # Wait for controller to be ready
            wait_count = 0
            max_wait_count = 50  # 5 seconds
            while not self.controller.ready and wait_count < max_wait_count:
                await asyncio.sleep(0.1)
                wait_count += 1

            if not self.controller.ready:
                logger.error("Bitwig OSC controller failed to become ready in time")
                raise RuntimeError("Bitwig OSC controller failed to initialize")

            logger.info(f"Bitwig Grid Bridge MCP started - hosting {self.settings.app_name}")
        except Exception as e:
            logger.exception(f"Failed to start Bitwig Grid Bridge MCP: {e}")
            await self.stop()
            raise

    async def stop(self) -> None:
        """Stop the Bitwig MCP server"""
        try:
            if hasattr(self, "controller"):
                self.controller.stop()
            logger.info("Bitwig Grid Bridge MCP stopped")
        except Exception as e:
            logger.exception(f"Error while stopping Bitwig Grid Bridge MCP: {e}")

    async def list_tools(self) -> List[Any]:
        """List available Bitwig tools"""
        from bitwig_mcp_server.mcp.tools import get_bitwig_tools

        return get_bitwig_tools()

    async def call_tool(
        self, name: str, arguments: dict[str, Any]
    ) -> List[TextContent]:
        """Call a Bitwig tool

        Args:
            name: Tool name to call
            arguments: Arguments for the tool

        Returns:
            Result from the tool execution

        Raises:
            ValueError: If tool name is unknown or arguments are invalid
        """
        try:
            from bitwig_mcp_server.mcp.tools import execute_tool

            return await execute_tool(self.controller, name, arguments)
        except Exception as e:
            logger.exception(f"Error calling tool {name}: {e}")
            return [TextContent(type="text", text=f"Error: {e!s}")]



async def run_server(settings: Optional[Settings] = None) -> None:
    """Run the Bitwig MCP server

    Args:
        settings: Optional custom settings
    """
    server = BitwigMCPServer(settings)
    try:

        await server.start()

        # Serve the MCP protocol over stdio.  Keeping the process alive
        # without reading stdin makes MCP clients wait indefinitely during
        # initialization.
        async with stdio_server() as (read_stream, write_stream):
            await server.mcp_server.run(
                read_stream,
                write_stream,
                server.mcp_server.create_initialization_options(),
            )
    except asyncio.CancelledError:
        pass
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
    finally:
        await server.stop()
