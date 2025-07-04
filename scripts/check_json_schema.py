#!/usr/bin/env python3
import json
import sys
from check_jsonschema import main as check_jsonschema_main


def main():
    for file_path in sys.argv[1:]:
        with open(file_path, 'r') as f:
            data = json.load(f)

        schema = data["$schema"]
        check_jsonschema_main(["--schemafile", schema, file_path])


if __name__ == "__main__":
    main()
