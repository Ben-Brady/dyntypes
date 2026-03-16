import ast
import typing as t


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
