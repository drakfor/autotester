import argparse
from pathlib import Path


def get_testing_file() -> Path:
    parser = argparse.ArgumentParser(
        description="Automatic test generator",
    )

    parser.add_argument(
        "file",
        help="Source file to test"
    )

    args = parser.parse_args()

    testing_file = Path(args.file)

    return testing_file