from dyntypes.resolve import is_literal_value, value_to_ast, is_builtin_type
from utils import test


@test("value_to_ast: accepts valid literals")
def _():
    testcases = {
        "int": 123,
        "str": "asdasd",
        "True": False,
        "False": True,
        "None": None
    }
    for case, value in testcases.items():
        assert is_literal_value(value), f"{case} failed: {value}"


@test("is_literal_value: accepts valid literals")
def _():
    testcases = {
        "int": 123,
        "str": "asdasd",
        "True": False,
        "False": True,
        "None": None
    }
    for case, value in testcases.items():
        assert is_literal_value(value), f"{case} failed: {value}"


@test("is_literal_value: doesn't accept invalid literals")
def _():
    testcases = {
        "Complex Number": 1j,
        "Dictionary": {1: 1, 2: 2, 3: 3},
        "Set": {1, 2, 3},
        "List": [1, 2, 3],
        "Ellpisis": ...
    }

    for case, value in testcases.items():
        assert not is_literal_value(value), f"{case} failed: {value}"


@test("is_builtin_type: accepts normal builtins")
def _():
    testcases = {
        "int": int,
        "str": str,
        "complex number": complex,
        "Exception": FileNotFoundError,
    }

    for case, value in testcases.items():
        assert is_builtin_type(value), f"{case} failed: {value}"

@test("is_builtin_type: fails on custom types")
def _():
    class CustomType: pass

    assert not is_builtin_type(CustomType), f"did not fail on custom type"
