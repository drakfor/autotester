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


# def to_cpp_type(arg_type: str) -> str:
#     types = {
#         "int": "int",
#         "double": "double",
#         "float": "float",
#         "bool": "bool",
#         "char": "char",
#         "string": "std::string",
#         "vector<int>": "std::vector<int>"
#     }
#
#     if arg_type not in types:
#         raise ValueError(f"Unsupported type: {arg_type}")
#
#     return types[arg_type]


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


# def generate_header(
#     generated_tests: GeneratedTests
# ) -> str:
#
#     includes = set()
#     declarations = []
#
#     for function in generated_tests.functions:
#
#         if not function.tests:
#             raise ValueError(
#                 f"Function '{function.function}' has no tests"
#             )
#
#         # Определяем возвращаемый тип
#         return_type = to_cpp_type(
#             function.tests[0].expected.type
#         )
#
#         arguments = []
#
#         for arg in function.formal_args:
#             cpp_type = to_cpp_type(arg.type)
#
#             # Здесь arg.value — имя формального аргумента
#             arguments.append(
#                 f"{cpp_type} {arg.value}"
#             )
#
#             if arg.type == "string":
#                 includes.add("#include <string>")
#
#             elif arg.type == "vector<int>":
#                 includes.add("#include <vector>")
#
#         expected_type = function.tests[0].expected.type
#
#         if expected_type == "string":
#             includes.add("#include <string>")
#
#         elif expected_type == "vector<int>":
#             includes.add("#include <vector>")
#
#         args_string = ", ".join(arguments)
#
#         declarations.append(
#             f"{return_type} {function.function}({args_string});"
#         )
#
#     lines = []
#
#     if includes:
#         lines.extend(sorted(includes))
#         lines.append("")
#
#     lines.extend(declarations)
#     lines.append("")
#
#     return '\n'.join(lines)