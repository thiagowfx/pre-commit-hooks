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

                # Forward check
                for filename in changed_files:
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

                        # Reverse check (if bidi)
                        if rule.get('bidi', False):                    # Check if then_pattern is static (no backreferences like \1, \g<1>)
                    is_static_target = '\\' not in then_pattern

                    if is_static_target:
                        if then_pattern in changed_files:
                            # If target matches, we expect ANY file matching if_pattern to be changed
                            # This is slightly loose but safe for "A <-> B" or "Any matching A <-> B"
                            if not any(if_regex.search(f) for f in changed_files):
                                 errors.append(f"Rule '{name}' (Reverse): File '{then_pattern}' was modified. You must also modify a file matching '{if_pattern}'.")
                                else:
                                    print(f"Warning: Rule '{name}' is marked bidi but has a dynamic target '{then_pattern}'. Reverse check skipped.", file=sys.stderr)    if errors:
        for err in errors:
            print(err)
        return 1

    return 0

if __name__ == '__main__':
    sys.exit(main())
