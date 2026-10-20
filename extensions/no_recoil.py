"""No recoil — zeroes the camera kick vector each tick."""
from __future__ import annotations

from trainer_host.contracts import TrainerExtension
from trainer_host.hotkeys import HotkeyBus
from trainer_host.state import TrainerState
from offsets.patterns import RECOIL_VECTOR_PATTERN
from offsets.resolver import resolve_pattern

ZERO_VEC = b"\x00\x00\x00\x00" * 3


class NoRecoilExtension(TrainerExtension):
    NAME = "no_recoil"
    VERSION = "1.0.4"
    REQUIRES_BUILD = "1.0.3-boilingpoint"
    DEFAULT_ENABLED = True

    def __init__(self) -> None:
        self.hotkey = "f3"
        self.strength = 1.0
        self._addr: int | None = None

    def on_attach(self, state: TrainerState, hotkeys: HotkeyBus) -> None:
        self._addr = resolve_pattern(state.process, RECOIL_VECTOR_PATTERN)
        hotkeys.bind(self.hotkey, self._toggle)
        self._state = state

    def _toggle(self) -> None:
        if self._state:
            self._state.set_flag("no_recoil", not self._state.no_recoil)

    def tick(self, state: TrainerState) -> None:
        if state.no_recoil and self._addr is not None and self.strength >= 1.0:
            state.process.write(self._addr, ZERO_VEC)