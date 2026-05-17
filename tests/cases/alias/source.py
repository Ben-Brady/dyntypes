import typing
import dyntypes

type Filename = str

def read(filename: Filename):
    with open(filename) as f:
        return f.read()


def run(codegen: dyntypes.Codegen):
    codegen.set_type_alias(Filename, dyntypes.Literal(["a", "b", "c"]))
