#!/usr/bin/env bash
set -euo pipefail

if ! command -v check-jsonschema /dev/null 2>&1; then
    echo >&2 "no check-jsonschema binary found; skipping"
    exit 0
fi

for file in "$@"; do
  schema="$(jq -r '."$schema"' "$file")"
  if [[ -z "$schema" || "$schema" == "null" ]]; then
    echo "✖ $file: no \$schema key"; exit 1
  fi
  check-jsonschema --schemafile "$schema" "$file"
done
