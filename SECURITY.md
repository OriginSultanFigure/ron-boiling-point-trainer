# Security Policy

## Scope

This repository ships memory-editing code for **Ready or Not: Boiling Point**. That is inherently sensitive. We treat the following as security-relevant:

- Any code path that can touch a process other than the target game.
- Any extension that opens a network socket.
- Signature / offset resolution that could false-positive on anti-cheat or system processes.
- Loader code that executes arbitrary files from disk.

## Reporting

Do **not** open public issues for security problems. Email `security@ron-bptrainer.dev` (PGP key in `SECURITY.asc` on the release page) with:

1. Affected extension or host module.
2. Reproduction steps.
3. Impact assessment (local only? network? persistence?).

We aim to acknowledge within 72 hours. Fixes ship in the next tagged release; the reporter is credited unless they ask otherwise.

## Out of scope

- Detection by anti-cheat on public servers. Using this tool online is against ToS and is not something we will "fix".
- Crashes from mismatched game builds — those are handled as normal bugs.