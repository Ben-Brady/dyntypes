from __future__ import annotations
from .astutils import parse_expr
import ast
import typing as t
from dataclasses import dataclass


@dataclass(slots=True)
class Literal:
    value: t.Any

    @classmethod
    def __class_getitem__(cls, parameter) -> Type:
        return cls(parameter)



class Union:
    values: list[Type]

    def __init__(self, *values: Type):
        self.values = list(values)

    @classmethod
    def __class_getitem__(cls, parameters) -> Type:
        if not isinstance(parameters, tuple):
            parameters = (parameters,)

        return cls(*parameters)

    def to_ast(self):
        if len(self.values) == 0:
            return parse_expr("t.Never")

        if len(self.values) == 1:
            return self.values[0].to_ast()

        def create_union(nodes: list[t.Any]):
            if len(nodes) == 1:
                return nodes[0].to_ast()
            else:
                a = nodes[0].to_ast()
                b = create_union(nodes[1:])
                return ast.BinOp(op=ast.BitOr(), left=a, right=b)

        return create_union(self.values)


Type: t.TypeAlias = Literal | Union
