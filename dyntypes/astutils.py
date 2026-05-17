import ast
import typing as t
from pathlib import Path


TNode = t.TypeVar("TNode", bound=ast.stmt)


def read_ast(filepath: str) -> ast.Module:
    path = Path(filepath)
    src = path.read_text()
    return ast.parse(src)


def write_ast(filepath: str | Path, module: ast.Module):
    path = Path(filepath)
    src = ast.unparse(module)
    path.write_text(src)


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


def literal(values: t.Sequence[int | str | bytes | bool | None], *, typing_import: str) -> ast.expr:
    if len(values) == 1:
        slice = constant(values[0])
    else:
        slice = tuple([constant(v) for v in values])

    return subscript(
        value=attribute(name(typing_import), "Literal"),
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


def import_(name: str, asname: str | None = None) -> ast.Import:
    return ast.Import(names=[ast.alias(name=name, asname=asname)])


def typing_overload(typing_import: str) -> ast.expr:
    return attribute(name(typing_import), "overload")


def strip_function_implementations(module: ast.Module):
    for node in ast.walk(module):
        if isinstance(node, ast.FunctionDef):
            node.body = [parse_stmt("...")]
