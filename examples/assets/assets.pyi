from dyntypes import Codegen
from pathlib import Path
import io
import typing as t
ASSET_FOLDER = Path('./files')
type AssetID = t.Literal['a.txt', 'b.txt', 'c.txt']

def open_asset(filename: str) -> io.BufferedReader:
    ...

def generate_types():
    ...