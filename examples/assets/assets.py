from dyntypes import Codegen
import typing as t
from pathlib import Path
import io

codegen = Codegen()
open_asset_func = codegen.func()
ASSET_FOLDER = Path("./files")


@open_asset_func.bind
def open_asset(filename: str) -> io.BufferedReader | None:
    try:
        return open(ASSET_FOLDER / filename, "rb")
    except FileNotFoundError:
        return None


def generate_types():
    files = (file.name for file in ASSET_FOLDER.iterdir())
    for filename in files:
        open_asset_func.overload(filename=filename, return_type=int)

    open_asset_func.overload(filename=str, return_type=None)

    codegen.save()
