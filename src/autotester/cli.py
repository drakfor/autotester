from pathlib import Path
import logging


from autotester.generate_cpp import generate_cpp
from autotester.cpp_compiler import CppCompiler
from autotester.scanner import get_testing_file
from autotester.llm_settings import get_tests


logging.basicConfig(level=logging.INFO)


logger = logging.getLogger(__name__)


def main():
    testing_file = get_testing_file()

    tests = get_tests(testing_file)

    tests_cpp = generate_cpp(tests, f"{testing_file.name}")

    # имя файла без расширения
    testing_file_name = testing_file.name.replace(".cpp", "")

    with open(f"{testing_file_name}_tests.cpp", "w") as file:
        file.write(tests_cpp)

    logger.info(f"Compiling {testing_file_name}_tests.cpp")
    compiler = CppCompiler()

    if compiler.compile(
        f"{testing_file_name}_tests.cpp",
        f"{testing_file_name}_tests"
    ):
        compiler.run(str(Path.cwd() / f"{testing_file_name}_tests"))






if __name__ == '__main__':
    main()