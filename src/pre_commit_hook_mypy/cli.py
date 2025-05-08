#!/usr/bin/env python
import sys
from pre_commit_hook_mypy.mypy_committed import main


def cli() -> None:
    sys.exit(main())


if __name__ == "__main__":
    cli()
