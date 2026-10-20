"""Infinite ammo — freezes the magazine count on the local weapon."""
from __future__ import annotations

from trainer_host.contracts import TrainerExtension
from trainer_host.hotkeys import HotkeyBus
from trainer_host.state import TrainerState
from offsets.patterns import AMMO_COUNTER_PATTERN
from offsets.resolver import resolve_pattern

MAG_SIZE = 30


class InfiniteAmmoExtension(TrainerExtension):
    NAME = "infinite_ammo"
    VERSION = "1.1.0"
    REQUIRES_BUILD = "1.0.3-boilingpoint"
    DEFAULT_ENABLED = True

    def __init__(self) -> None:
        self.hotkey = "f2"
        self._addr: int | None = None
        self._state: TrainerState | None = None

    def on_attach(self, state: TrainerState, hotkeys: HotkeyBus) -> None:
        self._state = state
        self._addr = resolve_pattern(state.process, AMMO_COUNTER_PATTERN)
        hotkeys.bind(self.hotkey, self._toggle)

    def _toggle(self) -> None:
        if self._state is None:
            return
        self._state.set_flag("infinite_ammo", not self._state.infinite_ammo)

    def tick(self, state: TrainerState) -> None:
        if not state.infinite_ammo or self._addr is None:
            return
        state.process.write(self._addr, MAG_SIZE.to_bytes(4, "little"))