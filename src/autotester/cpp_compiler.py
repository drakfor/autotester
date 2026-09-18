import subprocess
from pathlib import Path


AUTOTESTER_ROOT = Path(__file__).resolve().parents[2]
GTEST_ROOT = AUTOTESTER_ROOT / "googletest"
gtest_include = GTEST_ROOT / "googletest" / "include"
gtest_lib = GTEST_ROOT / "build" / "lib"


class CppCompiler:
    def compile(
        self,
        test_file: str,
        # solution_file: str,
        # header_file: str,
        output_file: str = "tests",
    ) -> bool:

        result = subprocess.run(
            [
                "g++",
                f"-I{gtest_include}",
                f"-L{gtest_lib}",
                test_file,
                # solution_file,
                # header_file,
                "-std=c++20",
                "-lgtest",
                "-lgtest_main",
                "-pthread",
                "-o",
                output_file
            ],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            print(result.stderr)
            return False

        return True


    def run(self, executable: str):
        result = subprocess.run(
            [executable],
            # capture_output=True,   вывод в переменную а не в консоль
            text=True,
            timeout=5
        )

        return result.returncode