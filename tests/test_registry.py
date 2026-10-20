from pathlib import Path

from trainer_host.registry import ExtensionRegistry


def test_registry_loads_default_extensions():
    reg = ExtensionRegistry(Path(__file__).resolve().parent.parent / "extensions" / "registry.json")
    modules = {s.module for s in reg.all_specs()}
    assert "extensions.godmode" in modules
    assert "extensions.no_recoil" in modules


def test_enabled_filter():
    reg = ExtensionRegistry(Path(__file__).resolve().parent.parent / "extensions" / "registry.json")
    enabled = {s.module for s in reg.enabled_specs()}
    assert "extensions.godmode" in enabled
    assert "extensions.esp" not in enabled
</br>