from . import astutils
import types
from dataclasses import dataclass
import ast

type FunctionID = str


@dataclass
class FunctionOverload:
    function: ast.FunctionDef
    parameter_types: dict[str, ast.expr] | types.EllipsisType = ...
    return_type: ast.expr | types.EllipsisType = ...


def apply_function_overlaoy(overload: FunctionOverload) -> ast.FunctionDef:
    func = astutils.clone_node(overload.function)

    if overload.parameter_types is not ...:
        for t in func.type_params:
            t.
        func.returns = overload.return_type

    if overload.return_type is not ...:
        func.returns = overload.return_type
