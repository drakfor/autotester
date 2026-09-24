from pathlib import Path
import logging


from autotester.compile.cpp_compiler import CppCompiler
from autotester.scanner import get_testing_files, setup_parser
from autotester.llm_settings import get_tests, setup_model
from autotester.make_files import write_tests_file


logging.basicConfig(level=logging.INFO)


logger = logging.getLogger(__name__)


def main():
    parser = setup_parser()

    if parser.parse_args().command == "setup":
        setup_model('qwen2.5-coder:14b')
        return


    testing_files = get_testing_files(parser)

    if not testing_files:
        raise FileNotFoundError("No tests file found.")

    tests = get_tests(testing_files)

    testing_file_name, ext = write_tests_file(testing_files, tests)

    compiler = CppCompiler()

    if compiler.compile(
        testing_file_name,
        testing_file_name.replace(ext, ""),
    ):
        compiler.run(str(Path.cwd() / testing_file_name))






if __name__ == '__main__':
    main()