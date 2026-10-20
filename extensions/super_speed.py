"""Super speed — scales the local player's movement velocity."""
from __future__ import annotations

from trainer_host.contracts import TrainerExtension
from trainer_host.hotkeys import HotkeyBus
from trainer_host.state import TrainerState
from offsets.patterns import VELOCITY_VECTOR_PATTERN
from offsets.resolver import resolve_pattern

import struct


class SuperSpeedExtension(TrainerExtension):
    NAME = "super_speed"
    VERSION = "0.9.1"
    REQUIRES_BUILD = "1.0.3-boilingpoint"
    DEFAULT_ENABLED = False

    def __init__(self) -> None:
        self.hotkey = "f4"
        self.multiplier = 2.5
        self._addr: int | None = None
        self._state: TrainerState | None = None

    def on_attach(self, state: TrainerState, hotkeys: HotkeyBus) -> None:
        self._state = state
        self._addr = resolve_pattern(state.process, VELOCITY_VECTOR_PATTERN)
        hotkeys.bind(self.hotkey, self._toggle)

    def _toggle(self) -> None:
        if self._state:
            self._state.set_flag("super_speed", not self._state.super_speed)

    def tick(self, state: TrainerState) -> None:
        if not state.super_speed or self._addr is None:
            return
        raw = state.process.read(self._addr, 12)
        vx, vy, vz = struct.unpack("<fff", raw)
        scaled = struct.pack("<fff", vx * self.multiplier, vy * self.multiplier, vz * self.multiplier)
        state.process.write(self._addr, scaled)