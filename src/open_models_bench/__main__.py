"""Allow running the package with `python -m open_models_bench`."""

from .cli import main

if __name__ == "__main__":
    raise SystemExit(main())
