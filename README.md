# pre-commit-hook-mypy

A pre-commit hook that runs mypy only on files that are being committed.

## Description

This pre-commit hook is similar to the standard mypy-mirrors pre-commit hook, but with one important difference: it only reports errors for files that are being committed. Any mypy errors in other files are ignored.

This is particularly useful when working in large codebases where you want to ensure your changes meet type checking requirements without being blocked by existing type issues in unchanged files.

## Installation

Add this to your `.pre-commit-config.yaml`:

```yaml
-   repo: https://github.com/yourusername/pre-commit-hook-mypy
    rev: v0.1.0  # Use the ref you want to point at
    hooks:
    -   id: mypy-committed
```

## Configuration

The hook supports the same configuration options as the standard mypy hook, such as:

```yaml
-   repo: https://github.com/yourusername/pre-commit-hook-mypy
    rev: v0.1.0
    hooks:
    -   id: mypy-committed
        args: [--strict, --ignore-missing-imports]
        additional_dependencies: ["django-stubs==1.14.0"]
```

## How It Works

The hook:
1. Identifies which Python files are being committed
2. Runs mypy on all Python files (to ensure proper module resolution)
3. Filters the output to only show errors from the committed files
4. Fails if any errors are found in the committed files

## License

MIT 