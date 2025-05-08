#!/usr/bin/env python
import argparse
import subprocess
import sys
from typing import List, Set, Tuple


def get_modified_files() -> Set[str]:
    """Get the list of files that are modified in this commit."""
    try:
        # This command shows the files that are staged for commit
        result = subprocess.run(
            ["git", "diff", "--cached", "--name-only", "--diff-filter=ACM"],
            capture_output=True,
            text=True,
            check=True,
        )
        return {f.strip() for f in result.stdout.splitlines() if f.strip().endswith(".py")}
    except subprocess.CalledProcessError:
        print("Error: Failed to get modified files from git.", file=sys.stderr)
        return set()


def run_mypy(args: List[str]) -> Tuple[int, List[str]]:
    """Run mypy and return its exit code and output lines."""
    try:
        result = subprocess.run(
            ["python3", "-m", "mypy"] + args,
            capture_output=True,
            text=True,
        )
        return result.returncode, result.stdout.splitlines()
    except FileNotFoundError:
        print("Error: mypy command not found. Please make sure mypy is installed.", file=sys.stderr)
        return 1, []


def filter_output_for_committed_files(lines: List[str], committed_files: Set[str]) -> List[str]:
    """Filter mypy output to only include lines from committed files."""
    filtered_lines = []
    for line in lines:
        # Check if the line starts with a file path that's in our committed files
        for committed_file in committed_files:
            if line.startswith(committed_file + ":"):
                filtered_lines.append(line)
                break
    return filtered_lines


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("files", nargs="*", help="Files to check (ignored, we always check all staged files)")
    parser.add_argument("--show-all-errors", action="store_true", help="Show all errors, not just from committed files")
    args, mypy_args = parser.parse_known_args()

    # Get the list of files being committed
    committed_files = get_modified_files()
    if not committed_files:
        print("No Python files being committed.")
        return 0

    # Run mypy on all files (for proper module resolution)
    exit_code, output_lines = run_mypy(mypy_args)
    
    # If mypy succeeded, no need to filter
    if exit_code == 0:
        return 0
    
    # Filter the output to only show errors from committed files
    if not args.show_all_errors:
        filtered_lines = filter_output_for_committed_files(output_lines, committed_files)
        
        # If there are no errors in committed files, consider it a success
        if not filtered_lines:
            return 0
        
        # Print only errors from committed files
        for line in filtered_lines:
            print(line)
        return 1
    else:
        # Print all errors if requested
        for line in output_lines:
            print(line)
        return exit_code


if __name__ == "__main__":
    sys.exit(main()) 