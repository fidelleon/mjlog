import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from mjlog.cli import cli  # noqa: E402


def main():
    cli()


if __name__ == "__main__":
    main()
