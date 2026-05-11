from .resolve import LiteralType
import typing as t


def Literal(values: list | LiteralType) -> type:
    return t.Literal[*values]  # type: ignore

def Union(values: list) -> type:
    return t.Union[*values]  # type: ignore
