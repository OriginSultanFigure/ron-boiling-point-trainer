"""Thin wrapper over pymem for the Ready or Not process."""
from __future__ import annotations

from dataclasses import dataclass

import pymem
import pymem.process
from loguru import logger

PROCESS_NAME = "ReadyOrNot-Win64-Shipping.exe"


@dataclass
class GameProcess:
    pid: int
    base: int
    handle: pymem.Pymem

    @classmethod
    def discover(cls) -> "GameProcess | None":
        try:
            pm = pymem.Pymem(PROCESS_NAME)
        except pymem.exception.ProcessNotFound:
            return None
        module = pymem.process.module_from_name(pm.process_handle, PROCESS_NAME)
        if module is None:
            logger.warning("module handle missing")
            return None
        return cls(pid=pm.process_id, base=module.lpBaseOfDll, handle=pm)

    def read(self, address: int, size: int) -> bytes:
        return self.handle.read_bytes(address, size)

    def write(self, address: int, data: bytes) -> None:
        self.handle.write_bytes(address, data, len(data))

    def close(self) -> None:
        try:
            self.handle.close_process()
        except Exception:
            pass