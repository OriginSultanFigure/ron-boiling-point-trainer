"""Global hotkey bus backed by the keyboard module."""
from __future__ import annotations

from typing import Callable

import keyboard
from loguru import logger

Handler = Callable[[], None]


class HotkeyBus:
    def __init__(self) -> None:
        self._bindings: list[tuple[str, Handler]] = []

    def bind(self, combo: str, handler: Handler) -> None:
        try:
            keyboard.add_hotkey(combo, handler, suppress=False)
            self._bindings.append((combo, handler))
            logger.debug("hotkey bound: {}", combo)
        except Exception as exc:
            logger.warning("hotkey {} failed: {}", combo, exc)

    def poll(self) -> None:
        # keyboard module runs its own thread; poll exists for future backends
        return

    def unbind_all(self) -> None:
        for combo, _ in self._bindings:
            try:
                keyboard.remove_hotkey(combo)
            except Exception:
                pass
        self._bindings.clear()