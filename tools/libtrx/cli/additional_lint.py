#!/usr/bin/env python3
import argparse
import sys
from collections.abc import Iterable
from fnmatch import fnmatch
from pathlib import Path

from libtrx.files import find_versioned_files, is_binary_file
from libtrx.linting import LintContext, lint_bulk_files, lint_file


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=Path, nargs="*")
    parser.add_argument("-D", "--debug", action="store_true")
    return parser.parse_args()


def filter_files(
    files: Iterable[Path], ignored_patterns: list[str] | None, debug: bool
) -> Iterable[Path]:
    for path in files:
        if is_binary_file(path):
            if debug:
                print(f"{path} is a binary file, ignoring", file=sys.stderr)
            continue
        if ignored_patterns and any(
            fnmatch(path.name, pattern) for pattern in ignored_patterns
        ):
            if debug:
                print(
                    f"{path} has a prohibited extension, ignoring",
                    file=sys.stderr,
                )
            continue
        yield path


def run_script(
    root_dir: Path, ignored_patterns: list[str] | None = None
) -> None:
    args = parse_args()

    context = LintContext(
        root_dir=root_dir,
        versioned_files=find_versioned_files(root_dir=root_dir),
    )
    if args.path:
        files = args.path
    else:
        files = context.versioned_files
    files = list(filter_files(files, ignored_patterns, debug=args.debug))

    exit_code = 0
    for file in files:
        if args.debug:
            print(f"Checking {file}...", file=sys.stderr)
        for lint_warning in lint_file(context, file):
            print(str(lint_warning), file=sys.stderr)
            exit_code = 1

    if args.debug:
        print(f"Checking files in bulk {file}...", file=sys.stderr)
    for lint_warning in lint_bulk_files(context, files):
        print(str(lint_warning), file=sys.stderr)
        exit_code = 1

    exit(exit_code)
