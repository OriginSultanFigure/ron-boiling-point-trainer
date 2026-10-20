"""Core trainer host: boots the process handle, loads extensions, runs the loop."""
from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

from loguru import logger

from trainer_host.contracts import TrainerExtension
from trainer_host.loader import ExtensionLoader
from trainer_host.registry import ExtensionRegistry
from trainer_host.process import GameProcess
from trainer_host.hotkeys import HotkeyBus
from trainer_host.state import TrainerState


def configure_logging(log_dir: Path) -> None:
    log_dir.mkdir(parents=True, exist_ok=True)
    logger.remove()
    logger.add(sys.stderr, level="INFO")
    logger.add(log_dir / "trainer.log", rotation="2 MB", retention=5, level="DEBUG")


def build_host(dry_run: bool = False) -> "TrainerHost":
    return TrainerHost(dry_run=dry_run)


class TrainerHost:
    def __init__(self, dry_run: bool = False) -> None:
        self.dry_run = dry_run
        self.state = TrainerState()
        self.hotkeys = HotkeyBus()
        self.registry = ExtensionRegistry()
        self.loader = ExtensionLoader(self.registry)
        self.process: GameProcess | None = None
        self.extensions: list[TrainerExtension] = []

    def attach(self) -> bool:
        self.process = GameProcess.discover()
        if self.process is None:
            logger.error("ReadyOrNot-Win64-Shipping.exe not found")
            return False
        logger.info("attached pid={} base=0x{:x}", self.process.pid, self.process.base)
        self.state.attach(self.process)
        return True

    def load_all(self) -> None:
        for spec in self.registry.enabled_specs():
            ext = self.loader.instantiate(spec)
            ext.on_attach(self.state, self.hotkeys)
            self.extensions.append(ext)
            logger.info("loaded extension {} v{}", ext.NAME, ext.VERSION)

    def run(self) -> None:
        if not self.dry_run and not self.attach():
            return
        self.load_all()
        logger.info("host running with {} extensions", len(self.extensions))
        try:
            while self.state.alive:
                self.hotkeys.poll()
                for ext in self.extensions:
                    ext.tick(self.state)
                time.sleep(0.016)
        except KeyboardInterrupt:
            logger.info("shutdown requested")
        finally:
            for ext in reversed(self.extensions):
                ext.on_detach()
            if self.process:
                self.process.close()


def main() -> int:
    parser = argparse.ArgumentParser(prog="ron-bptrainer")
    parser.add_argument("--dry-run", action="store_true", help="skip process attach")
    parser.add_argument("--log-dir", default="logs")
    args = parser.parse_args()
    configure_logging(Path(args.log_dir))
    build_host(dry_run=args.dry_run).run()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())