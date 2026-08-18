package io.github.critxjt.bitwig.gridbridge;

import com.bitwig.extension.controller.ControllerExtension;
import com.bitwig.extension.controller.api.ControllerHost;
import com.bitwig.extension.controller.api.CursorDevice;
import com.bitwig.extension.controller.api.CursorRemoteControlsPage;
import com.bitwig.extension.controller.api.CursorDeviceFollowMode;
import com.bitwig.extension.controller.api.CursorTrack;
import com.bitwig.extension.controller.api.TrackBank;
import com.bitwig.extension.controller.api.Device;
import com.bitwig.extension.controller.api.Parameter;
import com.bitwig.extension.controller.api.Action;
import com.bitwig.extension.controller.api.Application;
import com.bitwig.extension.controller.api.Project;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.net.ServerSocket;
import java.net.Socket;
import java.nio.charset.StandardCharsets;
import java.util.Locale;
import java.util.function.Consumer;
import java.util.concurrent.Callable;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.atomic.AtomicReference;

/**
 * Local line-oriented bridge for selected-device and Grid document access.
 *
 * Stable Controller API operations and version-gated private Grid operations
 * share one host-thread scheduler and Bitwig's native undo history.
 */
public final class GridBridgeExtension extends ControllerExtension {
    private static final int PORT = 8765;
    private static final int CONTROL_COUNT = 8;

    private final ControllerHost host;
    private CursorDevice cursorDevice;
    private CursorRemoteControlsPage remotePage;
    private Application application;
    private Project project;
    private CursorTrack cursorTrack;
    private TrackBank trackBank;
    private ServerSocket serverSocket;
    private ExecutorService clients;
    private Thread acceptThread;

    GridBridgeExtension(GridBridgeExtensionDefinition definition, ControllerHost host) {
        super(definition, host);
        this.host = host;
    }

    @Override
    public void init() {
        cursorTrack = host.createCursorTrack(
                "BitwigGridBridgeTrack", "Bitwig Grid Bridge cursor", 0, 0, true);
        trackBank = host.createMainTrackBank(16, 0, 0);
        for (int i = 0; i < trackBank.getCapacityOfBank(); i++) {
            trackBank.getItemAt(i).exists().markInterested();
            trackBank.getItemAt(i).name().markInterested();
        }
        cursorDevice = cursorTrack.createCursorDevice(
                "BitwigGridBridgeDevice", "Bitwig Grid Bridge device", 0,
                CursorDeviceFollowMode.FOLLOW_SELECTION);
        try {
            Device primaryDevice = cursorTrack.getPrimaryDevice();
            if (primaryDevice != null) {
                cursorDevice.selectDevice(primaryDevice);
            }
        } catch (RuntimeException error) {
            host.println("Bitwig Grid Bridge could not pin the initial device: " + error);
        }
        application = host.createApplication();
        project = host.getProject();
        application.projectName().markInterested();
        application.panelLayout().markInterested();
        application.canUndo().markInterested();
        application.canRedo().markInterested();
        project.isModified().markInterested();
        remotePage = cursorDevice.createCursorRemoteControlsPage(CONTROL_COUNT);
        cursorDevice.name().markInterested();
        cursorDevice.deviceType().markInterested();
        cursorDevice.exists().markInterested();
        cursorDevice.isPlugin().markInterested();
        cursorDevice.isNested().markInterested();
        cursorDevice.hasLayers().markInterested();
        cursorDevice.hasDrumPads().markInterested();
        cursorDevice.hasSlots().markInterested();
        cursorDevice.slotNames().markInterested();
        for (int i = 0; i < CONTROL_COUNT; i++) {
            Parameter parameter = remotePage.getParameter(i);
            parameter.exists().markInterested();
            parameter.name().markInterested();
            parameter.value().markInterested();
            parameter.displayedValue().markInterested();
        }

        clients = Executors.newCachedThreadPool(r -> {
            Thread thread = new Thread(r, "bitwig-grid-bridge-client");
            thread.setDaemon(true);
            return thread;
        });
        try {
            serverSocket = new ServerSocket(PORT, 16, java.net.InetAddress.getLoopbackAddress());
        } catch (IOException error) {
            host.errorln("Bitwig Grid Bridge could not bind 127.0.0.1:" + PORT + ": " + error);
            return;
        }
        acceptThread = new Thread(this::acceptClients, "bitwig-grid-bridge-accept");
        acceptThread.setDaemon(true);
        acceptThread.start();
        host.println("Bitwig Grid Bridge listening on 127.0.0.1:" + PORT);
    }

    private void acceptClients() {
        while (serverSocket != null && !serverSocket.isClosed()) {
            try {
                Socket socket = serverSocket.accept();
                clients.submit(() -> serve(socket));
            } catch (IOException error) {
                if (serverSocket != null && !serverSocket.isClosed()) {
                    host.errorln("Bitwig Grid Bridge accept failed: " + error);
                }
            }
        }
    }

    private void serve(Socket socket) {
        try (socket;
             BufferedReader reader = new BufferedReader(new InputStreamReader(
                     socket.getInputStream(), StandardCharsets.UTF_8));
             BufferedWriter writer = new BufferedWriter(new OutputStreamWriter(
                     socket.getOutputStream(), StandardCharsets.UTF_8))) {
            String line;
            while ((line = reader.readLine()) != null) {
                writer.write(handle(line));
                writer.newLine();
                writer.flush();
            }
        } catch (IOException error) {
            host.println("Bitwig Grid Bridge client closed: " + error.getMessage());
        }
    }

    private String handle(String command) {
        String[] parts = command.trim().split("\\s+");
        if (parts.length == 0 || parts[0].isEmpty()) {
            return error("empty command");
        }
        try {
            return switch (parts[0].toLowerCase(Locale.ROOT)) {
                case "state" -> state();
                case "set" -> {
                    require(parts, 3);
                    int index = Integer.parseInt(parts[1]);
                    double value = Double.parseDouble(parts[2]);
                    set(index, value);
                    yield "{\"ok\":true,\"changed\":[" + index + "]}";
                }
                case "history" -> history();
                case "actions" -> actions(parts);
                case "action" -> invokeAction(parts);
                case "insert" -> insertDevice(parts);
                case "undo" -> { runOnHost(() -> { application.undo(); return null; }); yield "{\"ok\":true}"; }
                case "redo" -> { runOnHost(() -> { application.redo(); return null; }); yield "{\"ok\":true}"; }
                case "capabilities" -> capabilities();
                case "inspect" -> inspect();
                case "graph-capabilities" ->
                        runOnHost(() -> GridGraphAccess.capabilities(cursorDevice));
                case "graph-state" -> runOnHost(() -> GridGraphAccess.snapshot(cursorDevice));
                case "graph-clear" -> graphClear();
                case "graph-modulators" -> graphModulators(parts);
                case "graph-host-modulators" ->
                        runOnHost(() -> GridGraphAccess.hostModulators(cursorDevice));
                case "graph-insert-modulator" -> graphInsertModulator(parts);
                case "graph-connect-modulator" -> graphConnectModulator(parts);
                case "graph-set-modulator" -> graphSetModulator(parts);
                case "graph-catalog" -> graphCatalog(parts);
                case "graph-insert" -> graphInsert(parts);
                case "graph-move" -> graphMove(parts);
                case "graph-set" -> graphSetParameter(parts);
                case "graph-connect" -> graphConnect(parts);
                case "graph-disconnect" -> graphDisconnect(parts);
                case "batch" -> batch(parts);
                case "tracks" -> tracks();
                case "track" -> track(parts);
                case "track-first" -> runOnHost(() -> {
                    cursorTrack.selectChannel(trackBank.getItemAt(0));
                    return "{\"ok\":true,\"selection\":\"track-first\"}";
                });
                case "track-next" -> runOnHost(() -> {
                    cursorTrack.selectNext();
                    return "{\"ok\":true,\"selection\":\"track-next\"}";
                });
                case "track-previous" -> runOnHost(() -> {
                    cursorTrack.selectPrevious();
                    return "{\"ok\":true,\"selection\":\"track-previous\"}";
                });
                case "device-first" -> runOnHost(() -> {
                    cursorDevice.selectFirst();
                    return "{\"ok\":true,\"selection\":\"device-first\"}";
                });
                case "device-primary" -> runOnHost(() -> {
                    com.bitwig.extension.controller.api.Device device = cursorTrack.getPrimaryDevice();
                    if (device == null) {
                        throw new IllegalStateException("cursor track has no primary device");
                    }
                    cursorDevice.selectDevice(device);
                    return "{\"ok\":true,\"selection\":\"device-primary\"}";
                });
                case "device-editor" -> runOnHost(() -> {
                    cursorDevice.selectInEditor();
                    return "{\"ok\":true,\"selection\":\"device-editor\"}";
                });
                case "next" -> runOnHost(() -> { cursorDevice.selectNext(); return "{\"ok\":true}"; });
                case "previous" -> runOnHost(() -> { cursorDevice.selectPrevious(); return "{\"ok\":true}"; });
                case "parent" -> runOnHost(() -> { cursorDevice.selectParent(); return "{\"ok\":true}"; });
                case "ping" -> "{\"ok\":true,\"bridge\":\"bitwig-grid-bridge\"}";
                default -> error("unknown command: " + parts[0]);
            };
        } catch (IllegalArgumentException error) {
            return error(error.getMessage());
        } catch (RuntimeException error) {
            host.errorln("Bitwig Grid Bridge command failed: " + error);
            return error(error.toString());
        }
    }
    private String capabilities() {
        return runOnHost(() -> {
            String graph = GridGraphAccess.capabilities(cursorDevice);
            boolean graphAvailable = graph.contains("\"graph_available\":true");
            return "{\"ok\":true,\"protocol\":3,\"graph_available\":"
                    + graphAvailable
                    + ",\"selected_device\":true,\"remote_controls\":true"
                    + ",\"container_inspection\":true,\"batch_writes\":true"
                    + ",\"host_thread_scheduling\":true,\"application_actions\":true"
                    + ",\"device_insertion\":true,\"undo_redo\":true"
                    + ",\"max_remote_controls\":" + CONTROL_COUNT
                    + ",\"grid_graph\":" + graph + "}";
        });
    }

    private String history() {
        return runOnHost(() -> "{\"ok\":true"
                + ",\"project_name\":" + json(application.projectName().get())
                + ",\"project_modified\":" + project.isModified().get()
                + ",\"can_undo\":" + application.canUndo().get()
                + ",\"can_redo\":" + application.canRedo().get()
                + ",\"panel_layout\":" + json(application.panelLayout().get())
                + "}");
    }

    private String tracks() {
        return runOnHost(() -> {
            StringBuilder result = new StringBuilder("{\"ok\":true,\"tracks\":[");
            boolean first = true;
            for (int i = 0; i < trackBank.getCapacityOfBank(); i++) {
                var track = trackBank.getItemAt(i);
                if (!track.exists().get()) {
                    continue;
                }
                if (!first) {
                    result.append(',');
                }
                first = false;
                result.append("{\"index\":").append(i);
                result.append(",\"name\":").append(json(track.name().get())).append('}');
            }
            return result.append("]}").toString();
        });
    }

    private String track(String[] parts) {
        require(parts, 2);
        int index = Integer.parseInt(parts[1]);
        if (index < 0 || index >= trackBank.getCapacityOfBank()) {
            throw new IllegalArgumentException("track index is outside the main track bank");
        }
        return runOnHost(() -> {
            var selected = trackBank.getItemAt(index);
            if (!selected.exists().get()) {
                throw new IllegalArgumentException("track does not exist: " + index);
            }
            cursorTrack.selectChannel(selected);
            return "{\"ok\":true,\"selection\":\"track\",\"index\":" + index
                    + ",\"name\":" + json(selected.name().get()) + "}";
        });
    }
    private String graphCatalog(String[] parts) {
        String query = null;
        if (parts.length > 1) {
            StringBuilder joined = new StringBuilder(parts[1]);
            for (int i = 2; i < parts.length; i++) {
                joined.append(' ').append(parts[i]);
            }
            query = joined.toString();
        }
        String finalQuery = query;
        return runOnHost(() -> GridGraphAccess.catalog(finalQuery));
    }
    private String graphModulators(String[] parts) {
        String query = null;
        if (parts.length > 1) {
            StringBuilder joined = new StringBuilder(parts[1]);
            for (int i = 2; i < parts.length; i++) {
                joined.append(' ').append(parts[i]);
            }
            query = joined.toString();
        }
        String finalQuery = query;
        return runOnHost(() -> GridGraphAccess.modulatorCatalog(finalQuery));
    }

    private String graphInsertModulator(String[] parts) {
        require(parts, 4);
        java.util.UUID moduleId;
        try {
            moduleId = java.util.UUID.fromString(parts[1]);
        } catch (IllegalArgumentException error) {
            throw new IllegalArgumentException("modulator package id must be a UUID", error);
        }
        int x = Integer.parseInt(parts[2]);
        int y = Integer.parseInt(parts[3]);
        if (Math.abs(x) > 4096 || Math.abs(y) > 4096) {
            throw new IllegalArgumentException("Grid coordinates must be between -4096 and 4096");
        }
        return awaitGraphMutation(
                "loading the Grid modulator",
                completion -> GridGraphAccess.insertModulator(
                        cursorDevice, moduleId, x, y, completion));
    }

    private String graphConnectModulator(String[] parts) {
        require(parts, 5);
        String sourceModule = parts[1];
        int sourcePort = Integer.parseInt(parts[2]);
        String targetModule = parts[3];
        int targetPort = Integer.parseInt(parts[4]);
        return awaitGraphMutation(
                "connecting the Grid modulator",
                completion -> GridGraphAccess.connectModulator(
                        cursorDevice,
                        sourceModule,
                        sourcePort,
                        targetModule,
                        targetPort,
                        completion));
    }
    private String graphSetModulator(String[] parts) {
        require(parts, 4);
        return awaitGraphMutation(
                "tuning a Grid modulator",
                completion -> GridGraphAccess.setModulatorParameter(
                        cursorDevice, parts[1], parts[2], parts[3], completion));
    }

    private String graphInsert(String[] parts) {
        require(parts, 4);
        java.util.UUID moduleId;
        try {
            moduleId = java.util.UUID.fromString(parts[1]);
        } catch (IllegalArgumentException error) {
            throw new IllegalArgumentException("module package id must be a UUID", error);
        }
        int x = Integer.parseInt(parts[2]);
        int y = Integer.parseInt(parts[3]);
        if (Math.abs(x) > 4096 || Math.abs(y) > 4096) {
            throw new IllegalArgumentException("Grid coordinates must be between -4096 and 4096");
        }
        return awaitGraphMutation(
                "loading the Grid module",
                completion -> GridGraphAccess.insert(
                        cursorDevice, moduleId, x, y, completion));
    }

    private String graphMove(String[] parts) {
        require(parts, 4);
        int x = Integer.parseInt(parts[2]);
        int y = Integer.parseInt(parts[3]);
        if (Math.abs(x) > 4096 || Math.abs(y) > 4096) {
            throw new IllegalArgumentException("Grid coordinates must be between -4096 and 4096");
        }
        return awaitGraphMutation(
                "moving a Grid module",
                completion -> GridGraphAccess.move(cursorDevice, parts[1], x, y, completion));
    }

    private String graphClear() {
        return awaitGraphMutation(
                "clearing the Grid graph",
                completion -> GridGraphAccess.clear(cursorDevice, completion));
    }


    private String graphSetParameter(String[] parts) {
        require(parts, 4);
        return awaitGraphMutation(
                "setting a Grid parameter",
                completion -> GridGraphAccess.setParameter(
                        cursorDevice, parts[1], parts[2], parts[3], completion));
    }

    private String graphConnect(String[] parts) {
        require(parts, 5);
        String sourceModule = parts[1];
        int sourcePort = Integer.parseInt(parts[2]);
        String targetModule = parts[3];
        int targetPort = Integer.parseInt(parts[4]);
        return awaitGraphMutation(
                "connecting Grid ports",
                completion -> GridGraphAccess.connect(
                        cursorDevice,
                        sourceModule,
                        sourcePort,
                        targetModule,
                        targetPort,
                        completion));
    }

    private String graphDisconnect(String[] parts) {
        require(parts, 3);
        String targetModule = parts[1];
        int targetPort = Integer.parseInt(parts[2]);
        return awaitGraphMutation(
                "disconnecting Grid ports",
                completion -> GridGraphAccess.disconnect(
                        cursorDevice, targetModule, targetPort, completion));
    }
    private String awaitGraphMutation(
            String description,
            Consumer<Consumer<String>> start) {
        AtomicReference<String> response = new AtomicReference<>();
        CountDownLatch completed = new CountDownLatch(1);
        runOnHost(() -> {
            start.accept(value -> {
                if (response.compareAndSet(null, value)) {
                    completed.countDown();
                }
            });
            return null;
        });
        try {
            if (!completed.await(10, TimeUnit.SECONDS)) {
                throw new IllegalStateException("Timed out " + description);
            }
        } catch (InterruptedException error) {
            Thread.currentThread().interrupt();
            throw new IllegalStateException("Interrupted " + description, error);
        }
        return response.get();
    }



    private String actions(String[] parts) {
        String filter = parts.length > 1 ? parts[1].toLowerCase(Locale.ROOT) : "";
        return runOnHost(() -> {
            StringBuilder result = new StringBuilder("{\"ok\":true,\"actions\":[");
            boolean first = true;
            for (Action action : application.getActions()) {
                String id = action.getId();
                String name = action.getName();
                String menu = action.getMenuItemText();
                String searchable = (id + " " + name + " " + menu).toLowerCase(Locale.ROOT);
                if (!filter.isEmpty() && !searchable.contains(filter)) continue;
                if (!first) result.append(',');
                first = false;
                result.append("{\"id\":").append(json(id));
                result.append(",\"name\":").append(json(name));
                result.append(",\"menu\":").append(json(menu)).append('}');
            }
            return result.append("]}").toString();
        });
    }

    private String invokeAction(String[] parts) {
        require(parts, 2);
        String id = parts[1];
        return runOnHost(() -> {
            Action action = application.getAction(id);
            if (action == null) throw new IllegalArgumentException("unknown action: " + id);
            action.invoke();
            return "{\"ok\":true,\"action\":" + json(id) + "}";
        });
    }


    private String insertDevice(String[] parts) {
        require(parts, 3);
        String position = parts[1].toLowerCase(Locale.ROOT);
        if (!position.equals("before") && !position.equals("after")) {
            throw new IllegalArgumentException("position must be before or after");
        }
        java.util.UUID deviceId;
        try {
            deviceId = java.util.UUID.fromString(parts[2]);
        } catch (IllegalArgumentException error) {
            throw new IllegalArgumentException("device id must be a UUID", error);
        }
        return runOnHost(() -> {
            if (position.equals("before")) {
                cursorDevice.beforeDeviceInsertionPoint().insertBitwigDevice(deviceId);
            } else {
                cursorDevice.afterDeviceInsertionPoint().insertBitwigDevice(deviceId);
            }
            return "{\"ok\":true,\"position\":" + json(position)
                    + ",\"device_id\":" + json(deviceId.toString()) + "}";
        });
    }

    private String inspect() {
        return runOnHost(() -> {
            StringBuilder result = new StringBuilder("{\"ok\":true");
            result.append(",\"exists\":").append(cursorDevice.exists().get());
            result.append(",\"name\":").append(json(cursorDevice.name().get()));
            result.append(",\"device_type\":").append(json(cursorDevice.deviceType().get()));
            result.append(",\"is_plugin\":").append(cursorDevice.isPlugin().get());
            result.append(",\"is_nested\":").append(cursorDevice.isNested().get());
            result.append(",\"has_layers\":").append(cursorDevice.hasLayers().get());
            result.append(",\"has_drum_pads\":").append(cursorDevice.hasDrumPads().get());
            result.append(",\"has_slots\":").append(cursorDevice.hasSlots().get());
            result.append(",\"slot_names\":").append(jsonArray(cursorDevice.slotNames().get()));
            return result.append('}').toString();
        });
    }

    private String batch(String[] parts) {
        require(parts, 2);
        int[][] indexes = new int[parts.length - 1][1];
        double[][] values = new double[parts.length - 1][1];
        for (int i = 1; i < parts.length; i++) {
            String[] assignment = parts[i].split("=", 2);
            if (assignment.length != 2) {
                throw new IllegalArgumentException("batch items must use index=value");
            }
            indexes[i - 1][0] = Integer.parseInt(assignment[0]);
            values[i - 1][0] = Double.parseDouble(assignment[1]);
            validateValue(values[i - 1][0]);
        }
        return runOnHost(() -> {
            StringBuilder changed = new StringBuilder("[");
            for (int i = 0; i < indexes.length; i++) {
                if (i > 0) changed.append(',');
                setImmediate(indexes[i][0], values[i][0]);
                changed.append(indexes[i][0]);
            }
            return "{\"ok\":true,\"changed\":" + changed.append(']') + "}";
        });
    }

    private String state() {
        return runOnHost(() -> {
            StringBuilder result = new StringBuilder("{\"ok\":true,\"graph_available\":false");
            result.append(",\"exists\":").append(cursorDevice.exists().get());
            result.append(",\"name\":").append(json(cursorDevice.name().get()));
            result.append(",\"device_type\":").append(json(cursorDevice.deviceType().get()));
            result.append(",\"parameters\":[");
            for (int i = 0; i < CONTROL_COUNT; i++) {
                if (i > 0) result.append(',');
                Parameter parameter = remotePage.getParameter(i);
                result.append("{\"index\":").append(i + 1);
                result.append(",\"exists\":").append(parameter.exists().get());
                result.append(",\"name\":").append(json(parameter.name().get()));
                result.append(",\"value\":").append(parameter.value().get());
                result.append(",\"display\":").append(json(parameter.displayedValue().get()));
                result.append('}');
            }
            return result.append("]}").toString();
        });
    }

    private void set(int index, double value) {
        validateValue(value);
        runOnHost(() -> {
            setImmediate(index, value);
            return null;
        });
    }

    private void setImmediate(int index, double value) {
        if (index < 1 || index > CONTROL_COUNT) {
            throw new IllegalArgumentException("index must be 1-8");
        }
        validateValue(value);
        Parameter parameter = remotePage.getParameter(index - 1);
        if (!parameter.exists().get()) {
            throw new IllegalArgumentException("parameter does not exist");
        }
        parameter.value().setImmediately(value);
    }

    private static void validateValue(double value) {
        if (!Double.isFinite(value) || value < 0 || value > 1) {
            throw new IllegalArgumentException("value must be normalized between 0 and 1");
        }
    }

    private <T> T runOnHost(Callable<T> action) {
        CountDownLatch completed = new CountDownLatch(1);
        AtomicReference<T> result = new AtomicReference<>();
        AtomicReference<RuntimeException> failure = new AtomicReference<>();
        host.scheduleTask(() -> {
            try {
                result.set(action.call());
            } catch (Exception error) {
                failure.set(error instanceof RuntimeException runtime
                        ? runtime
                        : new RuntimeException(error));
            } finally {
                completed.countDown();
            }
        }, 0);
        try {
            if (!completed.await(2, TimeUnit.SECONDS)) {
                throw new IllegalStateException("Bitwig host task timed out");
            }
        } catch (InterruptedException error) {
            Thread.currentThread().interrupt();
            throw new IllegalStateException("Interrupted waiting for Bitwig host task", error);
        }
        if (failure.get() != null) throw failure.get();
        return result.get();
    }


    private static void require(String[] parts, int count) {
        if (parts.length < count) throw new IllegalArgumentException("missing command arguments");
    }

    private static String error(String message) {
        return "{\"ok\":false,\"error\":" + json(message == null ? "error" : message) + "}";
    }

    private static String json(String value) {
        if (value == null) return "null";
        return "\"" + value.replace("\\", "\\\\").replace("\"", "\\\"")
                .replace("\n", "\\n").replace("\r", "\\r") + "\"";
    }

    private static String jsonArray(String[] values) {
        if (values == null) return "null";
        StringBuilder result = new StringBuilder("[");
        for (int i = 0; i < values.length; i++) {
            if (i > 0) result.append(',');
            result.append(json(values[i]));
        }
        return result.append(']').toString();
    }

    @Override
    public void exit() {
        if (serverSocket != null) {
            try { serverSocket.close(); } catch (IOException ignored) { }
        }
        if (clients != null) clients.shutdownNow();
        cursorDevice = null;
        remotePage = null;
        application = null;
        project = null;
    }

    @Override
    public void flush() {
        // State is read directly from subscribed API values.
    }
}
