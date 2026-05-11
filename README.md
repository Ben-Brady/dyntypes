# Dyntypes

Dyntypes is a library that lets you create types based on runtime values, allowing you to create more API patterns that were previously impossible.

## How it Works

Python lets you create `.pyi` type stub files. These are like regular python files, except they're only used by type checkers to see what types a file has. They override the original type definitions whilst not affecting the runtime. They're intended for use in C extensions where features such as docstrings are inaccessible, however they can be used to replace the types of an existing Python file.

## Usage Example

```py
import typing
from pathlib import Path
from dyntypes import Codegen

type AssetFilename = str

ASSET_FOLDER = Path("./assets")
def load_asset(name: AssetFilename) -> str:
    with open(f"{ASSET_FOLDER}/filename") as f:
        return f.read()

def generate_types():
    codegen = Codegen()
    asset_names = [file.name for file in ASSET_FOLDER.iterdir()]
    codegen.set_type_alias(AssetFilename, typing.Literal[*asset_names]) # redefine the alias with a literal of all the file names
    codegen.save() # This writes the type stub files to disk
```

For examples see the [examples folder](https://github.com/Ben-Brady/dyntypes/tree/main/examples) on GitHub.

## Documentation

### `Codegen()`

The main core of the library is the `Codegen` object. This holds the references to all the types you've defined and lets you save them with `.save()`.

### Aliases

Dyntypes supports redefining type aliases in stubs.

This lets create a loosely types alias, and then narrow it in the type stub.c

When redefining type alises you want the base alias to

#### Alias Example

```py
import typing
type AssetFilename = str

ASSET_FOLDER = Path("./assets")
def load_asset(name: AssetFilename) -> str:
    with open(f"{ASSET_FOLDER}/filename") as f:
        return f.read()

codegen = Codegen()

asset_names = [file.name for file in ASSET_FOLDER.iterdir()]
codegen.set_type_alias(AssetName, typing.Literal[*asset_names])
```

In this example, we're create a type alias that will store all the valid asset IDs held in a folder.

We define it as the loosest possible type, a string. Then we redefine it in the type stubs as a literal of all the files in that folder.

This means that when using this interface, we'll be able to get autocomplete on what is and isn't a valid filename

### Function Overloads

Dyntypes creating overloads for functions for specific use cases.


The order of overloads is also important, they will be checked first to last.

```py
codegen.overload_func(get_user, id="admin", return_type=User)
codegen.overload_func(get_user, id=str, return_type=None)
```

In this example: we're saying that if the ID is admin it's valid, but any other string should return None.

If we defined this the other way round, the string would be checked first and it would indicate that every string should return None.

#### Overload Example

```py
import typing

type AssetFilename = str

ASSET_FOLDER = Path("./assets")
def load_asset(name: AssetFilename) -> str:
    with open(f"{ASSET_FOLDER}/filename") as f:
        return f.read()

codegen = Codegen()

asset_names = [file.name for file in ASSET_FOLDER.iterdir()]
codegen.set_type_alias(AssetName, typing.Literal[*asset_names])
```


In this example, we're create a type alias that will store all the valid asset IDs held in a folder.

We define it as the loosest possible type, a string. Then we redefine it in the type stubs as a literal of all the files in that folder.

This means that when using this interface, we'll be able to get autocomplete on what is and isn't a valid filename/

### Notes

#### Literal Shorthand

As a shorthand, any value type such as string or int will automatically be converted into a Literal, so the following two lines are equivelent.

```py
codegen.overload_func(get_version, return_type=typing.Literal["1.0.0"])
codegen.overload_func(get_version, return_type="1.0.0")
```

This is performed for: `int`, `str`, `bytes`, `bool` and `None`.

#### `Literal` and `Union`

In order to dynamically support using `Literal` and `Union` types, dyntype has some helpers to do that. This is because IDEs through a warning if you try and use them directly. Although this can be removed with a `# type: ignore`, we do that for you to prevent errors in your own code.

```py
union_values = []
union_values.append(str)
union_values.append(int)
dyntypes.Union(union_values)
# equivelent to t.Union[*union_values]

first_100_numbers =  list(range(100))
dyntypes.Literal(first_100_numbers)
# equivelent to t.Literal[*first_100_numbers]
```

### Known Issues

#### Root Level

Dyntypes only supports generating types at the root level of the module, so any function or type alias defined inside a a class will be removed.

```py
def foo():
    type Bar = int # ❌: not in module body
    def bar(): # ❌: not in module body
        ...

class Foo:
    def foo(): # ❌: not in module body
        ...

if True:
    def foo(): # ❌: not in module body
        ...

type Bar = int # ️✅: will work correctly
def bar(): # ️✅: will work correctly
    ...
```

While support for type hinting objects inside classes may be added in a future version, conditional or nested functions are not planned.

#### Imported Types

Dyntypes currently doesn't support imported types directly due to limitations with how we convert values into their AST representation.

While support for this is planned, it can currently be worked around by defining a type alias:

```py

type MyAlias = t.Any

codegen.set_type_alias(MyAlias, io.BufferedReader)  # ❌: will not work due to import

type BufferedReader = io.BufferedReader
codegen.set_type_alias(MyAlias, BufferedReader)  # ️✅: current workaround
```

#### Function Overloads with the argument `return_type`

Due to the way overload_func is defined, you can't overload an argument named return_type.

This is a deliberate limitation to make using the API easier for the majority cases.

Support may be added for this use case if an actual use case is found.
