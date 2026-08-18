import type { ExtensionAPI } from "@oh-my-pi/pi-coding-agent";

export default function bitwigGridExtension(pi: ExtensionAPI) {
  pi.on("session_start", async (_event, ctx) => {
    ctx.ui.notify("Bitwig Grid shaping ready · /grid-shape <brief>", "info");
  });

  pi.registerCommand("grid-shape", {
    description: "Start a guided, preview-first Bitwig Grid shaping session",
    handler: async (args, ctx) => {
      const brief = args.trim();
      if (!brief) {
        ctx.ui.notify("Describe the Grid shape you want: /grid-shape <brief>", "warning");
        return;
      }
      pi.sendMessage(
        {
          customType: "bitwig-grid-shape",
          content: [
            "Start an interactive Bitwig Grid shaping session.",
            "Use the bitwig-grid-bridge MCP tools and follow the project skill.",
            `Brief: ${brief}`,
            "Begin with capability and selected-device reads, then return a non-mutating preview before applying.",
          ].join("\n"),
          display: true,
          attribution: "user",
        },
        { triggerTurn: true },
      );
    },
  });
}
