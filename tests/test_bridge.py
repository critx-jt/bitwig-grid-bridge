from unittest.mock import MagicMock, patch

from bitwig_mcp_server.bridge import GridBridgeClient, GridBridgeError


def test_bridge_client_state_request():
    connection = MagicMock()
    connection.__enter__.return_value = connection

    connection.makefile.return_value.readline.return_value = (
        '{"ok":true,"exists":true,"parameters":[]}'
    )
    with patch("socket.create_connection", return_value=connection) as create:
        result = GridBridgeClient().state()

    create.assert_called_once_with(("127.0.0.1", 8765), 3.0)
    connection.sendall.assert_called_once_with(b"state\n")
    assert result["exists"] is True


def test_bridge_client_atomic_parameter_batch():
    connection = MagicMock()
    connection.__enter__.return_value = connection
    connection.makefile.return_value.readline.return_value = (
        '{"ok":true,"changed":[1,2]}'
    )
    with patch("socket.create_connection", return_value=connection):
        result = GridBridgeClient().set_parameters_atomic({1: 64, 2: 32})

    assert result["changed"] == [1, 2]
    connection.sendall.assert_called_once_with(b"batch 1=0.5 2=0.25\n")

def test_bridge_client_rejects_bridge_error():
    connection = MagicMock()
    connection.__enter__.return_value = connection
    connection.makefile.return_value.readline.return_value = (
        '{"ok":false,"error":"parameter does not exist"}'
    )
    with patch("socket.create_connection", return_value=connection):
        try:
            GridBridgeClient().state()
        except GridBridgeError as error:
            assert str(error) == "parameter does not exist"
        else:
            raise AssertionError("expected GridBridgeError")
