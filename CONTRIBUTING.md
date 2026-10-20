# Contributing to ron-boiling-point-trainer

Thanks for wanting to help. This is a hobbyist trainer for **Ready or Not: Boiling Point** — a single-player / private-server cheat tool. Keep pull requests focused and small.

## Ground rules

- **Single-player / private servers only.** Do not submit anything that targets public matchmaking.
- Test your change against the current Steam build before opening a PR. Note the build hash in the PR description.
- Follow the plugin host contract in `trainer_host/contracts.py`. Extensions live under `extensions/` and are loaded dynamically.
- Do not hardcode offsets. Resolve them via `offsets/resolver.py` or add a pattern to `offsets/patterns.py`.

## Dev setup

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python -m trainer_host.host --dry-run
```

## Extension checklist

- [ ] Subclass `TrainerExtension`
- [ ] Declare `NAME`, `VERSION`, `REQUIRES_BUILD`
- [ ] Register hotkeys through `self.hotkeys.bind(...)`
- [ ] Add a test in `tests/`
- [ ] Update `extensions/registry.json` if shipping default-on

## Style

- Python 3.11+, type hints everywhere.
- `ruff` and `black` defaults. No tabs.
- Log through `loguru`, never `print` (except in `tools/`).

## Reporting bugs

Open an issue with: game build hash, Windows version, which extensions were enabled, and the last 40 lines of `logs/trainer.log`.