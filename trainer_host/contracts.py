"""Shared contracts every extension must implement."""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import ClassVar

from trainer_host.state import TrainerState
from trainer_host.hotkeys import HotkeyBus


class TrainerExtension(ABC):
    NAME: ClassVar[str] = "unnamed"
    VERSION: ClassVar[str] = "0.0.1"
    REQUIRES_BUILD: ClassVar[str] = "any"
    DEFAULT_ENABLED: ClassVar[bool] = False

    @abstractmethod
    def on_attach(self, state: TrainerState, hotkeys: HotkeyBus) -> None: ...

    def tick(self, state: TrainerState) -> None:
        """Called every frame from the host loop. Keep it cheap."""

    def on_detach(self) -> None:
        """Release handles, restore patched bytes, unbind hotkeys."""


class ExtensionSpec:
    __slots__ = ("module", "cls", "enabled", "options")

    def __init__(self, module: str, cls: str, enabled: bool, options: dict) -> None:
        self.module = module
        self.cls = cls
        self.enabled = enabled
        self.options = options

    def __repr__(self) -> str:
        return f"<ExtensionSpec {self.module}.{self.cls} enabled={self.enabled}>"