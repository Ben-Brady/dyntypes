# Dyntypes

Dyntypes is a library for generatinging


```py
from dyntypes import Codegen
import typing as t

codegen = Codegen()

query_func = codegen.func()
@query_func.bind
def query(statement: str, args: tuple) -> tuple: ...

def generate_types():
    query_func.overload(
        filename="SELECT * FROM posts WHERE ID = ",
        args=tuple[int],
        return_type=list[str | int],
    )
    query_func.overload(filename=str, return_type=t.Never)
    codegen.save()

if __name__ == "__main__":
    generate_types()
```

## What are Type Stubs?

Type stubs are a way of adding type hints to files in python, intended for C extensions.

However, there is nothing stopping code from using this to annotate dynamic types on files.

## Quickstart Guide

Create a codegen object, this stores all the type information you'll bind to functions

```py
from dyntypes import Codegen

codegen = Codegen()
```

Create a function type object

```py
example_func = codegen.func()
@example_func.bind
def example(bar: str) -> int | None: ...
```

Next we apply overloads to this function, we use the function binding to do this.

I recommend creating a seperate function for type generation so that it can be run conditionally.

```py
def generate_types():
    query_func.overload(
        filename="SELECT * FROM posts WHERE ID = ",
        args=tuple[int],
        return_type=list[str | int],
    )
    query_func.overload(filename=str, return_type=t.Never)
    codegen.generate() # Writes out the type stub files
```

## Examples

For example implementations, see the examples folder at LINK HEERE
