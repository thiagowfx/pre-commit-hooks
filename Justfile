alias tag := release

# Release a new version (defaults to auto-incrementing v0.0.N)
release TAG="":
    #!/usr/bin/env bash
    set -euo pipefail

    # Use provided tag or auto-increment
    if [[ -z "{{ TAG }}" ]]; then
        # Get the latest tag matching v0.0.* pattern
        latest_tag=$(git tag -l "v0.0.*" | sort -V | tail -n1)

        if [[ -z "$latest_tag" ]]; then
            # No tags found, start with v0.0.1
            version="v0.0.1"
        else
            # Extract the patch version number
            if [[ "$latest_tag" =~ ^v0\.0\.([0-9]+)$ ]]; then
                patch_version=${BASH_REMATCH[1]}
                next_patch=$((patch_version + 1))
                version="v0.0.$next_patch"
            else
                echo "Error: Unexpected tag format: $latest_tag"
                exit 1
            fi
        fi

        echo "Latest tag: $latest_tag"
        echo "Next tag: $version"
    else
        version="{{ TAG }}"
        echo "Using provided tag: $version"
    fi

    # Check if tag already exists
    if git rev-parse "$version" >/dev/null 2>&1; then
        echo "Error: Tag $version already exists"
        exit 1
    fi

    # Create and push tag
    git tag "$version"
    git push origin "$version"

    echo "✓ Tag $version created and pushed"
