from dyntypes import Codegen
from pathlib import Path
import io

ASSET_FOLDER = Path("./files")

type Reader = io.BufferedReader


def open_asset(filename: str) -> Reader | None:
    try:
        return open(ASSET_FOLDER / filename, "rb")
    except FileNotFoundError:
        return None


def generate_types():
    codegen = Codegen()

    for file in ASSET_FOLDER.iterdir():
        filename = file.name
        codegen.overload_func(
            open_asset, filename=filename, return_type=io.BufferedReader)

    codegen.overload_func(open_asset, filename=str, return_type=None)

    codegen.save()
