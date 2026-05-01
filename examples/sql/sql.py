from dyntypes import Codegen
import typing as t
from pathlib import Path

codegen = Codegen()
query_func = codegen.func()
statements: list[str] = []


def prepare_statement(statement: str):
    statements.append(statement)


@query_func.bind
def query(statement: str, args: tuple) -> tuple: ...


def generate_types():
    for statement in statements:
        parameter_count = statement.count("?")
        return_type = tuple[tuple([t.Any for _ in range(parameter_count)])]
        query_func.overload(
            statement=statement,
            args=return_type,
            return_type=tuple,
        )

    query_func.overload(filename=str, return_type=t.Never)

    codegen.save()
