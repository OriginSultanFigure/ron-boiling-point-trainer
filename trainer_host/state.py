"""Mutable shared state passed to every extension."""
from __future__ import annotations

import threading
from dataclasses import dataclass, field
from typing import Any

from trainer_host.process import GameProcess


@dataclass
class TrainerState:
    alive: bool = True
    godmode: bool = False
    infinite_ammo: bool = False
    no_recoil: bool = False
    super_speed: bool = False
    teleport_target: tuple[float, float, float] | None = None
    extras: dict[str, Any] = field(default_factory=dict)
    _process: GameProcess | None = None
    _lock: threading.RLock = field(default_factory=threading.RLock)

    def attach(self, process: GameProcess) -> None:
        self._process = process

    @property
    def process(self) -> GameProcess:
        if self._process is None:
            raise RuntimeError("state not attached to a process")
        return self._process

    def set_flag(self, name: str, value: bool) -> None:
        with self._lock:
            setattr(self, name, value)

    def shutdown(self) -> None:
        with self._lock:
            self.alive = False