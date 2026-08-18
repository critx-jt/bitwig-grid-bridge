"""Interactive, preview-first workflows for shaping exposed Bitwig Grid controls."""

from __future__ import annotations

import secrets
import time
from dataclasses import dataclass, field
from functools import wraps
from threading import RLock
from typing import Any, Callable, cast


STYLE_PRESETS: dict[str, dict[str, float]] = {
    "glass": {
        "pulse": 0.18,
        "width": 0.66,
        "saw": 0.78,
        "tri": 0.10,
        "num": 0.62,
        "den": 0.28,
        "pitch": 0.54,
        "detune": 0.58,
    },
    "ember": {
        "pulse": 0.58,
        "width": 0.42,
        "saw": 0.72,
        "tri": 0.24,
        "num": 0.34,
        "den": 0.28,
        "pitch": 0.46,
        "detune": 0.53,
    },
    "acid": {
        "pulse": 0.84,
        "width": 0.22,
        "saw": 0.65,
        "tri": 0.05,
        "num": 0.72,
        "den": 0.18,
        "pitch": 0.52,
        "detune": 0.61,
    },
    "hollow": {
        "pulse": 0.12,
        "width": 0.42,
        "saw": 0.08,
        "tri": 0.18,
        "num": 0.38,
        "den": 0.22,
        "pitch": 0.50,
        "detune": 0.50,
    },
}

STYLE_PROFILES: dict[str, dict[str, Any]] = {
    "slow-air": {
        "preset": "glass",
        "intensity": 0.35,
        "principles": ["slow movement", "defined scale", "diffuse space"],
    },
    "deep-bed": {
        "preset": "hollow",
        "intensity": 0.25,
        "principles": ["sustained drone", "low density", "background role"],
    },
    "distant-events": {
        "preset": "hollow",
        "intensity": 0.22,
        "principles": ["rare events", "wide space", "long tails"],
    },
    "soft-drift": {
        "preset": "hollow",
        "intensity": 0.18,
        "principles": ["gentle evolution", "low density", "soft contrast"],
    },
    "night-motion": {
        "preset": "ember",
        "intensity": 0.45,
        "principles": ["textured motion", "scale-aware movement", "dark atmosphere"],
    },
    "layered-motion": {
        "preset": "ember",
        "intensity": 0.60,
        "principles": ["layered diffusion", "controlled artifacts", "persistent motion"],
    },
    "pulse-lab": {
        "preset": "acid",
        "intensity": 0.80,
        "principles": ["bounded variation", "regenerate gesture", "percussive contrast"],
    },
}

_SEMANTIC_ALIASES: dict[str, tuple[str, ...]] = {
    "pulse": ("pulse", "pulse %"),
    "width": ("pw", "pulse width", "width"),
    "saw": ("saw", "saw %"),
    "tri": ("tri", "tri %", "triangle"),
    "num": ("num", "numerator"),
    "den": ("den", "denominator"),
    "pitch": ("pitch",),
    "detune": ("detune", "detuning"),
}


@dataclass
class GridShapeSession:
    session_id: str
    brief: str
    preset: str
    intensity: float
    controls: dict[str, float]
    style: str | None
    baseline: dict[str, Any]
    draft: dict[int, float]
    revision: int = 1
    status: str = "draft"
    history: list[dict[str, Any]] = field(default_factory=list)

def _synchronized(method: Callable[..., Any]) -> Callable[..., Any]:
    @wraps(method)
    def wrapper(self: Any, *args: Any, **kwargs: Any) -> Any:
        with self._lock:
            return method(self, *args, **kwargs)

    return wrapper



class GridShapeManager:
    """Own process-local preview/apply sessions for interactive Grid shaping."""

    def __init__(self) -> None:
        self._sessions: dict[str, GridShapeSession] = {}
        self._lock = RLock()

    @staticmethod
    def list_styles() -> list[dict[str, Any]]:
        return [
            {
                "id": style,
                "preset": profile["preset"],
                "intensity": profile["intensity"],
                "principles": profile["principles"],
            }
            for style, profile in STYLE_PROFILES.items()
        ]

    @_synchronized
    def start(
        self,
        controller: Any,
        brief: str,
        preset: str | None = None,
        intensity: float | None = None,
        controls: dict[str, Any] | None = None,
        style: str | None = None,
    ) -> dict[str, Any]:
        if not isinstance(brief, str) or not brief.strip():
            raise ValueError("brief must be a non-empty string")
        style = self._validate_style(style)
        profile = STYLE_PROFILES.get(style or "", {})
        preset = self._validate_preset(preset or profile.get("preset", "glass"))
        intensity = self._validate_unit(
            intensity if intensity is not None else profile.get("intensity", 0.72),
            "intensity",
        )
        normalized_controls = self._normalize_controls(controls or {})
        state = self._selected_state(controller)
        draft = self._compose_values(state, preset, intensity, normalized_controls)
        session = GridShapeSession(
            session_id=f"grid-{secrets.token_urlsafe(6)}",
            brief=brief.strip(),
            preset=preset,
            intensity=intensity,
            controls=normalized_controls,
            style=style,
            baseline=state,
            draft=draft,
        )
        self._sessions[session.session_id] = session
        return self._preview(session, state)

    @_synchronized
    def compose(
        self,
        controller: Any,
        session_id: str,
        preset: str | None = None,
        intensity: float | None = None,
        controls: dict[str, Any] | None = None,
        style: str | None = None,
    ) -> dict[str, Any]:
        session = self._get(session_id)
        if style is not None:
            session.style = self._validate_style(style)
        profile = STYLE_PROFILES.get(session.style or "", {})
        if preset is not None:
            session.preset = self._validate_preset(preset)
        elif style is not None:
            session.preset = self._validate_preset(profile.get("preset", "glass"))
        if intensity is not None:
            session.intensity = self._validate_unit(intensity, "intensity")
        elif style is not None:
            session.intensity = self._validate_unit(
                profile.get("intensity", 0.72), "intensity"
            )
        if controls is not None:
            session.controls.update(self._normalize_controls(controls))
        state = self._selected_state(controller)
        session.draft = self._compose_values(
            state,
            session.preset,
            session.intensity,
            session.controls,
        )
        session.revision += 1
        session.status = "draft"
        return self._preview(session, state)

    @_synchronized
    def apply(
        self,
        controller: Any,
        session_id: str,
        revision: int,
        confirm: bool,
    ) -> dict[str, Any]:
        session = self._get(session_id)
        if confirm is not True:
            raise ValueError("confirm must be true to apply a Grid shaping draft")
        if revision != session.revision:
            raise ValueError(
                f"stale draft revision {revision}; current revision is {session.revision}"
            )
        state = self._selected_state(controller)
        self._assert_unchanged(session.baseline, state)
        before = self._values(state)
        changed = {
            index: round(value * 128.0, 6)
            for index, value in session.draft.items()
            if abs(value - before.get(index, value)) > 0.0001
        }
        if changed:
            controller.set_selected_device_parameters(changed)
        after = self._wait_for_change(controller, state, changed)
        applied = {
            "revision": revision,
            "changed": sorted(changed),
            "before": self._diff_values(state, changed),
            "after": self._diff_values(after, changed),
        }
        session.history.append(applied)
        session.baseline = after
        session.draft = self._values(after)
        session.status = "applied"
        return self._session_payload(session, after, applied=applied)

    @_synchronized
    def undo(self, controller: Any, session_id: str) -> dict[str, Any]:
        session = self._get(session_id)
        if not session.history:
            raise ValueError("session has no applied shaping revision to undo")
        last = session.history.pop()
        state = self._selected_state(controller)
        restore = {
            int(index): round(value * 128.0, 6)
            for index, value in last["before"].items()
            if int(index) in last["changed"]
        }
        if restore:
            controller.set_selected_device_parameters(restore)
        after = self._wait_for_change(controller, state, restore)
        session.baseline = after
        session.draft = self._values(after)
        session.revision += 1
        session.status = "undone"
        return self._session_payload(
            session,
            after,
            undone={"changed": sorted(restore), "from_revision": last["revision"]},
        )

    @_synchronized
    def status(self, controller: Any, session_id: str) -> dict[str, Any]:
        session = self._get(session_id)
        return self._preview(session, self._selected_state(controller))

    def _selected_state(self, controller: Any) -> dict[str, Any]:
        state = controller.get_selected_device_state()
        if not state.get("available", False):
            raise ValueError("no selected Bitwig device is available")
        return cast(dict[str, Any], state)

    def _wait_for_change(
        self,
        controller: Any,
        baseline: dict[str, Any],
        writes: dict[int, float],
    ) -> dict[str, Any]:
        """Read back host-thread writes before reporting a mutation."""
        if not writes:
            return baseline
        baseline_values = self._values(baseline)
        expected_values = {
            index: round(value / 128.0, 6) for index, value in writes.items()
        }
        deadline = time.monotonic() + 2.0
        while True:
            current = self._selected_state(controller)
            current_values = self._values(current)
            if all(
                abs(current_values.get(index, 0.0) - baseline_values.get(index, 0.0))
                > 0.0001
                or abs(current_values.get(index, 0.0) - expected_values[index])
                <= 1 / 128
                for index in writes
            ):
                return current
            if time.monotonic() >= deadline:
                raise TimeoutError("timed out waiting for Bitwig Grid parameter write")
            time.sleep(0.02)

    @staticmethod
    def _values(state: dict[str, Any]) -> dict[int, float]:
        return {
            int(parameter["index"]): round(float(parameter.get("value", 0.0)) / 128.0, 6)
            for parameter in state.get("parameters", [])
            if parameter.get("exists", True)
        }

    @staticmethod
    def _catalog(state: dict[str, Any]) -> dict[str, int]:
        catalog: dict[str, int] = {}
        for parameter in state.get("parameters", []):
            if parameter.get("exists", True):
                index = int(parameter["index"])
                name = str(parameter.get("name", f"parameter {index}"))
                catalog[GridShapeManager._key(name)] = index
        return catalog

    @staticmethod
    def _key(value: str) -> str:
        return " ".join(value.lower().replace("%", " percent ").split())

    def _resolve(self, state: dict[str, Any], name: str) -> int | None:
        catalog = self._catalog(state)
        key = self._key(name)
        if key.isdigit():
            index = int(key)
            return index if index in self._values(state) else None
        if key in catalog:
            return catalog[key]
        for semantic, aliases in _SEMANTIC_ALIASES.items():
            if key == semantic or key in aliases:
                for alias in aliases:
                    if self._key(alias) in catalog:
                        return catalog[self._key(alias)]
        return None

    def _normalize_controls(self, controls: dict[str, Any]) -> dict[str, float]:
        if not isinstance(controls, dict):
            raise ValueError("controls must be an object mapping names or indexes to 0-1 values")
        return {
            str(name): self._validate_unit(value, f"control {name}")
            for name, value in controls.items()
        }

    def _compose_values(
        self,
        state: dict[str, Any],
        preset: str,
        intensity: float,
        controls: dict[str, Any],
    ) -> dict[int, float]:
        current = self._values(state)
        targets = dict(current)
        matched = 0
        for semantic, target in STYLE_PRESETS[preset].items():
            index = self._resolve(state, semantic)
            if index is not None:
                targets[index] = round(current[index] + intensity * (target - current[index]), 6)
                matched += 1
        for name, value in controls.items():
            index = self._resolve(state, str(name))
            if index is None:
                raise ValueError(f"control {name!r} is not exposed by the selected device")
            targets[index] = self._validate_unit(value, f"control {name}")
            matched += 1
        if matched == 0:
            raise ValueError(
                "the selected device exposes no style controls; use explicit control names"
            )
        return targets

    @staticmethod
    def _diff_values(state: dict[str, Any], indexes: dict[int, Any]) -> dict[str, float]:
        values = GridShapeManager._values(state)
        return {str(index): values.get(index, 0.0) for index in indexes}

    @staticmethod
    def _assert_unchanged(
        baseline: dict[str, Any], current: dict[str, Any]
    ) -> None:
        if baseline.get("properties") != current.get("properties"):
            raise ValueError("selected device changed during the shaping session")
        baseline_values = GridShapeManager._values(baseline)
        current_values = GridShapeManager._values(current)
        if baseline_values != current_values:
            raise ValueError(
                "selected device parameters changed outside this session; compose again"
            )

    @staticmethod
    def _validate_unit(value: Any, field: str) -> float:
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise ValueError(f"{field} must be a number between 0 and 1")
        if not 0 <= value <= 1:
            raise ValueError(f"{field} must be between 0 and 1")
        return float(value)

    @staticmethod
    def _validate_preset(preset: str) -> str:
        if preset not in STYLE_PRESETS:
            choices = ", ".join(sorted(STYLE_PRESETS))
            raise ValueError(f"unknown style preset {preset!r}; choose {choices}")
        return preset

    @staticmethod
    def _validate_style(style: str | None) -> str | None:
        if style is None:
            return None
        if style not in STYLE_PROFILES:
            choices = ", ".join(sorted(STYLE_PROFILES))
            raise ValueError(f"unknown style profile {style!r}; choose {choices}")
        return style

    def _get(self, session_id: str) -> GridShapeSession:
        session = self._sessions.get(session_id)
        if session is None:
            raise ValueError(f"unknown Grid shaping session: {session_id}")
        return session

    def _preview(
        self, session: GridShapeSession, state: dict[str, Any]
    ) -> dict[str, Any]:
        current = self._values(state)
        changes = [
            {
                "index": index,
                "name": next(
                    (
                        parameter.get("name", f"Parameter {index}")
                        for parameter in state.get("parameters", [])
                        if int(parameter["index"]) == index
                    ),
                    f"Parameter {index}",
                ),
                "before": round(current.get(index, 0.0), 6),
                "after": round(value, 6),
                "delta": round(value - current.get(index, 0.0), 6),
            }
            for index, value in sorted(session.draft.items())
            if abs(value - current.get(index, value)) > 0.0001
        ]
        return self._session_payload(
            session,
            state,
            preview={
                "mutates": False,
                "changes": changes,
                "change_count": len(changes),
            },
        )

    @staticmethod
    def _session_payload(
        session: GridShapeSession,
        state: dict[str, Any],
        **extra: Any,
    ) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "session_id": session.session_id,
            "brief": session.brief,
            "style": session.style,
            "principles": STYLE_PROFILES.get(session.style or "", {}).get(
                "principles", []
            ),
            "preset": session.preset,
            "intensity": session.intensity,
            "controls": session.controls,
            "revision": session.revision,
            "status": session.status,
            "selected_device": state.get("properties", {}),
            "history_count": len(session.history),
        }
        payload.update(extra)
        return payload


def get_grid_shape_manager(controller: Any) -> GridShapeManager:
    """Return the manager attached to a controller, creating it for tests/embedders."""
    manager = getattr(controller, "grid_shape_manager", None)
    if not isinstance(manager, GridShapeManager):
        manager = GridShapeManager()
        controller.grid_shape_manager = manager
    return manager
