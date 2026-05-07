import typing as t
from dyntypes import Codegen
import typing as t
from pathlib import Path
codegen = Codegen()
query_func = codegen.overload_func()
statements: list[str] = []


def prepare_statement(statement: str):
    ...


@t.overload
def query(statement: t.Literal['INSERT INTO users (id, name) VALUES(?, ?)'], args: tuple[t.Any, t.Any]) -> tuple:
    ...


@t.overload
def query(statement: t.Literal['SELECT * FROM users WHERE id = ?'], args: tuple[t.Any,]) -> tuple:
    ...


@t.overload
def query(statement: str, args: tuple) -> t.Never:
    ...


@query_func.bind
def query(statement: str, args: tuple) -> tuple:
    ...


def generate_types():
    ...
