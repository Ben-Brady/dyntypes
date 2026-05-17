from dyntypes import Union, Literal, TypegenFailureWarning, Codegen
from cases import alias, overload

import typing as t
import types
import ast
from utils import test
import warnings


@test("Codegen Examples: alias")
def _():
    perform_generation_test(
        generate=alias.source.run,
        expected_module=alias.expected
    )


@test("Codegen Examples: overload example")
def _():
    perform_generation_test(
        generate=overload.source.run,
        expected_module=overload.expected
    )


def perform_generation_test(*, generate: t.Callable[[Codegen], None],  expected_module: types.ModuleType):
    codegen = Codegen()
    generate(codegen)

    stubs = codegen._generate_stubs()
    stub_output = list(stubs.values())
    assert len(stub_output) == 1
    stub_ast = stub_output[0]

    expected_ast = load_module_ast(expected_module)
    assert_module_equals(stub_ast, expected_ast)


def assert_module_equals(a: ast.Module, b: ast.Module):
    ast.fix_missing_locations(a)
    ast.fix_missing_locations(b)
    a_src = ast.unparse(a)
    b_src = ast.unparse(b)

    if a_src == b_src:
        return

    import difflib
    print("\n".join(difflib.unified_diff(a_src.split("\n"), b_src.split("\n"))))
    assert False, "Modules not equal"


def load_module_ast(module: types.ModuleType) -> ast.Module:
    file = module.__file__
    if not file:
        raise FileNotFoundError(
            f"Could not find the file for the module: {module}")

    with open(file) as f:
        src = f.read()

    return ast.parse(src)
