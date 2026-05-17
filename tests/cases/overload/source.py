import typing
import dyntypes

files = ["a.txt", "b.py", "c.mp4"]

def read(filename: str) -> bytes | None:
    try:
        with open(filename, "rb") as f:
            return f.read()
    except Exception:
        return None



def run(codegen: dyntypes.Codegen):
    for file in files:
        codegen.overload_func(read, filename=file, return_type=bytes)

    codegen.overload_func(read, filename=str, return_type=None)
