from . import astutils
from .errors import TypegenFailureWarning
from .typing_import import generate_typing_import
import warnings
import typing as t
from dataclasses import dataclass
import ast


@dataclass
class OverloadDefinition:
    func: t.Callable
    parameters: dict[str, ast.expr]
    return_type: ast.expr


def apply_overloads(module: ast.Module, overloads: list[OverloadDefinition]):
    typing_import = generate_typing_import(module)

    func_overloads: dict[str, list[OverloadDefinition]] = {}
    for overload in overloads:
        func_name = overload.func.__name__

        func_overloads.setdefault(func_name, [])
        func_overloads[func_name].append(overload)

    for func_name, overloads in func_overloads.items():
        func_def = find_func_def_by_name(module, func_name)
        if func_def is None:
            continue

        # We need to reverse order for overloads since
        # when they'll be written in inverse order
        for overload in reversed(overloads):
            overload_def = generate_overload_definition(
                func_def=func_def,
                overload=overload,
                typing_import=typing_import,
            )
            index = module.body.index(func_def)
            module.body.insert(index, overload_def)


def generate_overload_definition(
    func_def: ast.FunctionDef,
    overload: OverloadDefinition,
    typing_import: str,
) -> ast.FunctionDef:

    overload_def = astutils.clone_node(func_def)
    overload_def.decorator_list = [astutils.typing_overload(typing_import)]

    for param, param_type in overload.parameters.items():
        update_def_parameter(overload_def, param, param_type)
    overload_def.returns = overload.return_type
    return overload_def


def update_def_parameter(func: ast.FunctionDef, param: str, value: ast.expr):
    for arg in func.args.args:
        if arg.arg == param:
            arg.annotation = value


def find_func_def_by_name(module: ast.Module, name: str) -> ast.FunctionDef | None:
    func_defs: list[ast.FunctionDef] = []
    for node in ast.walk(module):
        if isinstance(node, ast.FunctionDef) and node.name == name:
            func_defs.append(node)

    if len(func_defs) == 0:
        msg = f"Could not find function '{name}', unable to create overload"
        warnings.warn(msg, category=TypegenFailureWarning)
    elif len(func_defs) > 1:
        msg = f"More than one function named '{name}', unable to create overload"
        warnings.warn(msg, category=TypegenFailureWarning)
    else:
        return func_defs[0]
