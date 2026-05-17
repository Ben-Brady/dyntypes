from . import astutils
import builtins
import ast
import typing as t
import types
import re


def value_to_ast(value: t.Any, *, typing_import: str) -> ast.expr:
    # int, str, bool
    if isinstance(value, type) and is_builtin_type(value):
        return astutils.name(value.__name__)

    # "a", 1
    if is_literal_value(value):
        return astutils.literal([value], typing_import=typing_import)

    # 1 | 2 | 3
    # TODO: add support for imported types, i.e. io.Reader
    if isinstance(value, types.UnionType):
        args = t.get_args(value)
        union_values = [value_to_ast(
            v, typing_import=typing_import) for v in args]
        return astutils.union(union_values)

    # tuple[int, str, foo]
    if type(value) is types.GenericAlias and value.__qualname__ == "tuple":
        args = t.get_args(value)
        obj = astutils.tuple_generic(
            [value_to_ast(v, typing_import=typing_import) for v in args])
        return obj

    # type Foo = int
    if isinstance(value, t.TypeAliasType):
        return astutils.name(value.__name__)

    # Literal["a", "b"]
    if is_literal_type(value):
        args = t.cast(tuple[str], t.get_args(value))
        return astutils.literal(args, typing_import=typing_import)

    # typing.*
    if getattr(value, "__module__", None) == "typing":
        return astutils.attribute(astutils.name(typing_import), value.__name__)

    raise ValueError(
        f"generating types with type {type(value)} is not supported")


# https://typing.python.org/en/latest/spec/literal.html#legal-parameters-for-literal-at-type-check-time

type LiteralType = int | str | bytes | bool | None


def is_literal_value(value: t.Any) -> t.TypeGuard[LiteralType]:
    WHITELIST = (int, str, bytes, bool)

    # We check the type directly to prevent invalid subclasses
    if type(value) in WHITELIST:
        return True

    if value is None:
        return True

    return False


def is_literal_type(value: t.Any) -> bool:
    return getattr(value, "__name__", None) == "Literal"


def is_builtin_type(obj_type: type):
    try:
        name = obj_type.__name__

        if obj_type.__module__ == "builtins":
            return True

        # Check things re-exported in builtins
        if name in dir(builtins):
            return True
    except AttributeError:
        return False

    # Prevent evaling malicious code
    if not is_ident(name):
        return False

    # Fallback for special cases
    try:
        eval(name, {}, {})
    except NameError:
        return False
    else:
        return True


IDENT_REGEX = re.compile(r"[0-9A-Za-z_]+",)


def is_ident(name: str) -> bool:
    return bool(IDENT_REGEX.match(name))


def get_obj_file(obj: t.Any) -> str | None:
    try:
        if isinstance(obj, types.FunctionType):
            return inspect.getfile(obj)

        module = inspect.getmodule(obj)
        if not module:
            return None
        else:
            return module.__file__

    except Exception:
        return None
