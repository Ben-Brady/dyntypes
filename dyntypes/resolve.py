from . import astutils
import builtins
import ast
import typing as t
import types

TYPING_IMPORT = "t"


def value_to_ast(value: t.Any) -> ast.expr:
    # TODO: Swappout for generic approach
    if getattr(value, "__module__", None) == "typing":
        return astutils.attribute(astutils.name(TYPING_IMPORT), value.__name__)

    if isinstance(value, types.UnionType):
        args = t.get_args(value)
        union_values = [value_to_ast(v) for v in args]
        return astutils.union(union_values)

    if type(value) is types.GenericAlias:
        if value.__qualname__ == "tuple":
            args = t.get_args(value)
            obj = astutils.tuple_generic([value_to_ast(v) for v in args])
            return obj

    if is_literal_type(value):
        args = t.cast(tuple[str], t.get_args(value))
        return astutils.literal(args)

    if isinstance(value, type) and is_builtin(value):
        return astutils.name(value.__name__)

    if is_literal_value(value):
        return astutils.literal([value])

    raise ValueError(f"{value} ({type(value)}) is not supported")


# https://typing.python.org/en/latest/spec/literal.html#legal-parameters-for-literal-at-type-check-time

type LiteralType = int | str | bytes | bool | None


def is_literal_value(value: t.Any) -> t.TypeGuard[LiteralType]:
    # TODO: Support Enum variants
    return isinstance(value, (int, str, bytes, bool)) or value is None


def is_literal_type(value: t.Any) -> bool:
    return getattr(value, "__name__", None) == "Literal"


def is_builtin(value: type):
    name = value.__name__

    if value.__module__ == "builtins":
        return True

    if name in dir(builtins):
        return True

    try:
        eval(name, {}, {})
    except NameError:
        return False
    else:
        return True
