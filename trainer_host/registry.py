"""Loads extensions/registry.json and filters by build compatibility."""
from __future__ import annotations

import json
from pathlib import Path

from trainer_host import GAME_BUILD_TARGET
from trainer_host.contracts import ExtensionSpec

DEFAULT_REGISTRY = Path(__file__).resolve().parent.parent / "extensions" / "registry.json"


class ExtensionRegistry:
    def __init__(self, path: Path = DEFAULT_REGISTRY) -> None:
        self.path = path
        self._specs: list[ExtensionSpec] = []
        self._load()

    def _load(self) -> None:
        if not self.path.exists():
            return
        raw = json.loads(self.path.read_text(encoding="utf-8"))
        for entry in raw.get("extensions", []):
            self._specs.append(ExtensionSpec(
                module=entry["module"],
                cls=entry["class"],
                enabled=entry.get("enabled", False),
                options=entry.get("options", {}),
            ))

    def enabled_specs(self) -> list[ExtensionSpec]:
        return [s for s in self._specs if s.enabled]

    def all_specs(self) -> list[ExtensionSpec]:
        return list(self._specs)

    def target_build(self) -> str:
        return GAME_BUILD_TARGET