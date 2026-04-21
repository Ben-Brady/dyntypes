import typing as t
from dyntypes import Codegen
import typing as t
from pathlib import Path
import io
codegen = Codegen()
asset_func = codegen.func()
ASSET_FOLDER = Path('./files')

@t.overload
def open_asset(filename: t.Literal['c.txt']) -> int:
    ...

@t.overload
def open_asset(filename: t.Literal['a.txt']) -> int:
    ...

@t.overload
def open_asset(filename: t.Literal['b.txt']) -> int:
    ...

@t.overload
def open_asset(filename: str) -> t.Literal[None]:
    ...

@asset_func.bind
def open_asset(filename: str) -> io.BufferedReader | None:
    ...

def generate_types():
    ...