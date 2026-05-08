from .errors import TypegenFailureWarning
from .typing_import import generate_typing_import
from .resolve import value_to_ast
import warnings
import typing as t
from dataclasses import dataclass
import ast


@dataclass
class TypeAliasDefinition:
    type_alias: t.TypeAliasType
    value: type


def apply_type_aliases(module: ast.Module, aliases: list[TypeAliasDefinition]):
    typing_import = generate_typing_import(module)

    for alias in aliases:
        alias_def = find_type_alias_by_name(
            module, alias.type_alias.__name__
        )
        if alias_def is None:
            continue
        alias_def.value = value_to_ast(
            alias.value,
            typing_import=typing_import
        )


def find_type_alias_by_name(module: ast.Module, name: str) -> ast.TypeAlias | None:
    aliases: list[ast.TypeAlias] = []
    for node in ast.walk(module):
        if isinstance(node, ast.TypeAlias) and node.name.id == name:
                aliases.append(node)

    if len(aliases) == 0:
        msg = f"Could not find type alias '{name}', unable to create definition"
        warnings.warn(msg, category=TypegenFailureWarning)
    elif len(aliases) > 1:
        msg = f"More than one type alias named '{name}', unable to create definition"
        warnings.warn(msg, category=TypegenFailureWarning)
    else:
        return aliases[0]
