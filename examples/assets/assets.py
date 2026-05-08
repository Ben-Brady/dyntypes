from dyntypes import Codegen
from pathlib import Path
import io
import typing as t

ASSET_FOLDER = Path("./files")

type AssetID = str


def open_asset(filename: str) -> io.BufferedReader:
    return open(ASSET_FOLDER / filename, "rb")


def generate_types():
    codegen = Codegen()

    files = []
    for file in ASSET_FOLDER.iterdir():
        files.append(file.name)

    foo = t.Literal[*files]
    print(foo)
    codegen.set_type_alias(AssetID, foo)  # type: ignore
    codegen.save()
