#!/usr/bin/env bash
# Check the "yaml-language-server" directive is present in YAML files.

set -euo pipefail

for file in "$@"; do
    if [[ -f "$file" ]] && [[ "$file" =~ .yaml$ ]] && ! grep -q "^# yaml-language-server: \$schema=" "$file"; then
        echo "error: missing 'yaml-language-server' directive in '$file'."
        exit 1
    fi
done
