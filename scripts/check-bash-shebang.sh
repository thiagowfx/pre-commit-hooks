#!/usr/bin/env bash
# Check that bash scripts use "#!/usr/bin/env bash" instead of "#!/bin/bash"
# for better portability and access to newer bash versions.

set -euo pipefail

rc=0
for file in "$@"; do
    if [[ -f "$file" ]]; then
        # Read the first line of the file
        first_line=$(head -n 1 "$file")

        # Check if it's a bash script with a direct path shebang
        if [[ "$first_line" =~ ^#!/bin/bash ]]; then
            echo "error: '$file' uses '#!/bin/bash' instead of '#!/usr/bin/env bash'"
            rc=1
        fi
    fi
done

exit "$rc"
