"""Allows ``python -m notebook_audit ...`` to work."""

import sys

from .cli import main

if __name__ == "__main__":
    sys.exit(main())
