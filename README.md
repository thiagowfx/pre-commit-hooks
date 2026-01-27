# thiagowfx's pre-commit hooks

A collection of [pre-commit](https://pre-commit.com) hooks.

## CI status

`> grep -Erl '\b(push|schedule|workflow_dispatch):$' .github/workflows | xargs -n 1 basename | sort -d | sed 's|^[^/]*$|[![&](https://github.com/thiagowfx/pre-commit-hooks/actions/workflows/&/badge.svg)](https://github.com/thiagowfx/pre-commit-hooks/actions/workflows/&)|'`

<!-- BEGIN mdsh -->
[![ls-lint.yml](https://github.com/thiagowfx/pre-commit-hooks/actions/workflows/ls-lint.yml/badge.svg)](https://github.com/thiagowfx/pre-commit-hooks/actions/workflows/ls-lint.yml)
[![pre-commit.yml](https://github.com/thiagowfx/pre-commit-hooks/actions/workflows/pre-commit.yml/badge.svg)](https://github.com/thiagowfx/pre-commit-hooks/actions/workflows/pre-commit.yml)
<!-- END mdsh -->

## Installation

To use these hooks, you'll need to have `pre-commit` installed. You can install
it using `pip`:

```bash
pip install pre-commit
```

Or using Homebrew on macOS:

```bash
brew install pre-commit
```

## Usage

Add the following to your `.pre-commit-config.yaml` file:

```yaml
repos:
  - repo: https://github.com/thiagowfx/pre-commit-hooks
    rev: {tag}  # Replace with the latest tag
    hooks:
      - id: check-blank-first-line
      - id: check-bash-shebang
      - id: check-yaml-language-server
      - id: check-yamlschema-local
      - id: forbid-colon-filenames
      - id: just-format
      - id: pint
      - id: sort-codeowners-sections
```

Then, run `pre-commit autoupdate` to update the hooks to the latest version and
`pre-commit install` to install the hooks in your local repository.

## Available Hooks

### check-blank-first-line

This hook ensures text files do not have a blank first line. It automatically
removes blank first lines when the hook is triggered, maintaining consistency
in file formatting across the repository.

### check-bash-shebang

This hook ensures bash scripts use the portable shebang `#!/usr/bin/env bash`
instead of `#!/bin/bash`. Using `#!/usr/bin/env bash` provides better
portability across different systems and allows access to newer bash versions
installed via package managers (e.g., Homebrew on macOS), rather than being
locked to outdated system bash versions.

### check-yaml-language-server

This hook checks that YAML files include a `# yaml-language-server: $schema=`
directive at the top of the file. This directive enables IDE support for YAML
schema validation and autocompletion, improving the developer experience when
editing YAML configuration files.

### check-yamlschema-local

This hook checks that YAML files use local schema references instead of remote
(HTTP/HTTPS) URLs. This prevents potential issues with network availability,
security concerns, and checks faster validation by requiring schemas to be
stored locally.

### forbid-colon-filenames

This hook forbids filenames containing colons (`:`). This is useful to prevent
issues with filesystems that do not support colons in filenames.

### just-format (format-justfiles)

This hook formats `Justfiles` using `just --fmt`. It requires [just](https://just.systems) to be
installed and available in your `PATH`.

### pint

This hook validates Prometheus rules with [pint](https://cloudflare.github.io/pint/).

### sort-codeowners-sections

This hook sorts `[section]` blocks alphabetically in CODEOWNERS-style files. It
preserves the header (comments, settings, and global owners before the first
section) while ensuring all `[filename]` sections are in alphabetical order.

## See also

- https://github.com/Lucas-C/pre-commit-hooks
- https://github.com/jumanjihouse/pre-commit-hooks
