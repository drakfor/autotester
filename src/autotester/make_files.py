from pathlib import Path
import logging


from autotester.format import GeneratedTests
from autotester.generate_tests.generate_cpp import generate_cpp


logger = logging.getLogger(__name__)


GENERATE_FUNCS = {
    ".cpp": generate_cpp
}


def write_tests_file(testing_files: list[Path], tests: GeneratedTests, test_file_name = None):

    # записывает тестовый файл
    # и возвращает его название

    ext = Path(testing_files[0]).suffix

    tests_code = GENERATE_FUNCS[ext](tests, f"{testing_files[0].name}")

    if test_file_name is None:
        test_file_name = (
            f"{testing_files[0].name.replace(ext, "")}_tests{ext}")

    logger.info(f"Create testing file: {test_file_name}")
    with open(f"{test_file_name}", "w") as f:
        f.write(tests_code)

    return test_file_name, ext