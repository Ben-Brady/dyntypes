from . import types, astutils
from .resolve import value_to_ast

from resulting import Result, Ok, Err, Option, Some, none, optional, catch
import typing as t
import inspect
from modulefinder import ModuleFinder
from dataclasses import dataclass, field
from pathlib import Path
import ast


@dataclass
class FunctionOverloadOptions:
    parameters: dict[str, ast.expr]
    return_type: ast.expr


@dataclass
class Function:
    func_obj: t.Callable | None = None
    overloads: list[FunctionOverloadOptions] = field(default_factory=list)

    def bind[T: t.Callable](self, func: T) -> T:
        self.func_obj = func
        return func

    def overload(self, return_type: t.Any | None = None, **kwargs: t.Any):
        self.overloads.append(
            FunctionOverloadOptions(
                return_type=value_to_ast(return_type),
                parameters={key: value_to_ast(value) for key, value in kwargs.items()},
            )
        )


@dataclass
class FunctionOverload:
    func: Function
    parameters: dict[str, ast.expr]
    return_type: ast.expr


class Codegen:
    _functions: list[Function]

    def __init__(self) -> None:
        self._functions = []

    def generate(self):
        paths: dict[str, list[FunctionOverload]] = {}
        for func in self._functions:
            assert func.func_obj
            path = inspect.getfile(func.func_obj)
            paths.setdefault(path, [])
            for overload in func.overloads:
                paths[path].append(
                    FunctionOverload(
                        func=func,
                        parameters=overload.parameters,
                        return_type=overload.return_type,
                    )
                )

        for filepath, overloads in paths.items():
            path = Path(filepath)
            module = ast.parse(path.read_text())

            # TODO: Detect existing imports
            # TODO: Ensure it's an unsued name
            module.body.insert(0, astutils.typing_import())
            # Reverse overloads to match declaration order
            overloads = reversed(overloads)
            for overload in overloads:
                if overload.func.func_obj is None:
                    continue

                func_def = _find_func_node_by_name(
                    module, overload.func.func_obj.__name__
                )
                if func_def is None:
                    continue

                overload_def = _generate_overload_def(func_def, overload)
                index = module.body.index(func_def)
                module.body.insert(index, overload_def)

            _strip_implementation(module)
            stub_path = path.with_suffix(".pyi")
            stub_path.write_text(ast.unparse(module))

    def func(self) -> Function:
        func = Function()
        self._functions.append(func)
        return func


def _generate_overload_def(
    func_def: ast.FunctionDef, overload: FunctionOverload
) -> ast.FunctionDef:
    overload_def = astutils.clone_node(func_def)
    overload_def.decorator_list = [astutils.typing_overload()]

    for param, param_type in overload.parameters.items():
        _update_param(overload_def, param, param_type)
    overload_def.returns = overload.return_type
    return overload_def


def _find_func_node_by_name(module: ast.Module, name: str) -> ast.FunctionDef | None:
    for node in ast.walk(module):
        if isinstance(node, ast.FunctionDef) and node.name == name:
            return node

    return None


def _strip_implementation(module: ast.Module):
    for node in ast.walk(module):
        if isinstance(node, ast.FunctionDef):
            node.body = [astutils.parse_stmt("...")]


def _update_param(func: ast.FunctionDef, param: str, value: ast.expr):
    for arg in func.args.args:
        if arg.arg == param:
            arg.annotation = value
