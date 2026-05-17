from . import astutils
from .overloads import apply_overloads, OverloadDefinition, InitialType
from .alias import apply_type_aliases, TypeAliasDefinition
from .errors import TypegenFailureWarning
from .resolve import get_obj_file

import warnings

from dataclasses import dataclass, field
import typing as t
import types
import inspect
from pathlib import Path
import ast


@dataclass
class FileModifications:
    overloads: list[OverloadDefinition] = field(default_factory=list)
    aliases: list[TypeAliasDefinition] = field(default_factory=list)


class Codegen:
    _overloads: list[OverloadDefinition]
    _aliases: list[TypeAliasDefinition]

    def __init__(self) -> None:
        self._overloads = []
        self._aliases = []

    def overload_func(self, func: t.Callable, *, return_type: t.Any = InitialType(), **kwargs: t.Any):
        """
        Attaches a function overload to the specified function.

        Leaving a parameter or return type unspecified will use the original value.

        ## Example

        ```
        def find_user_id(name: str) -> int | None:
            ...

        codegen = Codegen()
        codegen.overload_func(find_user_id, name="admin", return_type=int)
        codegen.overload_func(find_user_id, name=str, return_type=None)
        ```
        """
        overload = OverloadDefinition(
            func=func,
            parameters=kwargs,
            return_type=return_type,
        )
        self._overloads.append(overload)

    def set_type_alias(self, type_alias: t.TypeAliasType, type: type):
        """
        Updates a type alias with a specified type

        ## Example

        ```
        type Foo = str

        codegen = Codegen()
        ids = ["a", "b", "c"]
        codegen.set_type_alias(Foo, typing.Literal[*ids])
        ```
        """
        func = TypeAliasDefinition(
            type_alias=type_alias,
            value=type,
        )
        self._aliases.append(func)
        return func

    def save(self):
        """
        Generate and creates the type stub files for any types declared
        using this object.

        ## Example

        ```
        codegen = Codegen()
        ...
        codegen.save()
        ```
        """
        stubs = self._generate_stubs()

        for stub_path, module in stubs.items():
            astutils.write_ast(stub_path, module)

    # Split off into a seperate file for testing
    def _generate_stubs(self) -> dict[Path, ast.Module]:
        files: dict[str, FileModifications] = {}
        for overload in self._overloads:
            path = get_obj_file(overload.func)
            if not path:
                warnings.warn(
                    f"Could not find source file for {overload.func}",
                    category=TypegenFailureWarning
                )
            else:
                files.setdefault(path, FileModifications())
                files[path].overloads.append(overload)

        for alias in self._aliases:
            path = get_obj_file(alias.type_alias)
            if not path:
                warnings.warn(
                    f"Could not find source file for {alias.type_alias}",
                    category=TypegenFailureWarning
                )
            else:
                files.setdefault(path, FileModifications())
                files[path].aliases.append(alias)

        outputs: dict[Path, ast.Module] = {}
        for filepath, modifications in files.items():
            module = astutils.read_ast(filepath)

            astutils.strip_function_implementations(module)
            apply_overloads(module, modifications.overloads)
            apply_type_aliases(module, modifications.aliases)

            stub_path = generate_stub_path(filepath)
            outputs[stub_path] = module

        return outputs


def generate_stub_path(filepath: str) -> Path:
    return Path(filepath).with_suffix(".pyi")
