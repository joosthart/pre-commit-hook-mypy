# Examples

This directory contains examples to demonstrate the use of the `pre-commit-hook-mypy` package.

## Files

- `pre-commit-config.yaml`: An example pre-commit configuration file that uses the hook.
- `good_file.py`: A Python file with correct type annotations that passes mypy checks.
- `bad_file.py`: A Python file with a type error that will be caught by mypy.

## Usage

You can use these files to test the hook functionality:

1. Copy the `pre-commit-config.yaml` to your project's root directory.
2. Run `pre-commit install` to set up the hooks.
3. Make some changes to Python files and try committing them.

## Expected Behavior

- If you make changes to a file like `good_file.py`, the commit will succeed because there are no type errors.
- If you make changes to a file like `bad_file.py`, the commit will fail because mypy will detect the type error.
- If you have type errors in files that you're not committing, the commit will succeed because the hook only checks files that are being committed. 