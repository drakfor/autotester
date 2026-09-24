from pathlib import Path
import logging


from autotester.compile.cpp_compiler import CppCompiler
from autotester.scanner import get_testing_files, get_parser
from autotester.llm_settings import get_tests, setup_model
from autotester.make_files import write_tests_file


logging.basicConfig(level=logging.INFO)


logger = logging.getLogger(__name__)


MODEL_NAME = "qwen2.5-coder:14b"


def main():
    parser = get_parser()
    args = parser.parse_args()


    global MODEL_NAME

    # изменения пользователем
    # модели для тестирования
    if args.command == "setup":
        setup_model(MODEL_NAME)

        if args.model:
            MODEL_NAME = args.model
            setup_model(MODEL_NAME)

        return


    testing_files = get_testing_files(args)

    if not testing_files:
        raise FileNotFoundError("No tests file found.")


    # поулчаем форматированный json файл
    # ответа от llm
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