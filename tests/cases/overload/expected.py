import typing
import dyntypes

files = ["a.txt", "b.py", "c.mp4"]


@typing.overload
def read(filename: typing.Literal["a.txt"]) -> bytes:
    ...


@typing.overload
def read(filename: typing.Literal["b.py"]) -> bytes:
    ...


@typing.overload
def read(filename: typing.Literal["c.mp4"]) -> bytes:
    ...


@typing.overload
def read(filename: str) -> None:
    ...


def read(filename: str) -> bytes | None:
    ...


def run(codegen: dyntypes.Codegen):
    ...
