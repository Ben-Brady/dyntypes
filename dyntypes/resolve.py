from . import astutils
import builtins
import ast
import typing as t
import types


def value_to_ast(value: t.Any, *, typing_import: str) -> ast.expr:
    if getattr(value, "__module__", None) == "typing":
        return astutils.attribute(astutils.name(typing_import), value.__name__)

    if isinstance(value, types.UnionType):
        args = t.get_args(value)
        union_values = [value_to_ast(
            v, typing_import=typing_import) for v in args]
        return astutils.union(union_values)

    if type(value) is types.GenericAlias:
        if value.__qualname__ == "tuple":
            args = t.get_args(value)
            obj = astutils.tuple_generic(
                [value_to_ast(v, typing_import=typing_import) for v in args])
            return obj

    if isinstance(value, t.TypeAliasType):
        return astutils.name(value.__name__)

    if is_literal_type(value):
        args = t.cast(tuple[str], t.get_args(value))
        return astutils.literal(args, typing_import=typing_import)

    if isinstance(value, type) and is_builtin(value):
        return astutils.name(value.__name__)

    if is_literal_value(value):
        return astutils.literal([value], typing_import=typing_import)

    raise ValueError(
        f"generating types with type {type(value)} is not supported")


# https://typing.python.org/en/latest/spec/literal.html#legal-parameters-for-literal-at-type-check-time

type LiteralType = int | str | bytes | bool | None


def is_literal_value(value: t.Any) -> t.TypeGuard[LiteralType]:
    return isinstance(value, (int, str, bytes, bool)) or value is None


def is_literal_type(value: t.Any) -> bool:
    return getattr(value, "__name__", None) == "Literal"


def is_builtin(value: type):
    try:
        if value.__module__ == "builtins":
            return True

        # Note this should be redundant
        # but is useful for things re-exported in builtins
        if value.__name__ in dir(builtins):
            return True
    except AttributeError:
        return False

    # Fallback for special cases
    try:
        eval(name, {}, {})
    except NameError:
        return False
    else:
        return True
