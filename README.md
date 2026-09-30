# Hermes Echo

[![npm version](https://img.shields.io/npm/v/@hermes-tools/hermes-echo.svg)](https://www.npmjs.com/package/@hermes-tools/hermes-echo)
[![GitHub release](https://img.shields.io/github/v/release/g1n0mag1k/hermes-echo)](https://github.com/g1n0mag1k/hermes-echo/releases)

Discover what your CLI actually does. Catch behavioral changes your tests missed.

## What it does

Hermes Echo finds your CLI’s console scripts from `setup.py` / `pyproject.toml`, including nested subcommands, and runs them like a user would. You accept the observed exit code, stdout, and stderr as Echo Contracts and commit them. On every pull request it re-runs those probes and comments when behavior drifts — with zero configuration it discovered and locked 30 behavioral contracts on [pypa/hatch](https://github.com/pypa/hatch).

## Quick start (GitHub Actions)

Add this to `.github/workflows/hermes-echo.yml`:

```yaml
name: Hermes Echo
on:
  pull_request:

permissions:
  contents: read
  pull-requests: write

jobs:
  echo:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      # Zero-config (auto-detects your console script):
      - uses: g1n0mag1k/hermes-echo@v0.3.6
      # Explicit:
      # - uses: g1n0mag1k/hermes-echo@v0.3.6
      #   with:
      #     command: myapp
```

`pull-requests: write` is required to post the drift comment on your PR.

`fetch-depth: 0` is required because Hermes Echo executes probes against both the PR branch and its base revision.

Accept contracts locally, commit `.hermes/contracts/`, and PR comments will show contract drift.

Zero configuration against [pypa/hatch](https://github.com/pypa/hatch): Hermes Echo auto-discovered all 30 commands from `pyproject.toml` and locked exit code, stdout, and stderr — for example `hatch env show`:

```yaml
# Echo Contract — accepted 2026-09-30T08:40:33.951Z
probe: env-show
command: hatch env show
accepted_at: '2026-09-30T08:40:33.951Z'
accepted_by: hermes-echo v0.3.5
observations:
  exit_code: 0
  stdout: |
    Standalone
    ┏┳┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┓
    ┃┃┃ Dependencies                           ┃ Environment varia… ┃ Scripts      ┃
    ┡╇╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━┩
    │││ coverage[toml]>=6.2                    │                    │ combine      │
    │││ mypy>=1.0.0                            │                    │ check        │
    │││ mkdocs-material~=9.7.0                 │ PYTHONUNBUFFERED=1 │ serve        │
    # ... 27 more rows
  stderr: null
```

## Handling nondeterministic output

Hermes Echo normalizes timestamps, UUIDs, and absolute paths before comparing observations. Commands that produce different output on every run (daemons, servers, interactive prompts) are automatically skipped.

## Does behavioral drift fail CI?

No. Hermes Echo always exits 0. It reports drift as a PR comment but does not block merging. You decide what to do with the information.

## Local CLI usage

```bash
npm install -g @hermes-tools/hermes-echo
hermes-echo doctor --command myapp
hermes-echo accept
hermes-echo accept validate
```

## How contracts work

- Accepted probes are stored as `.hermes/contracts/*.yml` (names like `env-show`, `fmt-check`)
- Each contract locks exit code, full stdout, and full stderr
- On PRs, Hermes Echo verifies those contracts and posts a drift table plus a git-style stdout/stderr diff

## Compliance

Accepted Echo Contracts are version-controlled records of observed CLI behavior — what exited, what printed, and when you accepted it. Teams with formal software validation requirements may find version-controlled behavioral contracts useful as supporting evidence.

Built by [Hermes Relay](https://hermesrelay.dev)
