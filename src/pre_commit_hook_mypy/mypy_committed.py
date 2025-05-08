#!/usr/bin/env python
import argparse
import subprocess
import sys


def get_modified_files() -> set[str]:
    try:
        result = subprocess.run(
            ["git", "diff", "--cached", "--name-only", "--diff-filter=ACM"],
            capture_output=True,
            text=True,
            check=True,
        )
        return {
            f.strip() for f in result.stdout.splitlines() if f.strip().endswith(".py")
        }
    except subprocess.CalledProcessError:
        print("Error: Failed to get modified files from git.", file=sys.stderr)
        return set()


def run_mypy(args: list[str]) -> tuple[int, list[str]]:
    try:
        result = subprocess.run(
            ["python3", "-m", "mypy"] + args,
            capture_output=True,
            text=True,
        )
        return result.returncode, result.stdout.splitlines()
    except FileNotFoundError:
        print(
            "Error: mypy command not found. Please make sure mypy is installed.",
            file=sys.stderr,
        )
        return 1, []


def filter_output_for_committed_files(
    lines: list[str], committed_files: set[str]
) -> list[str]:
    filtered_lines = []

    normalized_committed_files = {f.replace("\\", "/") for f in committed_files}

    for line in lines:
        line_normalized = line.replace("\\", "/")

        for committed_file in normalized_committed_files:
            parts = line_normalized.split(":", 2)
            if len(parts) >= 2 and parts[0] == committed_file:
                filtered_lines.append(line)
                break

    return filtered_lines


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "files",
        nargs="*",
        help="Files to check (ignored, we always check all staged files)",
    )
    parser.add_argument(
        "--show-all-errors",
        action="store_true",
        help="Show all errors, not just from committed files",
    )
    args, mypy_args = parser.parse_known_args()
    committed_files = get_modified_files()
    if not committed_files:
        print("No Python files being committed.")
        return 0

    input_files = args.files if args.files else list(committed_files)

    exit_code, output_lines = run_mypy(mypy_args + input_files)

    if exit_code == 0:
        return 0

    if not args.show_all_errors:
        filtered_lines = filter_output_for_committed_files(
            output_lines, committed_files
        )

        if not filtered_lines:
            return 0

        for line in filtered_lines:
            print(line)
        return 1
    else:
        for line in output_lines:
            print(line)
        return exit_code


if __name__ == "__main__":
    sys.exit(main())
