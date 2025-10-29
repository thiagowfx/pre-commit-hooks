# thiagowfx's pre-commit hooks

A collection of [pre-commit](https://pre-commit.com) hooks.

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
      - id: check-yamlschema-local
      - id: forbid-colon-filenames
      - id: just-format
      - id: pint
```

Then, run `pre-commit autoupdate` to update the hooks to the latest version and
`pre-commit install` to install the hooks in your local repository.

## Available Hooks

### check-yamlschema-local

This hook ensures that YAML files use local schema references instead of remote
(HTTP/HTTPS) URLs. This prevents potential issues with network availability,
security concerns, and ensures faster validation by requiring schemas to be
stored locally.

### forbid-colon-filenames

This hook forbids filenames containing colons (`:`). This is useful to prevent
issues with filesystems that do not support colons in filenames.

### just-format (format-justfiles)

This hook formats `Justfiles` using `just --fmt`. It requires [just](https://just.systems) to be
installed and available in your `PATH`.

### pint

This hook validates Prometheus rules with [pint](https://cloudflare.github.io/pint/).
