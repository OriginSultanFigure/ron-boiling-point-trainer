"""Godmode extension — patches the local player health write path."""
from __future__ import annotations

from loguru import logger

from trainer_host.contracts import TrainerExtension
from trainer_host.hotkeys import HotkeyBus
from trainer_host.state import TrainerState
from offsets.patterns import HEALTH_WRITE_PATTERN
from offsets.resolver import resolve_pattern

NOP = b"\x90"


class GodmodeExtension(TrainerExtension):
    NAME = "godmode"
    VERSION = "1.2.0"
    REQUIRES_BUILD = "1.0.3-boilingpoint"
    DEFAULT_ENABLED = True

    def __init__(self) -> None:
        self.hotkey: str = "f1"
        self._original: bytes | None = None
        self._patch_addr: int | None = None
        self._state: TrainerState | None = None

    def on_attach(self, state: TrainerState, hotkeys: HotkeyBus) -> None:
        self._state = state
        self._patch_addr = resolve_pattern(state.process, HEALTH_WRITE_PATTERN)
        if self._patch_addr is None:
            logger.error("godmode: health pattern not found")
            return
        self._original = state.process.read(self._patch_addr, 1)
        hotkeys.bind(self.hotkey, self._toggle)

    def _toggle(self) -> None:
        if self._state is None or self._patch_addr is None or self._original is None:
            return
        new = not self._state.godmode
        self._state.set_flag("godmode", new)
        payload = NOP if new else self._original
        self._state.process.write(self._patch_addr, payload)
        logger.info("godmode={}", new)

    def on_detach(self) -> None:
        if self._state and self._patch_addr and self._original:
            self._state.process.write(self._patch_addr, self._original)