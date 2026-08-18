package io.github.critxjt.bitwig.gridbridge;

import com.bitwig.extension.api.PlatformType;
import com.bitwig.extension.controller.AutoDetectionMidiPortNamesList;
import com.bitwig.extension.controller.ControllerExtension;
import com.bitwig.extension.controller.ControllerExtensionDefinition;
import com.bitwig.extension.controller.HardwareDeviceMatcherList;
import com.bitwig.extension.controller.api.ControllerHost;

import java.util.UUID;

/** Definition for the local Bitwig Grid bridge. */
public final class GridBridgeExtensionDefinition extends ControllerExtensionDefinition {
    private static final UUID ID = UUID.fromString("1c2d6d57-0d14-4d4d-9f2d-2a67bf7d89b1");

    @Override
    public String getName() { return "Bitwig Grid Bridge"; }

    @Override
    public String getAuthor() { return "critx-jt"; }

    @Override
    public String getVersion() { return "0.1.0"; }

    @Override
    public UUID getId() { return ID; }

    @Override
    public int getRequiredAPIVersion() { return 21; }

    @Override
    public String getHardwareVendor() { return "bitwig-grid-bridge"; }

    @Override
    public String getHardwareModel() { return "Bitwig Grid Bridge"; }

    @Override
    public int getNumMidiInPorts() { return 0; }

    @Override
    public int getNumMidiOutPorts() { return 0; }

    @Override
    public void listAutoDetectionMidiPortNames(
            AutoDetectionMidiPortNamesList list, PlatformType platformType) {
        // This extension is intentionally network-only.
    }

    @Override
    public void listHardwareDevices(HardwareDeviceMatcherList matchers) {
        // No physical hardware is claimed.
    }

    @Override
    public ControllerExtension createInstance(ControllerHost host) {
        return new GridBridgeExtension(this, host);
    }
}
