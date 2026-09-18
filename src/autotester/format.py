from typing import Literal, Any
from pydantic import BaseModel, Field


class Argument(BaseModel):
    type: Literal[
        "int",
        "double",
        "float",
        "bool",
        "char",
        "string",
        "vector<int>"
    ]
    value: Any


class TestCase(BaseModel):
    name: str
    args: list[Argument] = Field(min_length=1)
    expected: Argument


class FunctionTests(BaseModel):
    function: str
    formal_args: list[Argument] = Field(min_length=1)
    tests: list[TestCase]


class GeneratedTests(BaseModel):
    functions: list[FunctionTests]