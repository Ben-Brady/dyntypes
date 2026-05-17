import typing
import dyntypes

type Filename = typing.Literal["a", "b", "c"]

def read(filename: Filename):
    ...


def run(codegen: dyntypes.Codegen):
    ...
