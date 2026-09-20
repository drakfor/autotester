import argparse
from pathlib import Path


import argparse


def setup_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="autotester",
        description="Automatic test generator"
    )

    subparsers = parser.add_subparsers(
        dest="command",
        required=True
    )

    subparsers.add_parser(
        "setup",
        help="Setup Ollama model"
    )

    test_parser = subparsers.add_parser(
        "test",
        help="Generate and run tests"
    )

    test_parser.add_argument(
        "source_file",
        help="Path to source file"
    )

    test_parser.add_argument(
        "--header",
        "-H",
        default=None,
        help="Optional path to header file"
    )

    return parser


def get_testing_file(parser: argparse.ArgumentParser) -> list[Path]:
    args = parser.parse_args()

    testing_files = [Path(args.file)]

    if args.header:
        testing_files.append(Path(args.header))

    return testing_files