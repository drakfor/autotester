from autotester.format import GeneratedTests, Argument


import json


def to_cpp_value(arg: Argument) -> str:
    if arg.type == "int":
        return str(arg.value)

    if arg.type in ("float", "double"):
        return str(arg.value)

    if arg.type == "bool":
        return "true" if arg.value else "false"

    if arg.type == "string":
        return f'"{arg.value}"'

    if arg.type == "char":
        return f"'{arg.value}'"

    if arg.type == "vector<int>":
        values = arg.value
        print(arg.value)
        print(type(arg.value))

        if isinstance(values, str):
            values = json.loads(values)

        print(values)
        print(type(values))

        values = ", ".join(map(str, values))
        return f"std::vector<int>{{{values}}}"

    raise ValueError(f"Unsupported type: {arg.type}")


def generate_cpp(tests: GeneratedTests, solution_file: str) -> str:
    result = []

    result.append('#include <gtest/gtest.h>')
    result.append('#include <vector>')
    result.append('#include <string>')
    result.append(f'#include "{solution_file}"')
    result.append("")

    for function_tests in tests.functions:
        for test in function_tests.tests:
            args = ", ".join(
                to_cpp_value(arg)
                for arg in test.args
            )

            expected = to_cpp_value(test.expected)

            result.append(
                f"TEST({function_tests.function}Tests, {test.name}) {{"
            )

            result.append(
                f"    EXPECT_EQ("
                f"{function_tests.function}({args}), "
                f"{expected}"
                f");"
            )

            result.append("}")
            result.append("")

    return "\n".join(result)