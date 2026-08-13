"""Thin ``python -m harness`` entrypoint."""

from .cli import main


if __name__ == "__main__":
    raise SystemExit(main())
