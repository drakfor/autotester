import argparse
from pathlib import Path


def get_parser() -> argparse.ArgumentParser:

    # обработка команд от пользователя

    parser = argparse.ArgumentParser(
        prog="autotester",
        description="Automatic test generator"
    )

    subparsers = parser.add_subparsers(
        dest="command",
        required=True
    )

    setup_parser = subparsers.add_parser(
        "setup",
        help="Setup Ollama model"
    )

    setup_parser.add_argument(
        "--model",
        "-M",
        default=None,
        help="LLM model name in ollama"
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


def get_testing_files(args) -> list[Path]:

    # аргументы парсинга команд пользователя
    # передаются в функцию для создания списка файлов-исходников
    # для тестирования

    testing_files = [Path(args.file)]

    if args.header:
        testing_files.append(Path(args.header))

    return testing_files