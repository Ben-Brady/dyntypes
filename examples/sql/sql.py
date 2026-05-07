from dyntypes import Codegen
import typing as t

statements: list[str] = []


def prepare_statement(statement: str):
    statements.append(statement)


def query(statement: str, args: tuple) -> tuple: ...


def generate_types():
    codegen = Codegen()
    for statement in statements:
        parameter_count = statement.count("?")
        args = tuple[*[t.Any for _ in range(parameter_count)]]  # type: ignore
        codegen.overload_func(
            query,
            statement=statement,
            args=args,
        )

    codegen.overload_func(query, return_type=t.Never)
    codegen.save()
