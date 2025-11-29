#!/usr/bin/env python3
import argparse
import json
import re
import sys
import os
import yaml

def main():
    parser = argparse.ArgumentParser(description="IfThisThenThat: Ensure file changes are accompanied by other file changes.")
    parser.add_argument('filenames', nargs='*', help='Filenames to check')
    parser.add_argument('--config', default='.ifthisthenthat.yaml', help='Config file path (default: .ifthisthenthat.yaml)')
    args = parser.parse_args()

    if not os.path.exists(args.config):
        print(f"Error: Config file '{args.config}' not found.")
        return 1

    with open(args.config, 'r') as f:
        try:
            config = yaml.safe_load(f)
        except yaml.YAMLError as e:
            print(f"Error parsing {args.config}: {e}")
            return 1

    changed_files = set(args.filenames)
    errors = []

    for rule in config.get('rules', []):
        name = rule.get('name', 'Unnamed rule')
        if_pattern = rule.get('if_changed')
        then_pattern = rule.get('then_change')

        if not if_pattern or not then_pattern:
            continue

        try:
            if_regex = re.compile(if_pattern)
        except re.error as e:
            print(f"Error compiling regex '{if_pattern}' in rule '{name}': {e}")
            return 1

        for filename in changed_files:
            match = if_regex.fullmatch(filename) # Use fullmatch or search? usually paths are full. search is safer? Let's use search but anchor if needed.
            # Actually, usually we match the whole path relative to root.
            # Let's use search.
            match = if_regex.search(filename)

            if match:
                # Calculate the expected accompanying file
                try:
                    expected_file = match.expand(then_pattern)
                except re.error:
                    expected_file = then_pattern

                # Check if the expected file is also in the list of changed files
                if expected_file not in changed_files:
                    errors.append(f"Rule '{name}': File '{filename}' was modified. You must also modify '{expected_file}'.")

    if errors:
        for err in errors:
            print(err)
        return 1

    return 0

if __name__ == '__main__':
    sys.exit(main())
