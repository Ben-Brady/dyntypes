import ast
import typing as t

TYPING_IMPORT = "t"


TNode = t.TypeVar("TNode", bound=ast.stmt)


def clone_node(node: TNode) -> TNode:
    code = ast.unparse(node)
    cloned_node = parse_stmt(code)
    assert type(cloned_node) == type(node)
    return cloned_node


def parse_stmt(code: str) -> ast.stmt:
    module = ast.parse(code)
    node = module.body[0]
    return node


def to_expr(value: t.Any) -> ast.expr:
    expr = parse_expr(str(value))
    return expr


def parse_expr(code: str) -> ast.expr:
    node = parse_stmt(code)
    if not isinstance(node, ast.Expr):
        raise TypeError(f"{code} was not an Expr")

    return node.value


def subscript(value: ast.expr, slice: ast.expr) -> ast.expr:
    return ast.Subscript(value=value, slice=slice, ctx=ast.Load())


def name(id: str) -> ast.expr:
    return ast.Name(id=id, ctx=ast.Load())


def attribute(value: ast.expr, attr: str) -> ast.expr:
    return ast.Attribute(value=value, attr=attr, ctx=ast.Load())


def constant(value: None | str | bytes | int | float | complex) -> ast.expr:
    return ast.Constant(value=value)


def tuple(elements: list[ast.expr]) -> ast.expr:
    return ast.Tuple(elts=elements, ctx=ast.Load())


def literal(values: t.Sequence[int | str | bytes | bool | None]) -> ast.expr:
    if len(values) == 1:
        slice = constant(values[0])
    else:
        slice = tuple([constant(v) for v in values])

    return subscript(
        value=attribute(name(TYPING_IMPORT), "Literal"),
        slice=slice,
    )


def union(values: list[ast.expr]) -> ast.expr:
    if len(values) == 1:
        return values[0]
    else:
        first, *other = values
        return ast.BinOp(
            op=ast.BitOr(),
            left=first,
            right=union(other),
        )


def tuple_generic(values: list[ast.expr]) -> ast.expr:
    return subscript(
        value=name("tuple"),
        slice=ast.Tuple(elts=values, ctx=ast.Load()),
    )


def typing_import() -> ast.Import:
    return ast.Import(names=[ast.alias(name="typing", asname=TYPING_IMPORT)])


def typing_overload() -> ast.expr:
    return attribute(name(TYPING_IMPORT), "overload")
