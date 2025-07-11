#!/usr/bin/env bash
set -euo pipefail

if ! command -v just /dev/null 2>&1; then
    echo >&2 "error: no just binary found"
    exit 1
fi

rc=0
for file in "$@"; do
    if ! just --fmt --unstable --check -f "$file" >/dev/null 2>&1; then
        echo >&2 "fixing ${file}"
        just --fmt --unstable -f "$file" >/dev/null 2>&1
        rc=1
    fi
done

exit "$rc"
