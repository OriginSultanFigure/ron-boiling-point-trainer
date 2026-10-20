"""CLI: dump resolved offsets for the currently running game build."""
from __future__ import annotations

import json
import sys

from loguru import logger

from offsets.patterns import PATTERNS
from offsets.resolver import resolve_pattern
from trainer_host.process import GameProcess


def main() -> int:
    proc = GameProcess.discover()
    if proc is None:
        print("game not running", file=sys.stderr)
        return 1
    out: dict[str, str] = {}
    for name, pattern in PATTERNS.items():
        addr = resolve_pattern(proc, pattern)
        out[name] = hex(addr) if addr else "unresolved"
        logger.info("{} -> {}", name, out[name])
    print(json.dumps(out, indent=2))
    proc.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())