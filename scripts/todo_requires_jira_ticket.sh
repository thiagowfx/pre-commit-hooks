#!/usr/bin/env bash
set -euo pipefail

# Fail when newly added comments contain a TODO without a parenthesised JIRA
# issue key (the accepted form writes the key as a single token, following
# JIRA's PROJECT-NUMBER convention, e.g. TODO(PROJ-1234)).
#
# Only newly added lines are checked, via a diff. The range is the PR base in
# CI (PR_BASE_SHA, if set), else the staged index locally. A two-dot tree diff
# is used, so only the base commit needs to be present (no full history).
#
# TODO only, strict JIRA key format, no FIXME/XXX/lowercase -- deliberate.

if [ -n "${PR_BASE_SHA:-}" ]; then
  range="${PR_BASE_SHA}..HEAD"
else
  range="--cached"
fi

added=$(git diff -U0 "$range" | grep -E '^\+' | grep -vE '^\+\+\+' || true)

# Judge each TODO occurrence on its own, so a valid key elsewhere on the line
# can't excuse a bare one.
bad=$(printf '%s\n' "$added" |
  grep -oE '(#|//|/\*|<!--)[[:space:]]*TODO(\([^)]*\))?' |
  grep -vE 'TODO\([A-Z][A-Z0-9]*-[0-9]+\)$' || true)

if [ -n "$bad" ]; then
  echo "Newly added TODO comments must reference a JIRA issue key, e.g. TODO(PROJ-1234):"
  printf '%s\n' "$bad" | sort -u
  exit 1
fi
