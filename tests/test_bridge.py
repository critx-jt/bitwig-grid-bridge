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


def test_bridge_client_track_commands():
    connection = MagicMock()
    connection.__enter__.return_value = connection
    connection.makefile.return_value.readline.return_value = '{"ok":true}'

    with patch("socket.create_connection", return_value=connection):
        client = GridBridgeClient()
        client.tracks()
        client.select_track(2)

    calls = [call.args[0] for call in connection.sendall.call_args_list]
    assert calls == [b"tracks\n", b"track 2\n"]


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


def test_bridge_client_graph_commands():
    connection = MagicMock()
    connection.__enter__.return_value = connection
    connection.makefile.return_value.readline.return_value = '{"ok":true}'

    with patch("socket.create_connection", return_value=connection):
        client = GridBridgeClient()
        client.graph_state()
        client.graph_host_modulators()
        client.graph_catalog("sine")
        client.graph_modulators("lfo")
        client.graph_insert("module-uuid", 3, 2)
        client.graph_insert_modulator("modulator-uuid", 4, 5)
        client.graph_set_modulator_parameter("2", "RATE", 0.25)
        client.graph_set_parameter("2", "KEYTRACK", False)
        client.graph_connect("2", 0, "1", 0)
        client.graph_connect_modulator("2", 0, "1", 0)
        client.graph_disconnect("1", 0)

    calls = [call.args[0] for call in connection.sendall.call_args_list]
    assert b"graph-state\n" in calls
    assert b"graph-host-modulators\n" in calls
    assert b"graph-catalog sine\n" in calls
    assert b"graph-modulators lfo\n" in calls
    assert b"graph-insert module-uuid 3 2\n" in calls
    assert b"graph-insert-modulator modulator-uuid 4 5\n" in calls
    assert b"graph-set-modulator 2 RATE 0.25\n" in calls
    assert b"graph-set 2 KEYTRACK false\n" in calls
    assert b"graph-connect 2 0 1 0\n" in calls
    assert b"graph-connect-modulator 2 0 1 0\n" in calls
    assert b"graph-disconnect 1 0\n" in calls


def test_bridge_client_graph_state_exposes_parameter_metadata():
    connection = MagicMock()
    connection.__enter__.return_value = connection
    connection.makefile.return_value.readline.return_value = (
        '{"ok":true,"modules":{"items":[{"parameters":['
        '{"id":"LEVEL","type":"float","range":{"min":-1,"max":1}},'
        '{"id":"MODE","type":"integer","options":['
        '{"value":0,"label":"Off"},{"value":1,"label":"On"}]},'
        '{"id":"BYPASS","type":"boolean","options":[false,true]}'
        "] }]}}"
    )
    with patch("socket.create_connection", return_value=connection):
        result = GridBridgeClient().graph_state()

    parameters = result["modules"]["items"][0]["parameters"]
    assert parameters[0]["range"] == {"min": -1, "max": 1}
    assert parameters[1]["options"][1] == {"value": 1, "label": "On"}
    assert parameters[2]["options"] == [False, True]
