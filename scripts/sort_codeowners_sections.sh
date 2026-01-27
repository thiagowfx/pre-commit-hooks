#!/usr/bin/env bash
set -euo pipefail

# Sort [section] blocks in CODEOWNERS-style files alphabetically
# Preserves header (everything before the first [section])
# Each section consists of a [filename] line followed by owner lines
#
# Example input:
#
#   # Comment header
#   set inherit = false
#
#   @org/platform
#
#   [zebra.yaml]
#   @org/team-z
#
#   [apple.yaml]
#   @org/team-a
#
# Example output (sorted):
#
#   # Comment header
#   set inherit = false
#
#   @org/platform
#
#   [apple.yaml]
#   @org/team-a
#
#   [zebra.yaml]
#   @org/team-z

fix_mode=false
if [[ "${1:-}" == "--fix" ]]; then
  fix_mode=true
  shift
fi

failed=0

sort_file() {
  local file="$1"
  local tmpdir
  tmpdir=$(mktemp -d)
  # shellcheck disable=SC2064  # We want $tmpdir to expand now, not at signal time
  trap "rm -rf '$tmpdir'" RETURN

  # Parse file: extract header and sections to separate files
  # Normalize sections: strip trailing blank lines, we'll add them back consistently
  awk -v tmpdir="$tmpdir" '
    BEGIN {
      in_header = 1
      section_key = ""
      section_lines[0] = ""
      section_count = 0
    }

    /^\[.*\]$/ {
      # Save previous section if any
      if (section_key != "") {
        fname = section_key
        gsub(/[\[\]]/, "", fname)
        # Trim trailing empty lines
        while (section_count > 0 && section_lines[section_count] == "") {
          section_count--
        }
        for (i = 1; i <= section_count; i++) {
          print section_lines[i] > (tmpdir "/" fname)
        }
        close(tmpdir "/" fname)
      }
      in_header = 0
      section_key = $0
      section_count = 1
      section_lines[1] = $0
      next
    }

    in_header {
      print >> (tmpdir "/000_HEADER")
      next
    }

    {
      section_count++
      section_lines[section_count] = $0
    }

    END {
      if (section_key != "") {
        fname = section_key
        gsub(/[\[\]]/, "", fname)
        while (section_count > 0 && section_lines[section_count] == "") {
          section_count--
        }
        for (i = 1; i <= section_count; i++) {
          print section_lines[i] > (tmpdir "/" fname)
        }
      }
    }
  ' "$file"

  # Output header
  [[ -f "$tmpdir/000_HEADER" ]] && cat "$tmpdir/000_HEADER" && rm "$tmpdir/000_HEADER"

  # Sort section files by name and output with blank line between each
  local first=true
  for section_file in $(find "$tmpdir" -type f -print0 | sort -z | xargs -0 -n1 basename 2>/dev/null); do
    if [[ "$first" != true ]]; then
      echo ""
    fi
    first=false
    cat "$tmpdir/$section_file"
  done
}

for file in "$@"; do
  [[ -f "$file" ]] || continue

  sorted_content=$(sort_file "$file")
  # Command substitution strips trailing newlines, so comparison is normalized
  original_content=$(cat "$file")

  if [[ "$sorted_content" != "$original_content" ]]; then
    if [[ "$fix_mode" == true ]]; then
      printf '%s\n' "$sorted_content" > "$file"
      echo "Fixed: $file"
    else
      echo "Not sorted: $file"
      failed=1
    fi
  fi
done

exit "$failed"
