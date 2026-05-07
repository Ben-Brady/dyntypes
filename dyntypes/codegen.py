from . import astutils
from .overloads import apply_overloads, OverloadDefinition
from .alias import apply_type_aliases, TypeAliasDefinition

from dataclasses import dataclass, field
import typing as t
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

    def overload_func(self, func: t.Callable, *, return_type: t.Any | None = None, **kwargs: t.Any):
        """
        Attaches a function overload to the specified function

        ## Example

        ```
        def find_user_id(name: str) -> int | None:
            ...

        codegen = Codegen()
        codegen.overload_func(find_user_id, name="admin", return_type=int)
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

        files: dict[str, FileModifications] = {}
        for overload in self._overloads:
            path = inspect.getfile(overload.func)
            files.setdefault(path, FileModifications())
            files[path].overloads.append(overload)

        for alias in self._aliases:
            path = inspect.getfile(alias.type_alias)
            files.setdefault(path, FileModifications())
            files[path].overloads.append(overload)

        for filepath, modifications in files.items():
            path = Path(filepath)
            stub_path = path.with_suffix(".pyi")
            module = ast.parse(path.read_text())

            astutils.strip_function_implementations(module)
            apply_overloads(module, modifications.overloads)
            apply_type_aliases(module, modifications.aliases)

            stub_src = ast.unparse(module)
            stub_path.write_text(stub_src)
