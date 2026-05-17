from dyntypes.resolve import is_literal_value, value_to_ast_type, is_builtin_type
from dyntypes.astutils import literal
from utils import test
import ast


@test("value_to_ast_type: converts to expected types")
def _():
    typing_import = "typing"
    literal_object = ast.Attribute(
        value=ast.Name(id=typing_import),
        attr="Literal"
    )

    testcases = {
        "int": (int, ast.Name(id="int")),
        "None": (None, ast.Name(id="None")),
        "literal string": ("foo", ast.Subscript(
            value=literal_object,
            slice=ast.Constant(value="foo")
        )),
        "literal int": (1, ast.Subscript(
            value=literal_object,
            slice=ast.Constant(value=1)
        ))
    }
    for case, (value, expected) in testcases.items():
        ast_type = value_to_ast_type(value, typing_import=typing_import)
        assert ast_equal(ast_type, expected), f"{case} failed: {value}"


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
    class CustomType:
        pass

    assert not is_builtin_type(CustomType), f"did not fail on custom type"


def ast_equal(a: ast.AST, b: ast.AST):
    ast.fix_missing_locations(a)
    ast.fix_missing_locations(b)
    return ast.unparse(a) == ast.unparse(b)
