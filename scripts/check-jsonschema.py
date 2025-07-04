#!/usr/bin/env python3
import json
import shutil
import subprocess
import sys
from pathlib import Path


def main():
    if not shutil.which("check-jsonschema"):
        print("no check-jsonschema binary found; skipping", file=sys.stderr)
        sys.exit(0)

    for file_path in sys.argv[1:]:
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f"✖ {file_path}: {e}")
            sys.exit(1)

        schema = data.get("$schema")
        if not schema:
            print(f"✖ {file_path}: no $schema key")
            sys.exit(1)

        try:
            subprocess.run(
                ["check-jsonschema", "--schemafile", schema, file_path],
                check=True
            )
        except subprocess.CalledProcessError:
            sys.exit(1)


if __name__ == "__main__":
    main()
