"""Dynamic extension loader with importlib."""
from __future__ import annotations

import importlib
from typing import Any

from loguru import logger

from trainer_host.contracts import ExtensionSpec, TrainerExtension
from trainer_host.registry import ExtensionRegistry


class ExtensionLoader:
    def __init__(self, registry: ExtensionRegistry) -> None:
        self.registry = registry
        self._cache: dict[str, type[TrainerExtension]] = {}

    def resolve(self, spec: ExtensionSpec) -> type[TrainerExtension]:
        key = f"{spec.module}.{spec.cls}"
        if key in self._cache:
            return self._cache[key]
        try:
            module = importlib.import_module(spec.module)
        except ImportError as exc:
            logger.exception("cannot import {}", spec.module)
            raise RuntimeError(f"extension module {spec.module} unavailable") from exc
        cls: Any = getattr(module, spec.cls, None)
        if cls is None or not issubclass(cls, TrainerExtension):
            raise TypeError(f"{key} does not subclass TrainerExtension")
        self._cache[key] = cls
        return cls

    def instantiate(self, spec: ExtensionSpec) -> TrainerExtension:
        cls = self.resolve(spec)
        ext = cls()
        for k, v in spec.options.items():
            setattr(ext, k, v)
        return ext