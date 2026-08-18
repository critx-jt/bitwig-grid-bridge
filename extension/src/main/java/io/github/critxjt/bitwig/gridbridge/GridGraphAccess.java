package io.github.critxjt.bitwig.gridbridge;

import com.bitwig.extension.controller.api.CursorDevice;
import com.bitwig.extension.controller.api.ModulationSource;
import java.io.File;
import java.lang.reflect.Method;
import java.lang.reflect.Modifier;
import java.lang.reflect.Proxy;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Locale;
import java.util.Set;
import java.util.UUID;
import java.util.concurrent.atomic.AtomicBoolean;
import java.util.function.Consumer;
import java.util.stream.Stream;

/**
 * Version-gated access to Bitwig's in-process Grid document model.
 *
 * The Controller API has no Grid graph surface. This adapter deliberately keeps
 * all private access reflective and reports capability failures instead of
 * pretending that remote controls are graph nodes.
 */
final class GridGraphAccess {
    private GridGraphAccess() {
    }
    private record ModulatorSpec(
            String category,
            String role,
            String guidance,
            List<String> tuningParameters,
            List<String> inputHints,
            List<String> outputHints) {
    }

    private record ModuleCatalogEntry(UUID packageId, String name) {
    }

    /**
     * Grid does not expose a stable public "modulator" type. Keep the semantic
     * catalog name-based, but always intersect it with Bitwig's current package
     * catalog before exposing or inserting an entry.
     */
    private static ModulatorSpec modulatorSpec(String name) {
        return switch (name) {
            case "AD", "ADSR", "AR" -> new ModulatorSpec(
                    "envelope",
                    "source",
                    "Envelope source. Drive GATE_IN when triggered, then route OUT or MOD_OUT to a Grid control input.",
                    List.of("ATTACK", "DECAY", "SUSTAIN", "RELEASE", "MODEL"),
                    List.of("GATE_IN", "IN"),
                    List.of("OUT", "MOD_OUT", "BIASED_OUT"));
            case "Segments" -> new ModulatorSpec(
                    "envelope",
                    "source",
                    "Multi-segment envelope. Drive GATE_IN or PHASE_IN, then route OUT or MOD_OUT to a Grid control input.",
                    List.of("RATE", "TIMEBASE", "CURVE", "GATE"),
                    List.of("PHASE_IN", "IN", "GATE_IN"),
                    List.of("OUT", "MOD_OUT"));
            case "Curves", "Slopes" -> new ModulatorSpec(
                    "periodic",
                    "source",
                    "Clocked curve source. Use RATE_IN or GATE_IN for synchronization and route OUT to a Grid control input.",
                    List.of("TIMEBASE", "RETRIGGER", "BIPOLAR"),
                    List.of("RATE_IN", "GATE_IN", "PHASE_IN"),
                    List.of("OUT"));
            case "Follower", "Follower RF" -> new ModulatorSpec(
                    "follower",
                    "source",
                    "Audio envelope follower. Feed IN from audio and route OUT to a Grid control input.",
                    List.of("TIME", "RMS", "ATTACK", "DECAY", "MODE"),
                    List.of("IN"),
                    List.of("OUT"));
            case "LFO", "S/H LFO", "Wavetable LFO" -> new ModulatorSpec(
                    "lfo",
                    "source",
                    "Low-frequency source. Tune TIMEBASE, WAVE or table input, then route OUT to a Grid control input.",
                    List.of("RATE_MOD", "TIMEBASE", "WAVE", "BIPOLAR", "RETRIGGER"),
                    List.of("RATE_IN", "GATE_IN", "PHASE_IN", "TABLE_IN"),
                    List.of("OUT"));
            case "Steps", "Scale Steps", "Step Access", "Shift Register" -> new ModulatorSpec(
                    "sequencer",
                    "source",
                    "Stepped control source. Tune step count or scale behavior and route OUT to a Grid control input.",
                    List.of("STEPS", "BIPOLAR", "INTERPOLATION", "DEVICE_PHASE"),
                    List.of("PHASE_IN", "IN"),
                    List.of("OUT"));
            case "Sample / Hold", "Dice", "Chance", "Probabilities" -> new ModulatorSpec(
                    "random",
                    "source",
                    "Random or sampled control source. Add a trigger when available and route OUT to a Grid control input.",
                    List.of("BIPOLAR", "NOTE_TRIGGER"),
                    List.of("IN", "GATE_IN"),
                    List.of("OUT"));
            case "Noise" -> new ModulatorSpec(
                    "random",
                    "source",
                    "Noise source. Tune TYPE or STEREO, then route OUT through a scaler or directly to a Grid control input.",
                    List.of("TYPE", "STEREO"),
                    List.of(),
                    List.of("OUT"));
            case "Clock", "Clock Divide", "Clock Quantize", "Gate Length", "Gate Repeat",
                    "Gates", "Triggers", "Transport", "Transport Playing" -> new ModulatorSpec(
                    "timing",
                    "source",
                    "Timing source. Use its gate or clock output to synchronize envelopes, sequencers, or Grid controls.",
                    List.of("RATE", "RETRIGGER", "TIMEBASE", "LENGTH"),
                    List.of("GATE_IN"),
                    List.of("OUT", "GATE_OUT"));
            case "Key On", "Keys Held", "Note In", "Pressure In", "Timbre In",
                    "Velocity In", "Root Key", "Voice Stack Info" -> new ModulatorSpec(
                    "note",
                    "source",
                    "Note or expression source. Route the relevant output to a Grid pitch, gate, or control input.",
                    List.of("MIDI_KEY", "MIDI_CHANNEL", "VELOCITY_MODE"),
                    List.of(),
                    List.of("OUT", "GATE_OUT", "PITCH_OUT", "VELOCITY_OUT", "PRESSURE_OUT"));
            case "Audio In", "Audio Sidechain", "CC In", "CV In", "HW In",
                    "Phase In", "Pitch In", "Select In", "Gate In" -> new ModulatorSpec(
                    "external",
                    "source",
                    "External control source. Route its output to a Grid device input or an envelope/follower input.",
                    List.of(),
                    List.of(),
                    List.of("OUT", "GATE_OUT"));
            case "Constant", "Value", "Value Scaler" -> new ModulatorSpec(
                    "utility",
                    "source",
                    "Static or scaled control source. Use it as a stable modulation baseline or range limiter.",
                    List.of("VALUE", "STEREOIZE"),
                    List.of("IN"),
                    List.of("OUT"));
            case "Modulator Out" -> new ModulatorSpec(
                    "output",
                    "sink",
                    "Modulation destination. Connect a Grid control source to IN to expose it as a Poly Grid modulator.",
                    List.of("SOURCE"),
                    List.of("IN"),
                    List.of());
            default -> null;
        };
    }

    private static List<ModuleCatalogEntry> moduleCatalogEntries()
            throws ReflectiveOperationException {
        Class<?> catalogClass = Class.forName("com.bitwig.flt.packaging.core.ytr");
        Method listMethod = catalogClass.getDeclaredMethod("FhI");
        listMethod.setAccessible(true);
        Object value = listMethod.invoke(null);
        if (!(value instanceof List<?> entries)) {
            throw new IllegalStateException("module catalog unavailable");
        }
        List<ModuleCatalogEntry> modules = new ArrayList<>();
        for (Object entry : entries) {
            Object kind = invokeNoArg(entry, "VRl");
            if (!"MODULE".equals(String.valueOf(kind))) {
                continue;
            }
            modules.add(new ModuleCatalogEntry(
                    (UUID) invokeNoArg(entry, "FhI"),
                    String.valueOf(invokeNoArg(entry, "gGl"))));
        }
        return modules;
    }

    static String modulatorCatalog(String query) {
        try {
            String needle = query == null ? "" : query.strip().toLowerCase(Locale.ROOT);
            StringBuilder json = new StringBuilder("{\"ok\":true,\"modulators\":[");
            int emitted = 0;
            for (ModuleCatalogEntry entry : moduleCatalogEntries()) {
                ModulatorSpec spec = modulatorSpec(entry.name());
                if (spec == null
                        || (!needle.isEmpty()
                        && !entry.name().toLowerCase(Locale.ROOT).contains(needle)
                        && !entry.packageId().toString().contains(needle)
                        && !spec.category().contains(needle))) {
                    continue;
                }
                if (emitted++ > 0) {
                    json.append(',');
                }
                json.append("{\"package_id\":").append(string(entry.packageId()))
                        .append(",\"name\":").append(string(entry.name()))
                        .append(",\"category\":").append(string(spec.category()))
                        .append(",\"role\":").append(string(spec.role()))
                        .append(",\"guidance\":").append(string(spec.guidance()));
                appendStringArray(json, "tuning_parameters", spec.tuningParameters());
                appendStringArray(json, "input_hints", spec.inputHints());
                appendStringArray(json, "output_hints", spec.outputHints());
                json.append('}');
            }
            return json.append("],\"count\":").append(emitted).append('}').toString();
        } catch (Throwable error) {
            return "{\"ok\":false,\"error\":" + string(rootMessage(error)) + "}";
        }
    }

    private static void appendStringArray(
            StringBuilder json,
            String key,
            List<String> values) {
        json.append(",\"").append(key).append("\":[");
        for (int i = 0; i < values.size(); i++) {
            if (i > 0) {
                json.append(',');
            }
            json.append(string(values.get(i)));
        }
        json.append(']');
    }

    private static boolean isModulatorModule(UUID moduleId) {
        try {
            return moduleCatalogEntries().stream()
                    .anyMatch(entry -> entry.packageId().equals(moduleId)
                            && modulatorSpec(entry.name()) != null);
        } catch (Throwable error) {
            return false;
        }
    }

    static void insertModulator(
            CursorDevice cursorDevice,
            UUID moduleId,
            int x,
            int y,
            Consumer<String> completion) {
        if (!isModulatorModule(moduleId)) {
            completion.accept("{\"ok\":false,\"error\":"
                    + string("unknown Grid modulator package: " + moduleId) + "}");
            return;
        }
        insert(cursorDevice, moduleId, x, y, completion, false);
    }

    static void connectModulator(
            CursorDevice cursorDevice,
            String sourceModuleId,
            int sourcePortIndex,
            String targetModuleId,
            int targetPortIndex,
            Consumer<String> completion) {
        try {
            Object graph = selectedGraph(cursorDevice);
            Object sourceModule = requireModule(graph, sourceModuleId);
            Object descriptor = invokeNoArg(sourceModule, "EGC");
            UUID packageId = UUID.fromString(
                    String.valueOf(invokeNoArg(descriptor, "bD1")));
            if (!isModulatorModule(packageId)) {
                throw new IllegalArgumentException(
                        "source module is not a supported Grid modulator: " + sourceModuleId);
            }
        } catch (Throwable error) {
            completion.accept("{\"ok\":false,\"error\":" + string(rootMessage(error)) + "}");
            return;
        }
        connect(
                cursorDevice,
                sourceModuleId,
                sourcePortIndex,
                targetModuleId,
                targetPortIndex,
                completion,
                false);
    }
    static void setModulatorParameter(
            CursorDevice cursorDevice,
            String moduleId,
            String parameterId,
            String rawValue,
            Consumer<String> completion) {
        try {
            Object graph = selectedGraph(cursorDevice);
            Object module = requireModule(graph, moduleId);
            Object descriptor = invokeNoArg(module, "EGC");
            UUID packageId = UUID.fromString(
                    String.valueOf(invokeNoArg(descriptor, "bD1")));
            if (!isModulatorModule(packageId)) {
                throw new IllegalArgumentException(
                        "module is not a supported Grid modulator: " + moduleId);
            }
        } catch (Throwable error) {
            completion.accept("{\"ok\":false,\"error\":" + string(rootMessage(error)) + "}");
            return;
        }
        setParameter(cursorDevice, moduleId, parameterId, rawValue, completion, false);
    }


    static String probe(CursorDevice cursorDevice) {
        StringBuilder json = new StringBuilder("{\"ok\":true");
        try {
            Object target = invokeNoArg(cursorDevice, "getDeepestTarget");
            if (target == null) {
                return "{\"ok\":true,\"graph_available\":false,\"reason\":\"no selected document target\"}";
            }
            json.append(",\"target_class\":").append(string(target.getClass().getName()));
            Object graph = findGraph(target);
            json.append(",\"graph_class\":").append(graph == null
                    ? "null" : string(graph.getClass().getName()));
            if (graph != null) {
                json.append(",\"modules\":").append(modules(graph));
            }
            json.append(",\"catalog\":").append(catalog(null));
            File moduleResource = resolveModuleFile(
                    UUID.fromString("ca05aebd-ecaf-4d57-b0f6-c04ce81674c4"));
            json.append(",\"module_resource\":").append(moduleResource == null
                    ? "null" : string(moduleResource.getAbsolutePath()));
            return json.append('}').toString();
        } catch (Throwable error) {
            return "{\"ok\":true,\"graph_available\":false,\"error\":"
                    + string(rootMessage(error)) + "}";
        }
    }
    static String capabilities(CursorDevice cursorDevice) {
        try {
            Object target = selectedTarget(cursorDevice);
            Object graph = findGraph(target);
            boolean graphAvailable = graph != null;
            boolean insertionAvailable = graphAvailable
                    && findInsertMethod(graph.getClass()) != null
                    && resolveModuleFile(UUID.fromString(
                            "ca05aebd-ecaf-4d57-b0f6-c04ce81674c4")) != null;
            return "{\"ok\":true,\"protocol\":3,\"private_api\":true"
                    + ",\"graph_available\":" + graphAvailable
                    + ",\"graph_class\":" + (graph == null
                            ? "null" : string(graph.getClass().getName()))
                    + ",\"graph_inspection\":" + graphAvailable
                    + ",\"host_modulators\":" + graphAvailable
                    + ",\"module_catalog\":" + insertionAvailable
                    + ",\"module_insertion\":" + insertionAvailable
                    + ",\"port_connections\":" + graphAvailable
                    + ",\"native_undo\":true}";
        } catch (Throwable error) {
            return "{\"ok\":true,\"protocol\":3,\"private_api\":true"
                    + ",\"graph_available\":false,\"graph_inspection\":false"
                    + ",\"host_modulators\":false,\"module_catalog\":false"
                    + ",\"module_insertion\":false,\"port_connections\":false"
                    + ",\"native_undo\":true"
                    + ",\"reason\":" + string(rootMessage(error)) + "}";
        }
    }

    static String snapshot(CursorDevice cursorDevice) {
        try {
            Object graph = selectedGraph(cursorDevice);
            return "{\"ok\":true,\"graph_class\":"
                    + string(graph.getClass().getName())
                    + ",\"modules\":" + modules(graph) + "}";
        } catch (Throwable error) {
            throw new IllegalStateException(rootMessage(error), error);
        }
    }
    static void clear(CursorDevice cursorDevice, Consumer<String> completion) {
        try {
            Object graph = selectedGraph(cursorDevice);
            List<?> modules = moduleObjects(graph);
            onUiThread(() -> {
                try {
                    int removed = 0;
                    for (int index = modules.size() - 1; index >= 0; index--) {
                        invokeNoArg(modules.get(index), "TJs");
                        removed++;
                    }
                    completion.accept("{\"ok\":true,\"operation\":\"clear\""
                            + ",\"removed\":" + removed
                            + ",\"state\":" + modules(graph) + "}");
                } catch (Throwable error) {
                    completion.accept("{\"ok\":false,\"error\":"
                            + string(rootMessage(error)) + "}");
                }
            });
        } catch (Throwable error) {
            completion.accept("{\"ok\":false,\"error\":"
                    + string(rootMessage(error)) + "}");
        }
    }

    static String hostModulators(CursorDevice cursorDevice) {
        try {
            StringBuilder json = new StringBuilder(
                    "{\"ok\":true,\"capabilities\":[\"name\",\"mapped\",\"mapping\"],\"sources\":[");
            int emitted = 0;
            int emptySources = 0;
            for (int index = 0; index < 64; index++) {
                try {
                    ModulationSource source = cursorDevice.getModulationSource(index);
                    if (source == null) {
                        continue;
                    }
                    source.name().markInterested();
                    source.isMapped().markInterested();
                    source.isMapping().markInterested();
                    String name = source.name().get();
                    if (name == null || name.isBlank()) {
                        emptySources++;
                        if (index >= 8 && emptySources >= 8) {
                            break;
                        }
                        continue;
                    }
                    emptySources = 0;
                    if (emitted++ > 0) {
                        json.append(',');
                    }
                    json.append("{\"source_index\":").append(index)
                            .append(",\"name\":").append(string(name))
                            .append(",\"mapped\":").append(source.isMapped().get())
                            .append(",\"mapping\":").append(source.isMapping().get())
                            .append('}');
                } catch (Throwable ignored) {
                    if (index >= 8) {
                        break;
                    }
                }
            }
            return json.append("]}").toString();
        } catch (Throwable error) {
            return "{\"ok\":false,\"error\":" + string(rootMessage(error)) + "}";
        }
    }


    static String catalog(String query) {
        try {
            Class<?> catalogClass = Class.forName("com.bitwig.flt.packaging.core.ytr");
            Method listMethod = catalogClass.getDeclaredMethod("FhI");
            listMethod.setAccessible(true);
            Object value = listMethod.invoke(null);
            if (!(value instanceof List<?> entries)) {
                return "{\"ok\":false,\"error\":\"module catalog unavailable\"}";
            }
            String needle = query == null ? "" : query.strip().toLowerCase(Locale.ROOT);
            StringBuilder json = new StringBuilder("{\"ok\":true,\"modules\":[");
            int emitted = 0;
            for (Object entry : entries) {
                Object kind = invokeNoArg(entry, "VRl");
                String name = String.valueOf(invokeNoArg(entry, "gGl"));
                UUID id = (UUID) invokeNoArg(entry, "FhI");
                if (!"MODULE".equals(String.valueOf(kind))
                        || (!needle.isEmpty()
                        && !name.toLowerCase(Locale.ROOT).contains(needle)
                        && !id.toString().contains(needle))) {
                    continue;
                }
                if (emitted++ > 0) {
                    json.append(',');
                }
                json.append("{\"package_id\":").append(string(id))
                        .append(",\"name\":").append(string(name)).append('}');
            }
            return json.append("],\"count\":").append(emitted).append('}').toString();
        } catch (Throwable error) {
            return "{\"ok\":false,\"error\":" + string(rootMessage(error)) + "}";
        }
    }

    static void insert(
            CursorDevice cursorDevice,
            UUID moduleId,
            int x,
            int y,
            Consumer<String> completion) {
        insert(cursorDevice, moduleId, x, y, completion, true);
    }

    private static void insert(
            CursorDevice cursorDevice,
            UUID moduleId,
            int x,
            int y,
            Consumer<String> completion,
            boolean includeState) {
        try {
            if (!isGridModule(moduleId)) {
                throw new IllegalArgumentException("unknown Grid module package: " + moduleId);
            }
            Object graph = selectedGraph(cursorDevice);
            File moduleFile = resolveModuleFile(moduleId);
            if (moduleFile == null) {
                throw new IllegalStateException("Grid module resource is unavailable: " + moduleId);
            }
            Method insert = findInsertMethod(graph.getClass());
            if (insert == null) {
                throw new IllegalStateException("Bitwig Grid insertion API is unsupported by this build");
            }
            Set<String> before = moduleIds(graph);
            Class<?> callbackType = insert.getParameterTypes()[3];
            AtomicBoolean completed = new AtomicBoolean();
            Object callback = Proxy.newProxyInstance(
                    callbackType.getClassLoader(),
                    new Class<?>[]{callbackType},
                    (proxy, method, arguments) -> {
                        if (method.getDeclaringClass() == Object.class) {
                            return switch (method.getName()) {
                                case "toString" -> "Grid module insertion callback";
                                case "hashCode" -> System.identityHashCode(proxy);
                                case "equals" -> proxy == arguments[0];
                                default -> null;
                            };
                        }
                        Class<?> parameter = method.getParameterTypes()[0];
                        Object argument = arguments == null || arguments.length == 0
                                ? null : arguments[0];
                        if (parameter == String.class || Exception.class.isAssignableFrom(parameter)) {
                            if (completed.compareAndSet(false, true)) {
                                completion.accept("{\"ok\":false,\"error\":"
                                        + string(argument) + "}");
                            }
                        } else if (completed.compareAndSet(false, true)) {
                            String insertedId = firstNewModuleId(graph, before);
                            completion.accept("{\"ok\":true,\"operation\":\"insert\""
                                    + ",\"package_id\":" + string(moduleId)
                                    + ",\"instance_id\":" + string(insertedId)
                                    + ",\"state\":" + (includeState ? modules(graph) : "{}") + "}");
                        }
                        return null;
                    });
            insert.setAccessible(true);
            onUiThread(() -> {
                try {
                    insert.invoke(graph, moduleFile.getAbsolutePath(), x, y, callback);
                } catch (Throwable error) {
                    if (completed.compareAndSet(false, true)) {
                        completion.accept("{\"ok\":false,\"error\":"
                                + string(rootMessage(error)) + "}");
                    }
                }
            });
        } catch (Throwable error) {
            completion.accept("{\"ok\":false,\"error\":" + string(rootMessage(error)) + "}");
        }
    }

    static void move(
            CursorDevice cursorDevice,
            String instanceId,
            int x,
            int y,
            Consumer<String> completion) {
        try {
            Object graph = selectedGraph(cursorDevice);
            Object module = requireModule(graph, instanceId);
            Method setter = findPositionSetter(module.getClass());
            if (setter == null) {
                throw new IllegalStateException("Bitwig Grid module position API is unavailable");
            }
            setter.setAccessible(true);
            onUiThread(() -> {
                try {
                    setter.invoke(module, x, y);
                    completion.accept("{\"ok\":true,\"operation\":\"move\""
                            + ",\"instance_id\":" + string(instanceId)
                            + ",\"x\":" + x + ",\"y\":" + y
                            + ",\"state\":" + modules(graph) + "}");
                } catch (Throwable error) {
                    completion.accept("{\"ok\":false,\"error\":"
                            + string(rootMessage(error)) + "}");
                }
            });
        } catch (Throwable error) {
            completion.accept("{\"ok\":false,\"error\":"
                    + string(rootMessage(error)) + "}");
        }
    }

    static void connect(
            CursorDevice cursorDevice,
            String sourceModuleId,
            int sourcePortIndex,
            String targetModuleId,
            int targetPortIndex,
            Consumer<String> completion) {
        connect(
                cursorDevice,
                sourceModuleId,
                sourcePortIndex,
                targetModuleId,
                targetPortIndex,
                completion,
                true);
    }

    private static void connect(
            CursorDevice cursorDevice,
            String sourceModuleId,
            int sourcePortIndex,
            String targetModuleId,
            int targetPortIndex,
            Consumer<String> completion,
            boolean includeState) {
        try {
            Object graph = selectedGraph(cursorDevice);
            Object sourceModule = requireModule(graph, sourceModuleId);
            Object targetModule = requireModule(graph, targetModuleId);
            Object sourcePort = requirePort(sourceModule, "kfJ", sourcePortIndex, "output");
            Object targetPort = requirePort(targetModule, "gwb", targetPortIndex, "input");
            onUiThread(() -> {
                try {
                    setInputSource(targetPort, sourcePort);
                    completion.accept("{\"ok\":true,\"operation\":\"connect\",\"state\":"
                            + (includeState ? modules(graph) : "{}") + "}");
                } catch (Throwable error) {
                    completion.accept("{\"ok\":false,\"error\":"
                            + string(rootMessage(error)) + "}");
                }
            });
        } catch (Throwable error) {
            completion.accept("{\"ok\":false,\"error\":" + string(rootMessage(error)) + "}");
        }
    }

    static void disconnect(
            CursorDevice cursorDevice,
            String targetModuleId,
            int targetPortIndex,
            Consumer<String> completion) {
        try {
            Object graph = selectedGraph(cursorDevice);
            Object targetModule = requireModule(graph, targetModuleId);
            Object targetPort = requirePort(targetModule, "gwb", targetPortIndex, "input");
            onUiThread(() -> {
                try {
                    setInputSource(targetPort, null);
                    completion.accept("{\"ok\":true,\"operation\":\"disconnect\",\"state\":"
                            + modules(graph) + "}");
                } catch (Throwable error) {
                    completion.accept("{\"ok\":false,\"error\":"
                            + string(rootMessage(error)) + "}");
                }
            });
        } catch (Throwable error) {
            completion.accept("{\"ok\":false,\"error\":" + string(rootMessage(error)) + "}");
        }
    }
    static void setParameter(
            CursorDevice cursorDevice,
            String moduleId,
            String parameterId,
            String rawValue,
            Consumer<String> completion) {
        setParameter(cursorDevice, moduleId, parameterId, rawValue, completion, true);
    }

    private static void setParameter(
            CursorDevice cursorDevice,
            String moduleId,
            String parameterId,
            String rawValue,
            Consumer<String> completion,
            boolean includeState) {
        try {
            Object graph = selectedGraph(cursorDevice);
            Object module = requireModule(graph, moduleId);
            Object parameter = requireParameter(module, parameterId);
            Object value = parseParameterValue(rawValue);
            onUiThread(() -> {
                try {
                    setParameterValue(parameter, value);
                    completion.accept("{\"ok\":true,\"operation\":\"set_parameter\""
                            + ",\"module_id\":" + string(moduleId)
                            + ",\"parameter_id\":" + string(parameterId)
                            + ",\"state\":" + (includeState ? modules(graph) : "{}") + "}");
                } catch (Throwable error) {
                    completion.accept("{\"ok\":false,\"error\":"
                            + string(rootMessage(error)) + "}");
                }
            });
        } catch (Throwable error) {
            completion.accept("{\"ok\":false,\"error\":" + string(rootMessage(error)) + "}");
        }
    }


    private static Object selectedTarget(CursorDevice cursorDevice)
            throws ReflectiveOperationException {
        Object target = invokeNoArg(cursorDevice, "getDeepestTarget");
        if (target == null) {
            throw new IllegalStateException("no selected document target");
        }
        return target;
    }

    private static Object selectedGraph(CursorDevice cursorDevice)
            throws ReflectiveOperationException {
        Object graph = findGraph(selectedTarget(cursorDevice));
        if (graph == null) {
            throw new IllegalStateException("selected device has no editable Grid graph");
        }
        return graph;
    }

    private static Object findGraph(Object target) {
        for (Method method : methods(target.getClass())) {
            if (method.getParameterCount() != 0 || method.getReturnType().isPrimitive()) {
                continue;
            }
            Class<?> type = method.getReturnType();
            if (!type.getName().startsWith("com.bitwig.flt.document.core.master.device.")) {
                continue;
            }
            if (!hasMethod(type, "bZ_", 0) || !hasMethod(type, "FhI", 2)) {
                continue;
            }
            try {
                method.setAccessible(true);
                Object value = method.invoke(target);
                if (value != null) {
                    return value;
                }
            } catch (Throwable ignored) {
                // Try the next structurally matching target accessor.
            }
        }
        return null;
    }


    private static Method findInsertMethod(Class<?> graphType) {
        for (Method method : methods(graphType)) {
            Class<?>[] parameters = method.getParameterTypes();
            if (method.getName().equals("FhI")
                    && parameters.length == 4
                    && parameters[0] == String.class
                    && parameters[1] == int.class
                    && parameters[2] == int.class
                    && parameters[3].getName().equals("com.bitwig.base.async.uFl")) {
                return method;
            }
        }
        return null;
    }

    private static Method findPositionSetter(Class<?> moduleType) {
        for (Method method : methods(moduleType)) {
            Class<?>[] parameters = method.getParameterTypes();
            if (method.getName().equals("FhI")
                    && parameters.length == 2
                    && parameters[0] == int.class
                    && parameters[1] == int.class) {
                return method;
            }
        }
        return null;
    }

    private static boolean isGridModule(UUID moduleId) throws ReflectiveOperationException {
        Class<?> catalogClass = Class.forName("com.bitwig.flt.packaging.core.ytr");
        Method listMethod = catalogClass.getDeclaredMethod("FhI");
        listMethod.setAccessible(true);
        Object value = listMethod.invoke(null);
        if (!(value instanceof List<?> entries)) {
            return false;
        }
        for (Object entry : entries) {
            if (moduleId.equals(invokeNoArg(entry, "FhI"))
                    && "MODULE".equals(String.valueOf(invokeNoArg(entry, "VRl")))) {
                return true;
            }
        }
        return false;
    }

    private static Set<String> moduleIds(Object graph) throws ReflectiveOperationException {
        Set<String> ids = new HashSet<>();
        for (Object module : moduleObjects(graph)) {
            ids.add(String.valueOf(invokeNoArg(module, "cD_")));
        }
        return ids;
    }

    private static String firstNewModuleId(Object graph, Set<String> before)
            throws ReflectiveOperationException {
        for (Object module : moduleObjects(graph)) {
            String id = String.valueOf(invokeNoArg(module, "cD_"));
            if (!before.contains(id)) {
                return id;
            }
        }
        return null;
    }

    private static List<?> moduleObjects(Object graph) throws ReflectiveOperationException {
        Object value = invokeNoArg(graph, "bZ_");
        if (!(value instanceof Stream<?> stream)) {
            throw new IllegalStateException("Grid module stream unavailable");
        }
        return stream.toList();
    }

    private static Object requireModule(Object graph, String instanceId)
            throws ReflectiveOperationException {
        for (Object module : moduleObjects(graph)) {
            if (instanceId.equals(String.valueOf(invokeNoArg(module, "cD_")))) {
                return module;
            }
        }
        throw new IllegalArgumentException("Grid module instance does not exist: " + instanceId);
    }

    private static Object requireParameter(Object module, String parameterId)
            throws ReflectiveOperationException {
        Object value = invokeNoArg(module, "Ljv");
        if (!(value instanceof Stream<?> stream)) {
            throw new IllegalStateException("Grid parameter stream unavailable");
        }
        for (Object parameter : stream.toList()) {
            String id;
            String path;
            try {
                id = String.valueOf(invokeNoArg(parameter, "cD_"));
                path = String.valueOf(invokeNoArg(parameter, "gTB"));
            } catch (Throwable ignored) {
                continue;
            }
            if (!parameterId.equals(id)
                    || path.isEmpty()
                    || findParameterSetter(parameter) == null) {
                continue;
            }
            return parameter;
        }
        throw new IllegalArgumentException(
                "Grid parameter does not exist or is read-only: " + parameterId);
    }

    private static Object parseParameterValue(String rawValue) {
        if ("true".equalsIgnoreCase(rawValue)) {
            return Boolean.TRUE;
        }
        if ("false".equalsIgnoreCase(rawValue)) {
            return Boolean.FALSE;
        }
        double value = Double.parseDouble(rawValue);
        if (!Double.isFinite(value)) {
            throw new IllegalArgumentException("Grid numeric parameter must be finite");
        }
        return value;
    }

    private static void setParameterValue(Object parameter, Object value)
            throws ReflectiveOperationException {
        Method setter = findParameterSetter(parameter);
        if (setter == null) {
            throw new NoSuchMethodException("Grid parameter setter is unavailable");
        }
        String parameterId = String.valueOf(invokeNoArg(parameter, "cD_"));
        if ("TIMEBASE".equals(parameterId)) {
            throw new IllegalArgumentException(
                    "Grid TIMEBASE mutation is disabled because Bitwig 6.0.11 crashes "
                            + "when it is changed through the private Grid API");
        }
        Class<?> type = setter.getParameterTypes()[0];
        if (type == boolean.class) {
            if (!(value instanceof Boolean)) {
                throw new IllegalArgumentException("Grid parameter requires a boolean value");
            }
        } else if (type == double.class) {
            if (!(value instanceof Double number)) {
                throw new IllegalArgumentException("Grid parameter requires a numeric value");
            }
            validateParameterRange(parameter, type, number);
        } else if (type == int.class) {
            if (!(value instanceof Double number) || Math.rint(number) != number) {
                throw new IllegalArgumentException(
                        "Grid integer parameter requires a whole-number value");
            }
            validateParameterRange(parameter, type, number);
            value = number.intValue();
        }
        setter.setAccessible(true);
        setter.invoke(parameter, value);
    }
    private static void validateParameterRange(
            Object parameter,
            Class<?> type,
            double value) throws ReflectiveOperationException {
        Object definition = invokeNoArg(parameter, "cpx");
        if (definition == null) {
            if (type == int.class && isDiscreteOptionValue(parameter, value)) {
                return;
            }
            throw new IllegalStateException("Grid parameter range is unavailable");
        }
        String minimumMethod = type == int.class ? "vwE" : "JsS";
        String maximumMethod = type == int.class ? "yYp" : "jYd";
        Object minimum = invokeNoArg(definition, minimumMethod);
        Object maximum = invokeNoArg(definition, maximumMethod);
        if (!(minimum instanceof Number min) || !(maximum instanceof Number max)) {
            if (type == int.class && isDiscreteOptionValue(parameter, value)) {
                return;
            }
            throw new IllegalStateException("Grid parameter range is unavailable");
        }
        double minValue = min.doubleValue();
        double maxValue = max.doubleValue();
        if (!Double.isFinite(minValue)
                || !Double.isFinite(maxValue)
                || value < minValue
                || value > maxValue) {
            throw new IllegalArgumentException(
                    "Grid parameter must be between " + minValue + " and " + maxValue);
        }
    }

    private static boolean isDiscreteOptionValue(Object parameter, double value)
            throws ReflectiveOperationException {
        if (!Double.isFinite(value) || Math.rint(value) != value) {
            return false;
        }
        Object scale = invokeNoArg(parameter, "lwe");
        Object values = invokeNoArg(scale, "Ehl");
        return values instanceof String[] labels
                && labels.length > 0
                && value >= 0
                && value < labels.length;
    }

    private static Method findParameterSetter(Object parameter) {
        for (Method method : methods(parameter.getClass())) {
            Class<?>[] types = method.getParameterTypes();
            if (types.length != 1) {
                continue;
            }
            if (method.getName().equals("Swu") && types[0] == double.class) {
                return method;
            }
            if (method.getName().equals("FhI") && types[0] == boolean.class) {
                return method;
            }
            if (method.getName().equals("yYp") && types[0] == int.class) {
                return method;
            }
        }
        return null;
    }

    private static String parameterType(Method setter) {
        return switch (setter.getParameterTypes()[0].getName()) {
            case "boolean" -> "boolean";
            case "int" -> "integer";
            default -> "float";
        };
    }

    private static Object requirePort(
            Object module,
            String methodName,
            int index,
            String direction) throws ReflectiveOperationException {
        if (index < 0) {
            throw new IllegalArgumentException(direction + " port index must be non-negative");
        }
        Object value = invokeNoArg(module, methodName);
        if (!(value instanceof Stream<?> stream)) {
            throw new IllegalStateException("Grid " + direction + " port stream unavailable");
        }
        List<?> ports = stream.toList();
        if (index >= ports.size()) {
            throw new IllegalArgumentException(direction + " port index " + index
                    + " is outside 0-" + Math.max(ports.size() - 1, 0));
        }
        return ports.get(index);
    }

    private static void setInputSource(Object input, Object output)
            throws ReflectiveOperationException {
        for (Method method : methods(input.getClass())) {
            Class<?>[] parameters = method.getParameterTypes();
            if (!method.getName().equals("gGl")
                    || parameters.length != 1
                    || (!parameters[0].getName().equals(
                            "com.bitwig.flt.document.core.master.device.NMK"))
                    || (output != null && !parameters[0].isAssignableFrom(output.getClass()))) {
                continue;
            }
            method.setAccessible(true);
            method.invoke(input, output);
            return;
        }
        throw new NoSuchMethodException("Bitwig Grid input connection API is unavailable");
    }


    private static String modules(Object graph) {
        Object streamValue;
        try {
            streamValue = invokeNoArg(graph, "bZ_");
        } catch (Throwable error) {
            return "{\"error\":" + string(rootMessage(error)) + "}";
        }
        if (!(streamValue instanceof Stream<?> stream)) {
            return "{\"error\":\"Grid module stream unavailable\"}";
        }
        List<?> modules = stream.toList();
        StringBuilder json = new StringBuilder("{\"count\":").append(modules.size())
                .append(",\"items\":[");
        for (int i = 0; i < modules.size(); i++) {
            if (i > 0) {
                json.append(',');
            }
            json.append(module(modules.get(i)));
        }
        return json.append("]}").toString();
    }

    private static String module(Object module) {
        StringBuilder json = new StringBuilder("{\"class\":")
                .append(string(module.getClass().getName()));
        appendString(json, module, "instance_id", "cD_");
        try {
            Object descriptor = invokeNoArg(module, "EGC");
            appendString(json, descriptor, "package_id", "bD1");
            appendString(json, descriptor, "module_name", "vwE");
        } catch (Throwable ignored) {
            // The fixed Grid input/output modules have no package descriptor.
        }
        appendInt(json, module, "x", "cL_");
        appendInt(json, module, "y", "vwE");
        appendPorts(json, module, "outputs", "kfJ");
        appendPorts(json, module, "inputs", "gwb");
        appendParameters(json, module);
        return json.append('}').toString();
    }

    private static void appendParameters(StringBuilder json, Object module) {
        try {
            Object value = invokeNoArg(module, "Ljv");
            if (!(value instanceof Stream<?> stream)) {
                return;
            }
            json.append(",\"parameters\":[");
            int index = 0;
            for (Object parameter : stream.toList()) {
                String id;
                String path;
                try {
                    path = String.valueOf(invokeNoArg(parameter, "gTB"));
                } catch (Throwable ignored) {
                    continue;
                }
                if (path.isEmpty()) {
                    continue;
                }
                try {
                    id = String.valueOf(invokeNoArg(parameter, "cD_"));
                } catch (Throwable ignored) {
                    continue;
                }
                Method setter = findParameterSetter(parameter);
                if (setter == null) {
                    continue;
                }
                if (index++ > 0) {
                    json.append(',');
                }
                json.append("{\"id\":").append(string(id))
                        .append(",\"type\":").append(string(parameterType(setter)));
                try {
                    Object current = parameterValue(parameter, setter);
                    json.append(",\"label\":").append(string(current));
                    if (current instanceof Number number) {
                        json.append(",\"value\":").append(number);
                    } else if (current instanceof Boolean bool) {
                        json.append(",\"value\":").append(bool);
                    }
                } catch (Throwable ignored) {
                    // A control can still be writable when its current value is unavailable.
                }
                appendParameterMetadata(json, parameter, setter);
                try {
                    String display = String.valueOf(invokeNoArg(parameter, "TJK"));
                    if (!display.isEmpty() && !"null".equals(display)) {
                        json.append(",\"display\":").append(string(display));
                    }
                } catch (Throwable ignored) {
                    // Human-readable display metadata is optional.
                }
                json.append('}');
            }
            json.append(']');
        } catch (Throwable ignored) {
            // Parameter metadata is optional in unsupported Grid builds.
        }
    }

    private static Object parameterValue(Object parameter, Method setter)
            throws ReflectiveOperationException {
        Class<?> type = setter.getParameterTypes()[0];
        if (type == double.class || type == boolean.class) {
            return invokeNoArg(parameter, "yos");
        }
        if (type == int.class) {
            return invokeNoArg(parameter, "fpT");
        }
        throw new IllegalArgumentException("unsupported Grid parameter type: " + type);
    }

    private static void appendParameterMetadata(
            StringBuilder json,
            Object parameter,
            Method setter) {
        Class<?> type = setter.getParameterTypes()[0];
        if (type == boolean.class) {
            json.append(",\"options\":[false,true]");
            return;
        }
        try {
            Object definition = invokeNoArg(parameter, "cpx");
            String minimumMethod = type == int.class ? "vwE" : "JsS";
            String maximumMethod = type == int.class ? "yYp" : "jYd";
            Object minimum = invokeNoArg(definition, minimumMethod);
            Object maximum = invokeNoArg(definition, maximumMethod);
            if (minimum instanceof Number min && maximum instanceof Number max
                    && Double.isFinite(min.doubleValue())
                    && Double.isFinite(max.doubleValue())) {
                json.append(",\"range\":{\"min\":")
                        .append(min.doubleValue())
                        .append(",\"max\":")
                        .append(max.doubleValue())
                        .append('}');
            }
        } catch (Throwable ignored) {
            // Range metadata is optional in unsupported parameter implementations.
        }
        if (type == int.class) {
            appendDiscreteOptions(json, parameter);
        }
    }

    private static void appendDiscreteOptions(StringBuilder json, Object parameter) {
        try {
            Object scale = invokeNoArg(parameter, "lwe");
            Object values = invokeNoArg(scale, "Ehl");
            if (!(values instanceof String[] labels) || labels.length == 0) {
                return;
            }
            json.append(",\"options\":[");
            for (int i = 0; i < labels.length; i++) {
                if (i > 0) {
                    json.append(',');
                }
                json.append("{\"value\":").append(i)
                        .append(",\"label\":").append(string(labels[i]))
                        .append('}');
            }
            json.append(']');
        } catch (Throwable ignored) {
            // Discrete options are optional in unsupported parameter implementations.
        }
    }

    private static void appendPorts(
            StringBuilder json,
            Object module,
            String key,
            String methodName) {
        try {
            Object value = invokeNoArg(module, methodName);
            if (!(value instanceof Stream<?> stream)) {
                return;
            }
            json.append(',').append(string(key)).append(':').append('[');
            int index = 0;
            for (Object port : stream.toList()) {
                if (index > 0) {
                    json.append(',');
                }
                json.append("{\"index\":").append(index)
                        .append(",\"class\":").append(string(port.getClass().getName()));
                appendString(json, port, "path", "gTB");
                appendString(json, port, "name", "cD_");
                if ("inputs".equals(key)) {
                    appendConnection(json, port);
                }
                json.append('}');
                index++;
            }
            json.append(']');
        } catch (Throwable ignored) {
            // Port streams are build-specific; module state remains inspectable.
        }
    }

    private static void appendConnection(StringBuilder json, Object input) {
        try {
            Object source = invokeNoArg(input, "zDV");
            if (source == null || !hasMethod(source.getClass(), "cD_", 0)) {
                json.append(",\"connection\":null");
                return;
            }
            json.append(",\"connection\":{\"source_port\":")
                    .append(string(invokeNoArg(source, "cD_")));
            try {
                String path = String.valueOf(invokeNoArg(input, "gTB"));
                String marker = "CONTENTS/MODULES/";
                int start = path.indexOf(marker);
                if (start >= 0) {
                    start += marker.length();
                    int end = path.indexOf('/', start);
                    if (end > start) {
                        json.append(",\"source_module\":")
                                .append(string(path.substring(start, end)));
                    }
                }
            } catch (Throwable ignored) {
                // Unknown builds may use a different persisted connection path.
            }
            json.append('}');
        } catch (Throwable ignored) {
            json.append(",\"connection\":null");
        }
    }

    private static File resolveModuleFile(UUID moduleId) {
        try {
            Class<?> catalogClass = Class.forName("com.bitwig.flt.packaging.core.ytr");
            Method resolver = null;
            for (Method method : catalogClass.getDeclaredMethods()) {
                Class<?>[] parameters = method.getParameterTypes();
                if (Modifier.isStatic(method.getModifiers())
                        && method.getName().equals("FhI")
                        && parameters.length == 2
                        && parameters[0] == UUID.class
                        && method.getReturnType() == File.class) {
                    resolver = method;
                    break;
                }
            }
            if (resolver == null) {
                return null;
            }
            resolver.setAccessible(true);
            Class<?> managerType = resolver.getParameterTypes()[1];
            Class<?> applicationClass = Class.forName("com.bitwig.flt.app.gOg");
            Method singleton = applicationClass.getDeclaredMethod("kHC");
            singleton.setAccessible(true);
            Object application = singleton.invoke(null);
            for (Method accessor : methods(applicationClass)) {
                if (accessor.getParameterCount() != 0
                        || accessor.getReturnType() != managerType) {
                    continue;
                }
                try {
                    accessor.setAccessible(true);
                    Object manager = accessor.invoke(application);
                    if (manager == null) {
                        continue;
                    }
                    File file = (File) resolver.invoke(null, moduleId, manager);
                    if (file != null && file.isFile()) {
                        return file;
                    }
                } catch (Throwable ignored) {
                    // Some manager views are optional or unavailable during startup.
                }
            }
        } catch (Throwable ignored) {
            // Private packaging access is explicitly version-gated.
        }
        return null;
    }
    private static void onUiThread(Runnable action) throws ReflectiveOperationException {
        Class<?> applicationClass = Class.forName("com.bitwig.flt.app.gOg");
        Method singleton = applicationClass.getDeclaredMethod("kHC");
        singleton.setAccessible(true);
        Object application = singleton.invoke(null);
        for (Method method : methods(applicationClass)) {
            Class<?>[] parameters = method.getParameterTypes();
            if (method.getName().equals("asyncExec")
                    && parameters.length == 1
                    && parameters[0] == Runnable.class) {
                method.setAccessible(true);
                method.invoke(application, action);
                return;
            }
        }
        throw new NoSuchMethodException("Bitwig application event dispatcher is unavailable");
    }



    private static void appendString(StringBuilder json, Object target, String key, String methodName) {
        try {
            Object value = invokeNoArg(target, methodName);
            json.append(',').append(string(key)).append(':').append(string(value));
        } catch (Throwable ignored) {
            // Optional property.
        }
    }

    private static void appendInt(StringBuilder json, Object target, String key, String methodName) {
        try {
            int value = ((Number) invokeNoArg(target, methodName)).intValue();
            json.append(',').append(string(key)).append(':').append(value);
        } catch (Throwable ignored) {
            // Optional property.
        }
    }

    private static boolean hasMethod(Class<?> type, String name, int parameterCount) {
        for (Method method : methods(type)) {
            if (method.getName().equals(name) && method.getParameterCount() == parameterCount) {
                return true;
            }
        }
        return false;
    }

    private static Object invokeNoArg(Object target, String name) throws ReflectiveOperationException {
        for (Method method : methods(target.getClass())) {
            if (method.getName().equals(name) && method.getParameterCount() == 0) {
                method.setAccessible(true);
                return method.invoke(target);
            }
        }
        throw new NoSuchMethodException(target.getClass().getName() + '.' + name + "()");
    }

    private static List<Method> methods(Class<?> type) {
        List<Method> methods = new ArrayList<>();
        for (Class<?> current = type; current != null; current = current.getSuperclass()) {
            for (Method method : current.getDeclaredMethods()) {
                if (!Modifier.isStatic(method.getModifiers())) {
                    methods.add(method);
                }
            }
        }
        return methods;
    }

    private static String rootMessage(Throwable error) {
        Throwable current = error;
        while (current.getCause() != null) {
            current = current.getCause();
        }
        return current.toString();
    }

    private static String string(Object value) {
        if (value == null) {
            return "null";
        }
        String text = value instanceof UUID ? value.toString() : String.valueOf(value);
        return '"' + text.replace("\\", "\\\\").replace("\"", "\\\"") + '"';
    }
}
