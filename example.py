import typing as t
from pathlib import Path
import types
from fyp_types import Codegen, Function, Union, Literal

codegen = Codegen()

foo_func = codegen.func()

foo_func.add(param1=str, return_type=None)
for file in Path(".").iterdir():
    foo_func.add(param1=t.Literal[str(file)], return_type=int)


@foo_func.bind
def foo(param1: str) -> int | None:
    param1


codegen.generate()
