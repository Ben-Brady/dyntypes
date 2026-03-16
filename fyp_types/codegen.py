from . import types, astutils

from resulting import Result, Ok, Err, Option, Some, none, optional, catch
import typing as t
import inspect
from modulefinder import ModuleFinder
from dataclasses import dataclass
from pathlib import Path
import ast


def find_func_node(module: ast.Module, line: int) -> ast.FunctionDef | None:
    for node in ast.walk(module):
        if not isinstance(node, ast.FunctionDef):
            continue

        print(line, node.lineno)
        if line == node.lineno:
            return node

        for decor in node.decorator_list:
            if decor.lineno == line:
                return node

        return None

    return None


def get_module_path_from_name(moudle_name: str) -> Path | None:
    finder = ModuleFinder()
    reader, filepath, _ = finder.find_module(moudle_name, None)
    if reader is None or filepath is None:
        return None

    reader.close()
    return Path(filepath)


def strip_implementation(module: ast.Module):
    for node in ast.walk(module):
        if isinstance(node, ast.FunctionDef):
            node.body = [astutils.parse_stmt("...")]


def update_param(func: ast.FunctionDef, param: str, value: ast.expr):
    for arg in func.args.args:
        if arg.arg == param:
            arg.annotation = value


@dataclass
class FunctionOverload:
    parameters: dict[str, ast.expr]
    return_type: ast.expr


class Parameter:
    def __init__(self) -> None:
        pass


class Function:
    func_obj: t.Callable | None = None
    overloads: list[FunctionOverload]

    def __init__(self) -> None:
        self.overloads = []

    def bind[T: t.Callable](self, func: T) -> T:
        self.func_obj = func
        return func

    def add(self, return_type: type | None = None, **kwargs):
        self.overloads.append(
            FunctionOverload(
                return_type=astutils.to_expr(return_type),
                parameters={
                    key: astutils.to_expr(value) for key, value in kwargs.items()
                },
            )
        )


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
                paths[path].append(overload)

        for filepath, modifications in paths.items():
            path = Path(filepath)
            module = ast.parse(path.read_text())
            for mod in modifications:
                _, line = inspect.getsourcelines(mod.func)
                node = find_func_node(module, line)
                if node is None:
                    print(f"Could not find func {mod.func}")
                    continue

                update_param(node, mod.parameters, mod.return_type)

            strip_implementation(module)
            stub_path = path.with_suffix(".pyi")
            output = ast.unparse(module)
            stub_path.write_text(output)

    def func(self) -> Function:
        func = Function()
        self._functions.append(func)
        return func
