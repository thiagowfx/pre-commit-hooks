# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a collection of custom [pre-commit](https://pre-commit.com) hooks implemented as shell scripts. The hooks are defined in `.pre-commit-hooks.yaml` and their implementations live in `scripts/`.

## Development Commands

```bash
# Run all prek hooks on all files
prek run --all-files

# Run a specific hook on all files
prek run --all-files <hook-id>

# Update hooks to latest versions (with frozen revisions)
prek auto-update --freeze

# Install hooks locally
prek install
```

## Architecture

- **`.pre-commit-hooks.yaml`**: Hook definitions that consumers reference. Uses `keep-sorted` directives to maintain alphabetical order.
- **`scripts/`**: Shell script implementations for each hook. All scripts use `#!/usr/bin/env bash` and `set -euo pipefail`.
- **`.pre-commit-config.yaml`**: This repo's own prek configuration, used for self-validation and CI.

## Adding New Hooks

1. Create the script in `scripts/` with portable bash shebang (`#!/usr/bin/env bash`)
2. Add the hook definition to `.pre-commit-hooks.yaml` within the `keep-sorted` block
3. Update `README.md` with hook documentation

## CI

- **prek.yml**: Runs prek hooks on all files
- **ls-lint.yml**: Validates file naming conventions

The `just-format` hook is skipped in CI (prek) because `just` is not available there.
