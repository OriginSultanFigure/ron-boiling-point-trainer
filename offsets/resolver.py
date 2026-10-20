"""Resolve byte patterns to absolute addresses inside the game module."""
from __future__ import annotations

import json
from pathlib import Path

import pymem.pattern
from loguru import logger

from trainer_host.process import GameProcess

CACHE_DIR = Path(__file__).resolve().parent / "cache"


def _cache_path(pattern: str) -> Path:
    digest = abs(hash(pattern)) & 0xFFFFFFFF
    return CACHE_DIR / f"{digest:08x}.json"


def resolve_pattern(process: GameProcess, pattern: str) -> int | None:
    cached = _cache_path(pattern)
    if cached.exists():
        try:
            data = json.loads(cached.read_text())
            if data.get("base") == process.base:
                return int(data["addr"], 16)
        except (json.JSONDecodeError, KeyError):
            pass

    try:
        addr = pymem.pattern.pattern_scan_module(
            process.handle.process_handle, process.handle.get_module(PROCESS_NAME := "ReadyOrNot-Win64-Shipping.exe"), pattern, return_multiple=False,
        )
    except Exception as exc:
        logger.debug("pattern scan failed: {}", exc)
        return None

    if addr:
        CACHE_DIR.mkdir(parents=True, exist_ok=True)
        cached.write_text(json.dumps({"base": process.base, "addr": hex(addr)}))
        logger.debug("resolved {} -> 0x{:x}", pattern[:12], addr)
    return addr
</br>