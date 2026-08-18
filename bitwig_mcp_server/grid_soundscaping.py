"""Generic, provenance-free Grid soundscape composition guidance.

The planner describes reusable signal roles rather than serializing or copying
any external preset. Every module name is resolved against the live Grid
catalog before a caller mutates a project.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any


_UNIT_CONTROLS = ("density", "motion", "contrast", "temperature")

_MODULE_TUNING: dict[str, tuple[str, ...]] = {
    "Sine": ("PITCH", "DETUNE", "STEREO", "RETRIGGER"),
    "Sawtooth": ("PITCH", "DETUNE", "STEREO", "RETRIGGER"),
    "Pulse": ("PITCH", "TIMBRE", "DETUNE", "STEREO"),
    "Wavetable": ("PITCH", "TABLE_INDEX", "PHASE_MOD", "DETUNE"),
    "Noise": ("TYPE", "STEREO"),
    "AD": ("ATTACK", "DECAY", "MODEL"),
    "ADSR": ("ATTACK", "DECAY", "SUSTAIN", "RELEASE", "MODEL"),
    "Pluck": ("ATTACK", "DECAY", "RELEASE"),
    "S/H LFO": ("RATE", "TIMEBASE", "BIPOLAR", "SMOOTH", "FEEDBACK"),
    "Segments": ("RATE", "TIMEBASE", "CURVE", "ENABLE_SMOOTH"),
    "Chance": ("PROBABILITY", "NOTE_TRIGGER"),
    "Probabilities": ("STEPS", "DEVICE_PHASE", "MUTE_WHEN_STOPPED"),
    "Triggers": ("STEPS", "DEVICE_PHASE", "MUTE_WHEN_STOPPED"),
    "Clock": ("RATE", "RETRIGGER"),
    "Pitch Quantize": ("DISTRIBUTION", "USE_NOTE_INPUT"),
    "Pitches": ("STEPS", "DEVICE_PHASE", "MUTE_WHEN_STOPPED"),
    "All-pass Delay": ("TIME", "GAIN"),
    "Long Delay": ("UNIT", "TIME", "STEPS", "OFFSET"),
    "Mod Delay": ("TIME", "MODULATION", "FEEDBACK", "CUTOFF", "DRIVE"),
    "Stereo Width": ("WIDTH",),
    "Low-pass": ("CUTOFF", "POLES"),
    "High-pass": ("CUTOFF", "POLES"),
    "Sallen-Key": ("CUTOFF", "RESONANCE", "DRIVE", "POLES"),
    "Wavefolder": ("DRIVE", "AA"),
    "AM/RM": ("DEPTH",),
    "Blend": ("DEPTH", "MODE"),
    "Gain - Vol": ("DRIVE",),
}


_RECIPES: dict[str, dict[str, Any]] = {
    "deep-ambient": {
        "aliases": ("deep-bed", "slow-air", "sleep", "drone", "pad"),
        "principles": (
            "Start with a small sustained harmonic bed.",
            "Use slow, bounded motion instead of constant event density.",
            "Let serial diffusion create size; keep the dry source quiet.",
        ),
        "layers": (
            {
                "id": "bed",
                "role": "sustained harmonic floor",
                "modules": ("Sine", "Sawtooth", "Transpose", "Mixer"),
                "routing": "Use a root plus restrained interval voices, then mix before diffusion.",
                "tuning": ("PITCH", "DETUNE", "LEVEL_1", "LEVEL_2"),
            },
            {
                "id": "space",
                "role": "large but controlled space",
                "modules": (
                    "All-pass Delay",
                    "All-pass Delay",
                    "Long Delay",
                    "Stereo Width",
                ),
                "routing": "Cascade diffusion, then add one longer echo and widen after the main buildup.",
                "tuning": ("TIME", "GAIN", "STEPS", "WIDTH"),
            },
            {
                "id": "motion",
                "role": "slow spectral drift",
                "modules": ("S/H LFO", "Low-pass", "Blend"),
                "routing": "Modulate filter cutoff or blend depth with a slow bipolar source.",
                "tuning": ("RATE", "TIMEBASE", "SMOOTH", "CUTOFF"),
            },
        ),
    },
    "weather-texture": {
        "aliases": ("weather", "rain", "wind", "nature", "water", "beach"),
        "principles": (
            "Build texture from noise and filtering, not a dense melodic layer.",
            "Use independent event envelopes so droplets or accents remain sparse.",
            "Separate low rumble, mid texture, and bright transients before space.",
        ),
        "layers": (
            {
                "id": "texture",
                "role": "continuous environmental bed",
                "modules": ("Noise", "Low-pass", "High-pass", "S/H LFO"),
                "routing": "Split noise into slow low-band motion and a restrained high-band texture.",
                "tuning": ("TYPE", "CUTOFF", "POLES", "RATE"),
            },
            {
                "id": "events",
                "role": "rare droplets or organic accents",
                "modules": ("Clock", "Chance", "AD", "Sine", "High-pass"),
                "routing": "Gate short tonal events through probability before filtering and diffusion.",
                "tuning": ("RATE", "PROBABILITY", "ATTACK", "DECAY", "PITCH"),
            },
            {
                "id": "space",
                "role": "distance and cohesion",
                "modules": ("All-pass Delay", "Mod Delay", "Stereo Width"),
                "routing": "Diffuse each layer separately, then use modest modulation and width for glue.",
                "tuning": ("TIME", "MODULATION", "FEEDBACK", "WIDTH"),
            },
        ),
    },
    "distant-events": {
        "aliases": (
            "distant-signals",
            "night-motion",
            "signals",
            "space",
            "city",
            "rooftop",
        ),
        "principles": (
            "Keep a stable bed while events arrive at unrelated slow rates.",
            "Quantize pitch choices, but randomize timing and level independently.",
            "Reserve the brightest or most resonant material for infrequent events.",
        ),
        "layers": (
            {
                "id": "bed",
                "role": "stable tonal reference",
                "modules": ("Sine", "Transpose", "Pitch Quantize", "Mixer"),
                "routing": "Create a quiet root-and-interval bed and constrain pitch before audio generation.",
                "tuning": ("PITCH", "VALUE", "DISTRIBUTION", "LEVEL_1"),
            },
            {
                "id": "events",
                "role": "rare pitched signals",
                "modules": ("Clock", "Probabilities", "Pitches", "ADSR", "Wavetable"),
                "routing": "Use clocked probability to choose events, then send pitch through the active scale.",
                "tuning": (
                    "RATE",
                    "STEPS",
                    "DEVICE_PHASE",
                    "ATTACK",
                    "DECAY",
                    "TABLE_INDEX",
                ),
            },
            {
                "id": "tail",
                "role": "distant tails and echoes",
                "modules": ("Long Delay", "All-pass Delay", "Low-pass", "Stereo Width"),
                "routing": "Filter the return, diffuse it, and keep the wet tail below the dry event peak.",
                "tuning": ("TIME", "STEPS", "OFFSET", "CUTOFF", "WIDTH"),
            },
        ),
    },
    "harmonic-drift": {
        "aliases": ("layered-motion", "modal", "generative-harmony", "drift"),
        "principles": (
            "Use a defined pitch vocabulary while allowing slow root movement.",
            "Separate harmonic motion from timbral motion so the result stays legible.",
            "Rotate or transpose the bed gradually; do not randomize every voice at once.",
        ),
        "layers": (
            {
                "id": "harmony",
                "role": "scale-aware chord bed",
                "modules": (
                    "Sine",
                    "Sawtooth",
                    "Root Key",
                    "Pitch Quantize",
                    "Transpose",
                ),
                "routing": "Generate related voices, quantize their pitch, then apply slow interval motion.",
                "tuning": ("PITCH", "DETUNE", "DISTRIBUTION", "VALUE"),
            },
            {
                "id": "movement",
                "role": "slow non-repeating movement",
                "modules": ("S/H LFO", "Steps", "Scale Steps", "Blend"),
                "routing": "Use stepped or smoothed control for one musical destination at a time.",
                "tuning": ("RATE", "STEPS", "INTERPOLATION", "DEPTH"),
            },
            {
                "id": "diffusion",
                "role": "soft stereo field",
                "modules": (
                    "All-pass Delay",
                    "All-pass Delay",
                    "Chorus+",
                    "Stereo Width",
                ),
                "routing": "Build depth with serial all-pass stages, then add chorus and width conservatively.",
                "tuning": ("TIME", "GAIN", "WIDTH"),
            },
        ),
    },
    "artifact-bed": {
        "aliases": ("machine-dream", "industrial", "cyberpunk", "artifact", "feedback"),
        "principles": (
            "Put nonlinear processing inside a bounded feedback or modulation loop.",
            "Control unstable energy with filtering, gain staging, and a visible meter.",
            "Contrast clipped artifacts with a quiet tonal or noise bed.",
        ),
        "layers": (
            {
                "id": "source",
                "role": "tonal or noisy excitation",
                "modules": ("Noise", "Sine", "AM/RM", "Wavefolder"),
                "routing": "Cross-modulate a simple source, then fold or ring-modulate before the return path.",
                "tuning": ("TYPE", "PITCH", "DEPTH", "DRIVE"),
            },
            {
                "id": "control",
                "role": "bounded instability",
                "modules": ("S/H LFO", "Chance", "Low-pass", "High-pass", "Blend"),
                "routing": "Randomize one or two control destinations and smooth them before nonlinear stages.",
                "tuning": ("RATE", "PROBABILITY", "CUTOFF", "DEPTH"),
            },
            {
                "id": "safety",
                "role": "frequency and level containment",
                "modules": ("Mod Delay", "All-pass Delay", "Gain - Vol", "VU Meter"),
                "routing": "Limit feedback, filter the return, and monitor the level before the final output.",
                "tuning": ("FEEDBACK", "CUTOFF", "DRIVE"),
            },
        ),
    },
    "generative-percussion": {
        "aliases": ("pulse-lab", "percussion", "rhythm", "drums"),
        "principles": (
            "Generate several short voices with different envelopes and spectral centers.",
            "Use probability and phase offsets for variation instead of dense random writes.",
            "High-pass and short diffusion keep the result articulate.",
        ),
        "layers": (
            {
                "id": "voices",
                "role": "contrasting short voices",
                "modules": ("Noise", "Pulse", "Pluck", "AD"),
                "routing": "Give each voice a different source, pitch region, and envelope time.",
                "tuning": ("TYPE", "PITCH", "ATTACK", "DECAY"),
            },
            {
                "id": "variation",
                "role": "controlled pattern variation",
                "modules": ("Triggers", "Chance", "Steps", "Sample / Hold"),
                "routing": "Clock each voice independently and keep probability below continuous activity.",
                "tuning": ("STEPS", "PROBABILITY", "BIPOLAR", "RATE"),
            },
            {
                "id": "glue",
                "role": "short room and spectral glue",
                "modules": ("High-pass", "Blend", "All-pass Delay", "Mixer"),
                "routing": "Remove low buildup, blend dry and wet, then mix the voices deliberately.",
                "tuning": ("CUTOFF", "DEPTH", "TIME", "LEVEL_1"),
            },
        ),
    },
}


def _unit(value: Any, name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{name} must be a number between 0 and 1")
    result = float(value)
    if result < 0.0 or result > 1.0:
        raise ValueError(f"{name} must be between 0 and 1")
    return round(result, 3)


def _style_key(style: str | None, brief: str) -> str:
    if style is not None:
        if not isinstance(style, str) or not style.strip():
            raise ValueError("style must be a non-empty string when provided")
        needle = style.strip().lower()
        for key, recipe in _RECIPES.items():
            if needle == key or needle in recipe["aliases"]:
                return key
        raise ValueError(f"unknown soundscape style: {style}")

    text = brief.lower()
    for key in (
        "weather-texture",
        "generative-percussion",
        "artifact-bed",
        "distant-events",
        "harmonic-drift",
        "deep-ambient",
    ):
        if any(alias in text for alias in (key, *_RECIPES[key]["aliases"])):
            return key
    return "deep-ambient"


def plan_soundscape(
    brief: str,
    *,
    style: str | None = None,
    density: float = 0.3,
    motion: float = 0.35,
    contrast: float = 0.3,
    temperature: float = 0.5,
) -> dict[str, Any]:
    """Return a generic, live-resolvable Grid soundscape recipe."""
    if not isinstance(brief, str) or not brief.strip():
        raise ValueError("brief must be a non-empty string")
    controls = {
        name: _unit(value, name)
        for name, value in {
            "density": density,
            "motion": motion,
            "contrast": contrast,
            "temperature": temperature,
        }.items()
    }
    key = _style_key(style, brief)
    recipe = _RECIPES[key]
    layers = [deepcopy(layer) for layer in recipe["layers"]]
    if controls["density"] < 0.22:
        layers = [
            layer for layer in layers if layer["id"] not in {"events", "variation"}
        ]
    elif controls["density"] > 0.72 and key in {"weather-texture", "distant-events"}:
        layers.append(
            {
                "id": "accent",
                "role": "optional high-contrast accent",
                "modules": ("Chance", "Sine", "ADSR", "Mod Delay"),
                "routing": "Add only after the main bed is balanced; keep the accent probability low.",
                "tuning": ("PROBABILITY", "PITCH", "ATTACK", "DECAY", "MODULATION"),
            }
        )

    modules = sorted({module for layer in layers for module in layer["modules"]})
    for layer in layers:
        layer["module_tuning"] = {
            module: list(_MODULE_TUNING[module])
            for module in layer["modules"]
            if module in _MODULE_TUNING
        }
    return {
        "ok": True,
        "brief": brief.strip(),
        "style": key,
        "controls": controls,
        "principles": list(recipe["principles"]),
        "layers": layers,
        "module_queries": modules,
        "assembly_order": [layer["id"] for layer in layers],
        "resolution": {
            "step_1": "Call get_grid_capabilities and require graph_available=true.",
            "step_2": "Resolve every module_queries name with search_grid_modules.",
            "step_3": "Insert only returned package UUIDs at explicit coordinates.",
            "step_4": "Re-read get_grid_graph after each insertion and use fresh instance IDs.",
            "step_5": "Set only parameters present in the live graph range/options metadata.",
            "step_6": "Connect exact live ports, then re-read the graph before continuing.",
        },
        "guardrails": [
            "Do not treat this recipe as a preset or patch payload.",
            "Keep the dry bed audible while building the wet network.",
            "Use probability for sparse events and a separate clock for each independent layer.",
            "Bound feedback and monitor level before adding more diffusion.",
            "Prefer fewer voices with distinct roles over many continuously active voices.",
        ],
    }


def list_soundscape_styles() -> list[dict[str, Any]]:
    """Return the stable style vocabulary without external provenance."""
    return [
        {
            "id": key,
            "aliases": list(recipe["aliases"]),
            "principles": list(recipe["principles"]),
        }
        for key, recipe in _RECIPES.items()
    ]
