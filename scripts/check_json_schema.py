#!/usr/bin/env python3
import json
import sys
from pathlib import Path
from check_jsonschema import main as check_jsonschema_main


def main():
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
            check_jsonschema_main(["--schemafile", schema, file_path])
        except SystemExit as e:
            if e.code != 0:
                sys.exit(1)


if __name__ == "__main__":
    main()
