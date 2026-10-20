"""Byte patterns for Ready or Not: Boiling Point 1.0.3."""
from __future__ import annotations

# Signature strings use '?' as wildcard nibbles, matching pymem's pattern format.
HEALTH_WRITE_PATTERN = "48 89 5C 24 ? 57 48 83 EC 20 48 8B D9 E8 ? ? ? ?"
AMMO_COUNTER_PATTERN = "89 87 ? ? ? ? 8B 87 ? ? ? ? 85 C0 74 ?"
RECOIL_VECTOR_PATTERN = "F3 0F 11 87 ? ? ? ? F3 0F 11 8F ? ? ? ?"
VELOCITY_VECTOR_PATTERN = "F3 0F 11 87 ? ? ? ? F3 0F 11 8F ? ? ? ? F3 0F 11 97"
ENTITY_LIST_PATTERN = "48 8B 0D ? ? ? ? 48 8B 01 48 8B 80 ? ? ? ? 48 FF 60 20"

PATTERNS = {
    "health_write": HEALTH_WRITE_PATTERN,
    "ammo_counter": AMMO_COUNTER_PATTERN,
    "recoil_vector": RECOIL_VECTOR_PATTERN,
    "velocity_vector": VELOCITY_VECTOR_PATTERN,
    "entity_list": ENTITY_LIST_PATTERN,
}