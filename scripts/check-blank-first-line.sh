#!/usr/bin/env bash
set -euo pipefail

# Check and fix blank first lines in text files
# If --fix flag is provided, remove blank first lines; otherwise just report

fix_mode=false
if [[ "${1:-}" == "--fix" ]]; then
  fix_mode=true
  shift
fi

failed=0

for file in "$@"; do
  # Skip binary files
  if file "$file" | grep -q "binary"; then
    continue
  fi

  # Check if first line is blank
  if [[ -f "$file" ]] && [[ -s "$file" ]]; then
    first_line=$(head -n 1 "$file")
    if [[ -z "$first_line" ]]; then
      if [[ "$fix_mode" == true ]]; then
        # Remove blank first line
        tail -n +2 "$file" > "$file.tmp" && mv "$file.tmp" "$file"
        echo "✓ $file: removed blank first line"
      else
        echo "❌ $file: first line is blank"
        failed=1
      fi
    fi
  fi
done

exit "$failed"
