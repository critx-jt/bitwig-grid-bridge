"""
Bitwig OSC Controller

High-level controller that combines client and server functionality
"""

import logging
import socket
import time
from typing import Any, Dict, List, Optional

from bitwig_mcp_server.bridge import GridBridgeClient, GridBridgeError

from .client import BitwigOSCClient
from .error_handler import ErrorHandler
from .exceptions import (
    BitwigNotRespondingError,
    ConnectionError,
    ResourceNotFoundError,
    TimeoutError,
)
from .server import BitwigOSCServer

logger = logging.getLogger(__name__)


class BitwigOSCController:
    """Controller for bidirectional OSC communication with Bitwig Studio"""

    def __init__(
        self,
        ip: str = "127.0.0.1",
        send_port: int = 8000,
        receive_port: int = 9000,
        connection_timeout: float = 10.0,
        reconnect_attempts: int = 5,
        bridge_enabled: bool = False,
        bridge_host: str = "127.0.0.1",
        bridge_port: int = 8765,
    ):
        """Initialize the controller

        Args:
            ip: IP address of Bitwig instance
            send_port: Port to send messages to
            receive_port: Port to receive messages on
            connection_timeout: Timeout for initial connection in seconds
            reconnect_attempts: Number of reconnection attempts
        """
        self.ip = ip
        self.send_port = send_port
        self.receive_port = receive_port
        self.connection_timeout = connection_timeout
        self.reconnect_attempts = reconnect_attempts

        # Create client and server
        self.client = BitwigOSCClient(ip, send_port)
        self.server = BitwigOSCServer(ip, receive_port)

        # Create error handler
        self.error_handler = ErrorHandler()

        # Controller state
        self.ready = False
        self.connected = False
        self.last_refresh = 0.0
        self.connection_attempts = 0
        self.parameter_snapshots: Dict[str, Dict[str, Any]] = {}
        # In-memory snapshots are intentionally process-local. They provide
        # safe comparison/apply workflows for the OSC parameter surface;
        # Grid topology is read and mutated through the bridge graph API.
        self.bridge: GridBridgeClient | None = (
            GridBridgeClient(bridge_host, bridge_port) if bridge_enabled else None
        )
        self.bridge_available = False

    def start(self) -> None:
        """Start the OSC controller.

        OSC over UDP is connectionless: successfully binding the receive
        socket is the only connection check available at startup.  Bitwig's
        built-in OSC controller does not acknowledge ``/refresh`` requests,
        so waiting for a response here makes a healthy setup time out.

        Raises:
            ConnectionError: If the local OSC receive socket cannot start.
        """
        try:
            # Start the OSC server before sending the initial state request so
            # any unsolicited state messages are captured.
            self.server.start()
            time.sleep(0.1)

            # This is best-effort initialization, not a handshake.  Bitwig
            # may ignore /refresh while still accepting all control messages.
            self.client.refresh()
            if self.bridge is not None:
                self.bridge_available = self.bridge.ping()
                if self.bridge_available:
                    logger.info(
                        "Bitwig Grid bridge detected; selected-device operations will prefer it"
                    )
                else:
                    logger.info("Bitwig Grid bridge unavailable; using OSC fallback")

            self.ready = True
            self.connected = True
            self.connection_attempts = 0
            self.error_handler.record_success()

            logger.info(
                f"OSC controller listening for Bitwig at "
                f"{self.ip}:{self.receive_port}; sending to "
                f"{self.ip}:{self.send_port}"
            )

        except Exception as e:
            self.ready = False
            self.connected = False

            try:
                self.server.stop()
            except Exception:
                pass

            error = ConnectionError(details=str(e))
            self.error_handler.record_error("start", error)
            raise error

    def _connect_with_timeout(self) -> None:
        """Attempt to connect to Bitwig with timeout

        Raises:
            ConnectionError: If unable to connect to Bitwig
            TimeoutError: If connection times out
        """
        start_time = time.time()
        self.connection_attempts += 1

        # Send ping to check if Bitwig is responding
        try:
            # Request initial state from Bitwig
            self.client.refresh()

            # Wait for a response with timeout
            while time.time() - start_time < self.connection_timeout:
                # Check if we've received any messages
                if self.server.received_messages:
                    return

                # Wait a bit before checking again
                time.sleep(0.1)

            # If we get here, we timed out
            if self.connection_attempts < self.reconnect_attempts:
                logger.warning(
                    f"Connection attempt {self.connection_attempts} timed out, retrying..."
                )
                return self._connect_with_timeout()

            raise TimeoutError("connect", self.connection_timeout)

        except socket.error as e:
            raise ConnectionError(details=f"Socket error: {e}")
        except Exception as e:
            raise ConnectionError(details=str(e))

    def stop(self) -> None:
        """Stop the controller"""
        self.ready = False
        self.connected = False
        self.server.stop()
        logger.info("OSC controller stopped")

    def __enter__(self) -> "BitwigOSCController":
        """Context manager entry"""
        self.start()
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Context manager exit"""
        self.stop()

    def ping(self, timeout: float = 2.0) -> bool:
        """Check if Bitwig is responding

        Args:
            timeout: Timeout in seconds

        Returns:
            True if Bitwig is responding, False otherwise
        """
        try:
            # Clear all messages
            self.server.clear_messages()

            # Send a query that should always return a value
            self.client.send("/refresh", 1)

            # Wait for any response
            start_time = time.time()
            while time.time() - start_time < timeout:
                if self.server.received_messages:
                    self.error_handler.record_success()
                    return True
                time.sleep(0.1)

            # If we get here, we timed out
            error = BitwigNotRespondingError()
            self.error_handler.record_error("ping", error)
            return False

        except Exception as e:
            logger.error(f"Error pinging Bitwig: {e}")
            return False

    def refresh(self, timeout: float = 2.0) -> bool:
        """Refresh state from Bitwig

        Args:
            timeout: Timeout in seconds

        Returns:
            True if successful, False otherwise
        """
        try:
            # Rate limit refreshes
            now = time.time()
            if (
                now - self.last_refresh < 0.2
            ):  # Don't refresh more than 5 times per second
                return True

            self.last_refresh = now

            # Send refresh command
            self.client.refresh()

            # Wait for any response
            start_time = time.time()
            received_count = len(self.server.received_messages)

            # Wait for new messages
            while time.time() - start_time < timeout:
                # If we've received new messages, success
                if len(self.server.received_messages) > received_count:
                    logger.debug(
                        f"Received {len(self.server.received_messages) - received_count} new messages during refresh"
                    )
                    self.error_handler.record_success()
                    return True
                time.sleep(0.1)

            # If we get here, we timed out waiting for new messages
            logger.debug(
                f"No new messages received after {timeout}s. Testing connection..."
            )

            # Explicitly test connection with a ping
            if self.ping(timeout=1.0):
                # Connection is good, Bitwig just didn't send new messages
                # This can happen when Bitwig has already sent all the state info
                # and doesn't have anything new to report
                logger.info(
                    "No new messages from Bitwig, but connection is good. Proceeding with cached state."
                )
                self.error_handler.record_success()
                return True

            # Connection test failed - we have a real problem
            logger.warning("Connection test failed after refresh timeout")
            if self.error_handler.connection_status["consecutive_timeouts"] > 3:
                error = BitwigNotRespondingError()
                self.error_handler.record_error("refresh", error)
                self.connected = False

            return False

        except Exception as e:
            logger.error(f"Error refreshing Bitwig state: {e}")
            return False

    # Synchronized command methods with response waiting
    def send_and_wait(
        self,
        address: str,
        value: Any,
        response_address: Optional[str] = None,
        timeout: float = 2.0,
    ) -> Any:
        """Send command and wait for response

        Args:
            address: The OSC address to send to
            value: The value to send
            response_address: The address to wait for (defaults to same as sent)
            timeout: Timeout in seconds

        Returns:
            The response value

        Raises:
            TimeoutError: If the operation times out
            BitwigNotRespondingError: If Bitwig is not responding
        """
        # Ensure connection is healthy
        if not self.ready or not self.connected:
            if not self._attempt_reconnect():
                raise BitwigNotRespondingError(address)

        if response_address is None:
            response_address = address

        # Define the operation to retry
        def _send_and_wait_operation() -> Any:
            # Clear any previous messages with this address
            self.server.received_messages.pop(response_address, None)

            # Send the command
            self.client.send(address, value)

            # Wait for response
            result = self.server.wait_for_message(response_address, timeout)
            if result is None:
                raise TimeoutError(f"send_and_wait({address})", timeout)
            return result

        # Retry the operation with timeout handling
        try:
            return self.error_handler.retry_with_timeout(
                _send_and_wait_operation,
                f"send_and_wait({address})",
                max_retries=2,
                retry_delay=0.2,
                timeout=timeout,
            )
        except Exception:
            # If still failing after retries, check connection
            if not self.ping():
                self.connected = False
                raise BitwigNotRespondingError(address)
            raise

    def _attempt_reconnect(self) -> bool:
        """Attempt to reconnect to Bitwig

        Returns:
            True if successful, False otherwise
        """
        if self.connection_attempts >= self.reconnect_attempts:
            logger.error("Maximum reconnection attempts reached")
            return False

        logger.info("Attempting to reconnect to Bitwig...")

        try:
            # Stop everything
            try:
                self.server.stop()
            except Exception:
                pass

            time.sleep(1.0)

            # Restart
            self.server = BitwigOSCServer(self.ip, self.receive_port)
            self.server.start()

            # Attempt connection
            self._connect_with_timeout()

            self.ready = True
            self.connected = True
            self.error_handler.record_success()

            logger.info("Successfully reconnected to Bitwig")
            return True

        except Exception as e:
            logger.error(f"Failed to reconnect: {e}")
            return False

    # High-level control methods
    def get_track_info(self, track_index: int) -> Dict[str, Any]:
        """Get information about a track

        Args:
            track_index: Track index (1-based)

        Returns:
            Dict containing track information

        Raises:
            InvalidParameterError: If track_index is invalid
            ResourceNotFoundError: If track not found
            BitwigNotRespondingError: If Bitwig is not responding
        """
        # Validate track index
        track_index = self.error_handler.validate_track_index(track_index)

        # Refresh to get latest state
        if not self.refresh():
            raise BitwigNotRespondingError(f"/track/{track_index}")

        # Check if track exists
        name = self.server.get_message(f"/track/{track_index}/name")
        if not name:
            raise ResourceNotFoundError("Track", str(track_index))

        prefix = f"/track/{track_index}/"
        track_info = {"name": name, "index": track_index}

        # Extract all track properties from received messages
        for address, value in self.server.received_messages.items():
            if address.startswith(prefix) and not address.endswith("/name"):
                # Extract property name from address
                prop = address[len(prefix) :]
                track_info[prop] = value

        return track_info

    def get_device_params(self) -> List[Dict[str, Any]]:
        """Get information about device parameters

        Returns:
            List of parameter information dictionaries

        Raises:
            ResourceNotFoundError: If no device is selected
            BitwigNotRespondingError: If Bitwig is not responding
        """
        # Refresh to get latest state
        if not self.refresh():
            raise BitwigNotRespondingError("/device")

        # Check if a device is selected
        device_exists = self.server.get_message("/device/exists")
        if not device_exists:
            raise ResourceNotFoundError("Device", "No device selected")

        params = []

        # Find all parameters
        for i in range(1, 9):  # Assuming 8 parameters max
            prefix = f"/device/param/{i}/"
            param_exists = self.server.get_message(f"{prefix}exists")

            if not param_exists:
                continue

            param_info = {"index": i}

            # Extract parameter properties
            for address, value in self.server.received_messages.items():
                if address.startswith(prefix) and not address.endswith("/exists"):
                    # Extract property name from address
                    prop = address[len(prefix) :]
                    param_info[prop] = value

            # Only add if we have some properties
            if len(param_info) > 1:
                params.append(param_info)

        return params

    def _ensure_bridge_available(self) -> bool:
        """Reconnect to a bridge that appeared after controller startup."""
        if self.bridge is None:
            return False
        if self.bridge_available:
            return True
        self.bridge_available = self.bridge.ping()
        if self.bridge_available:
            logger.info("Bitwig Grid bridge became available")
        return self.bridge_available

    def _require_bridge(self) -> GridBridgeClient:
        """Return a live bridge client or raise a transport error."""
        if not self._ensure_bridge_available() or self.bridge is None:
            raise GridBridgeError("Bitwig Grid bridge is unavailable")
        return self.bridge

    def get_selected_device_state(self) -> Dict[str, Any]:
        """Return observable state, preferring the in-process Bitwig bridge."""
        bridge = self.bridge
        if bridge is not None and self._ensure_bridge_available():
            try:
                payload = bridge.state()
                parameters = [
                    {
                        **parameter,
                        "value": parameter["value"] * 128
                        if isinstance(parameter.get("value"), (int, float))
                        else parameter.get("value"),
                    }
                    for parameter in payload.get("parameters", [])
                ]
                result = {
                    "available": bool(payload.get("exists")),
                    "graph_available": bool(payload.get("graph_available", False)),
                    "bridge": True,
                    "properties": {
                        "name": payload.get("name"),
                        "device_type": payload.get("device_type"),
                    },
                    "parameters": parameters,
                }
                if result["graph_available"]:
                    result["graph"] = bridge.graph_state()
                return result
            except GridBridgeError as error:
                logger.warning(
                    "Bitwig Grid bridge read failed; falling back to OSC: %s", error
                )
                self.bridge_available = False

        params = self.get_device_params()
        device_properties: Dict[str, Any] = {}
        prefix = "/device/"
        for address, value in self.server.received_messages.items():
            if address.startswith(prefix) and "/param/" not in address:
                property_name = address[len(prefix) :]
                if property_name not in {"exists"}:
                    device_properties[property_name] = value

        return {
            "available": True,
            "graph_available": False,
            "bridge": False,
            "properties": device_properties,
            "parameters": params,
        }

    def get_grid_capabilities(self) -> Dict[str, Any]:
        """Return bridge capabilities and selected-device inspection data."""
        if self.bridge is None:
            return {"available": False, "bridge": False, "graph_available": False}
        try:
            capabilities = self.bridge.capabilities()
            inspection = self.bridge.inspect()
            self.bridge_available = True
            return {
                "available": True,
                "bridge": True,
                "capabilities": capabilities,
                "inspection": inspection,
            }
        except GridBridgeError as error:
            self.bridge_available = False
            return {
                "available": False,
                "bridge": False,
                "graph_available": False,
                "error": str(error),
            }

    def get_grid_graph(self) -> Dict[str, Any]:
        """Return the selected Grid graph topology and editable parameters."""
        if not self._ensure_bridge_available():
            return {"available": False, "bridge": False, "graph_available": False}
        try:
            graph = self._require_bridge().graph_state()
            return {
                "available": True,
                "bridge": True,
                **graph,
            }
        except GridBridgeError as error:
            self.bridge_available = False
            return {
                "available": False,
                "bridge": False,
                "graph_available": False,
                "error": str(error),
            }

    def get_grid_host_modulators(self) -> Dict[str, Any]:
        """Return host-level modulation sources on the selected Grid device."""
        if not self._ensure_bridge_available():
            return {"available": False, "bridge": False, "sources": []}
        try:
            return {
                "available": True,
                "bridge": True,
                **self._require_bridge().graph_host_modulators(),
            }
        except GridBridgeError as error:
            self.bridge_available = False
            return {
                "available": False,
                "bridge": False,
                "sources": [],
                "error": str(error),
            }

    def search_grid_modules(self, query: str = "") -> Dict[str, Any]:
        """Search the installed Bitwig Grid module catalog."""
        if not self._ensure_bridge_available():
            return {"available": False, "bridge": False, "modules": []}
        try:
            return self._require_bridge().graph_catalog(query)
        except GridBridgeError as error:
            self.bridge_available = False
            return {
                "available": False,
                "bridge": False,
                "modules": [],
                "error": str(error),
            }

    def search_grid_modulators(self, query: str = "") -> Dict[str, Any]:
        """Search the installed Grid modulation source and destination catalog."""
        if not self._ensure_bridge_available():
            return {"available": False, "bridge": False, "modulators": []}
        try:
            return self._require_bridge().graph_modulators(query)
        except GridBridgeError as error:
            self.bridge_available = False
            return {
                "available": False,
                "bridge": False,
                "modulators": [],
                "error": str(error),
            }

    def grid_insert_modulator(self, package_id: str, x: int, y: int) -> Dict[str, Any]:
        """Insert a cataloged Grid modulator at graph coordinates."""
        if not self._ensure_bridge_available():
            raise GridBridgeError("Bitwig Grid bridge is unavailable")
        return self._require_bridge().graph_insert_modulator(package_id, x, y)

    def grid_connect_modulator(
        self,
        source_module_id: str,
        source_port: int,
        target_module_id: str,
        target_port: int,
    ) -> Dict[str, Any]:
        """Connect a cataloged Grid modulator to a Grid input."""
        if not self._ensure_bridge_available():
            raise GridBridgeError("Bitwig Grid bridge is unavailable")
        return self._require_bridge().graph_connect_modulator(
            source_module_id,
            source_port,
            target_module_id,
            target_port,
        )

    def grid_set_modulator_parameter(
        self,
        module_id: str,
        parameter_id: str,
        value: float | int | bool,
    ) -> Dict[str, Any]:
        """Tune one parameter on a cataloged Grid modulator."""
        if not self._ensure_bridge_available():
            raise GridBridgeError("Bitwig Grid bridge is unavailable")
        return self._require_bridge().graph_set_modulator_parameter(
            module_id, parameter_id, value
        )

    def grid_insert_module(self, package_id: str, x: int, y: int) -> Dict[str, Any]:
        """Insert a Grid module at graph coordinates."""
        if not self._ensure_bridge_available():
            raise GridBridgeError("Bitwig Grid bridge is unavailable")
        return self._require_bridge().graph_insert(package_id, x, y)

    def grid_set_module_parameter(
        self, module_id: str, parameter_id: str, value: float | int | bool
    ) -> Dict[str, Any]:
        """Set one editable Grid module parameter."""
        if not self._ensure_bridge_available():
            raise GridBridgeError("Bitwig Grid bridge is unavailable")
        return self._require_bridge().graph_set_parameter(module_id, parameter_id, value)

    def grid_connect_modules(
        self,
        source_module_id: str,
        source_port: int,
        target_module_id: str,
        target_port: int,
    ) -> Dict[str, Any]:
        """Connect a Grid output port to a Grid input port."""
        if not self._ensure_bridge_available():
            raise GridBridgeError("Bitwig Grid bridge is unavailable")
        return self._require_bridge().graph_connect(
            source_module_id, source_port, target_module_id, target_port
        )

    def grid_disconnect_module(
        self, target_module_id: str, target_port: int
    ) -> Dict[str, Any]:
        """Disconnect a Grid input port."""
        if not self._ensure_bridge_available():
            raise GridBridgeError("Bitwig Grid bridge is unavailable")
        return self._require_bridge().graph_disconnect(target_module_id, target_port)

    def grid_history(self) -> Dict[str, Any]:
        """Return Bitwig project history state from the local bridge."""
        if not self._ensure_bridge_available():
            return {"available": False, "bridge": False}
        try:
            return self._require_bridge().history()
        except GridBridgeError as error:
            self.bridge_available = False
            return {"available": False, "bridge": False, "error": str(error)}

    def grid_actions(self, filter_text: str = "") -> Dict[str, Any]:
        """List host actions exposed by the local bridge."""
        if not self._ensure_bridge_available():
            return {"available": False, "bridge": False}
        try:
            return self._require_bridge().actions(filter_text)
        except GridBridgeError as error:
            self.bridge_available = False
            return {"available": False, "bridge": False, "error": str(error)}

    def grid_invoke_action(self, action_id: str) -> Dict[str, Any]:
        """Invoke one exact Bitwig host action exposed by the bridge."""
        if not self._ensure_bridge_available():
            raise GridBridgeError("Bitwig Grid bridge is unavailable")
        return self._require_bridge().invoke_action(action_id)

    def grid_insert_device(self, position: str, device_id: str) -> Dict[str, Any]:
        """Insert a Bitwig device through the local bridge."""
        if not self._ensure_bridge_available():
            raise GridBridgeError("Bitwig Grid bridge is unavailable")
        return self._require_bridge().insert_device(position, device_id)

    def grid_undo(self) -> Dict[str, Any]:
        """Undo the latest Bitwig host operation."""
        if not self._ensure_bridge_available():
            raise GridBridgeError("Bitwig Grid bridge is unavailable")
        return self._require_bridge().undo()

    def grid_redo(self) -> Dict[str, Any]:
        """Redo the latest Bitwig host operation."""
        if not self._ensure_bridge_available():
            raise GridBridgeError("Bitwig Grid bridge is unavailable")
        return self._require_bridge().redo()

    def grid_navigate(self, direction: str) -> Dict[str, Any]:
        """Navigate the selected device through the local bridge."""
        if not self._ensure_bridge_available():
            raise GridBridgeError("Bitwig Grid bridge is unavailable")
        return self._require_bridge().navigate(direction)

    def grid_tracks(self) -> Dict[str, Any]:
        """List the live main-track bank exposed by the local bridge."""
        if not self._ensure_bridge_available():
            return {"available": False, "bridge": False}
        try:
            return self._require_bridge().tracks()
        except GridBridgeError as error:
            self.bridge_available = False
            return {"available": False, "bridge": False, "error": str(error)}

    def grid_select_track(self, index: int) -> Dict[str, Any]:
        """Select a main track by its zero-based live bank index."""
        if not self._ensure_bridge_available():
            raise GridBridgeError("Bitwig Grid bridge is unavailable")
        return self._require_bridge().select_track(index)

    def set_selected_device_parameters(self, parameters: Dict[int, float]) -> List[int]:
        """Set multiple selected-device parameters and return changed indexes."""
        if not parameters:
            raise ValueError("At least one parameter is required")

        for index, value in parameters.items():
            if not isinstance(index, int) or index < 1:
                raise ValueError("Parameter indexes must be positive integers")
            if not isinstance(value, (int, float)) or isinstance(value, bool):
                raise ValueError(f"Invalid value for parameter {index}")
            if value < 0 or value > 128:
                raise ValueError(
                    f"Value for parameter {index} must be between 0 and 128"
                )

        if self._ensure_bridge_available():
            try:
                self._require_bridge().set_parameters_atomic(parameters)
                return list(parameters)
            except GridBridgeError as error:
                logger.warning(
                    "Bitwig Grid bridge write failed; falling back to OSC: %s", error
                )
                self.bridge_available = False

        for index, value in parameters.items():
            self.client.set_device_parameter(index, value)
        return list(parameters)

    def save_parameter_snapshot(self, name: str) -> Dict[str, Any]:
        """Capture the currently observable selected-device parameter state."""
        if not name or not isinstance(name, str):
            raise ValueError("Snapshot name must be a non-empty string")
        state = self.get_selected_device_state()
        snapshot = {
            "name": name,
            "parameters": {
                str(parameter["index"]): parameter.get("value")
                for parameter in state["parameters"]
                if "value" in parameter
            },
        }
        self.parameter_snapshots[name] = snapshot
        return snapshot

    def compare_parameter_snapshots(self, first: str, second: str) -> Dict[str, Any]:
        """Compare two saved snapshots by parameter index."""
        try:
            left = self.parameter_snapshots[first]["parameters"]
            right = self.parameter_snapshots[second]["parameters"]
        except KeyError as exc:
            raise ValueError(f"Unknown parameter snapshot: {exc.args[0]}") from exc

        indexes = sorted(set(left) | set(right), key=int)
        changed = [
            {
                "index": int(index),
                "before": left.get(index),
                "after": right.get(index),
            }
            for index in indexes
            if left.get(index) != right.get(index)
        ]
        return {
            "first": first,
            "second": second,
            "changed": changed,
            "identical": not changed,
        }

    def apply_parameter_snapshot(self, name: str) -> List[int]:
        """Apply a saved parameter snapshot to the selected device."""
        try:
            values = self.parameter_snapshots[name]["parameters"]
        except KeyError as exc:
            raise ValueError(f"Unknown parameter snapshot: {exc.args[0]}") from exc
        return self.set_selected_device_parameters(
            {int(index): value for index, value in values.items() if value is not None}
        )

    def get_status(self) -> Dict[str, Any]:
        """Get controller status information

        Returns:
            Dict with status information
        """
        connection_health = self.error_handler.check_connection_health()

        # If connection doesn't seem healthy but we think we're connected,
        # do a quick ping test
        if not connection_health and self.connected:
            self.connected = self.ping()

        return {
            "ready": self.ready,
            "connected": self.connected,
            "ip": self.ip,
            "send_port": self.send_port,
            "receive_port": self.receive_port,
            "connection_health": connection_health,
            "errors": self.error_handler.recent_errors,
            "diagnostics": self.error_handler.get_diagnostic_info(),
        }
