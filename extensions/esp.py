"""ESP — draws enemy positions as world-to-screen boxes via the overlay."""
from __future__ import annotations

from trainer_host.contracts import TrainerExtension
from trainer_host.hotkeys import HotkeyBus
from trainer_host.state import TrainerState
from offsets.patterns import ENTITY_LIST_PATTERN
from offsets.resolver import resolve_pattern


class EspExtension(TrainerExtension):
    NAME = "esp"
    VERSION = "0.6.0"
    REQUIRES_BUILD = "1.0.3-boilingpoint"
    DEFAULT_ENABLED = False

    def __init__(self) -> None:
        self.hotkey = "f5"
        self.max_distance = 200.0
        self._entity_list: int | None = None
        self._state: TrainerState | None = None

    def on_attach(self, state: TrainerState, hotkeys: HotkeyBus) -> None:
        self._state = state
        self._entity_list = resolve_pattern(state.process, ENTITY_LIST_PATTERN)
        hotkeys.bind(self.hotkey, self._toggle)

    def _toggle(self) -> None:
        if not self._state:
            return
        current = self._state.extras.get("esp_on", False)
        self._state.extras["esp_on"] = not current

    def tick(self, state: TrainerState) -> None:
        if not state.extras.get("esp_on") or self._entity_list is None:
            return
        # entity iteration happens in overlay.draw via state.extras["esp_boxes"]
        state.extras.setdefault("esp_boxes", [])