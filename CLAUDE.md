# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a collection of custom [pre-commit](https://pre-commit.com) hooks. The hooks are defined in `.pre-commit-hooks.yaml`. Shell implementations live in `scripts/`; the Python JSON Schema hook lives in `check_json_schema_meta.py`.

## Development Commands

```bash
# Run all prek hooks on all files
prek run --all-files

# Run a specific hook on all files
prek run --all-files <hook-id>

# Run Python tests
uv run --python 3.12 --locked pytest

# Build the Python package
uv build

# Update hooks to latest versions (with frozen revisions)
prek update --freeze

# Install hooks locally
prek install
```

## Architecture

- **`.pre-commit-hooks.yaml`**: Hook definitions that consumers reference. Uses `keep-sorted` directives to maintain alphabetical order.
- **`scripts/`**: Shell script implementations. All scripts use `#!/usr/bin/env bash` and `set -euo pipefail`.
- **`check_json_schema_meta.py`**: JSON Schema validator and CLI. Preserve `--strict` and `--expand-env-vars` behavior.
- **`pyproject.toml`** and **`uv.lock`**: Python packaging and locked dependencies. The distribution and CLI retain the `check-json-schema-meta` name.
- **`tests/`**: Python validator and CLI tests.
- **`.pre-commit-config.yaml`**: This repo's own prek configuration, used for self-validation and CI.

## Adding New Hooks

1. For shell hooks, create the script in `scripts/` with portable bash shebang (`#!/usr/bin/env bash`)
2. Add the hook definition to `.pre-commit-hooks.yaml` within the `keep-sorted` block
3. Update `README.md` with hook documentation

## CI

- **prek.yml**: Runs prek hooks on all files
- **ls-lint.yml**: Validates file naming conventions
- **pytest.yml**: Runs Python tests and builds the package

The `just-format` hook is skipped in CI (prek) because `just` is not available there.
