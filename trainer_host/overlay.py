"""Simple pygame overlay for toggles — click-through via Win32."""
from __future__ import annotations

import pygame
from loguru import logger

from trainer_host.state import TrainerState

WIDTH, HEIGHT = 320, 220
BG = (14, 16, 20, 180)
FG = (230, 240, 255)
ACCENT = (255, 96, 64)


class Overlay:
    def __init__(self, title: str = "Boiling Point Trainer") -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.NOFRAME)
        pygame.display.set_caption(title)
        self.font = pygame.font.SysFont("consolas", 14)
        self.clock = pygame.time.Clock()

    def draw(self, state: TrainerState) -> None:
        self.screen.fill(BG)
        rows = [
            ("GODMODE", state.godmode),
            ("INF AMMO", state.infinite_ammo),
            ("NO RECOIL", state.no_recoil),
            ("SUPER SPEED", state.super_speed),
        ]
        for i, (label, on) in enumerate(rows):
            color = ACCENT if on else FG
            surf = self.font.render(f"[{'x' if on else ' '}] {label}", True, color)
            self.screen.blit(surf, (16, 20 + i * 26))
        pygame.display.flip()
        self.clock.tick(60)

    def close(self) -> None:
        pygame.quit()
        logger.debug("overlay closed")