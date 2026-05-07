import typing
from dyntypes import Codegen
from pathlib import Path
import io
ASSET_FOLDER = Path('./files')
type Reader = io.BufferedReader

@typing.overload
def open_asset(filename: typing.Literal['a.txt']) -> Reader:
    ...

@typing.overload
def open_asset(filename: typing.Literal['b.txt']) -> Reader:
    ...

@typing.overload
def open_asset(filename: typing.Literal['c.txt']) -> Reader:
    ...

@typing.overload
def open_asset(filename: str) -> typing.Literal[None]:
    ...

def open_asset(filename: str) -> Reader | None:
    ...

def generate_types():
    ...