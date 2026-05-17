from .resolve import LiteralType, is_literal_value
from .errors import TypegenFailureWarning
import warnings
import typing as t


def Literal(values: list | LiteralType) -> type:
    if not isinstance(values, list):
        values = [values]

    try:
        for value in values:
            if not is_literal_value(value):
                raise TypeError(f"Expected literal type, not {value}")

        return t.Literal[*values]  # type: ignore
    except Exception as e:
        warnings.warn(
            message="Failed to generate union literal, defaulting to never",
            category=TypegenFailureWarning,
        )
        print(e)
        return t.Never  # type: ignore


def Union(values: list) -> type:
    try:
        return t.Union[*values]  # type: ignore
    except Exception as e:
        warnings.warn(
            message="Failed to generate union type, defaulting to never",
            category=TypegenFailureWarning,
            source=e,
        )
        return t.Never  # type: ignore
