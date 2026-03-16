import typing as t
from fyp_types import Codegen, Union, Literal

codegen = Codegen()


@codegen.bind_param(
    "param",
    t.Union[
        t.Literal["A"], t.Literal["B"], t.Literal["C"], t.Literal["D"], t.Literal["D"]
    ],
)
def foo(param1): ...

codegen.generate()
