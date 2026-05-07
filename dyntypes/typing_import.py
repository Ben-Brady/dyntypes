import ast
from . import astutils


def generate_typing_import(module: ast.Module) -> str:
    existing_import = _find_existing_typing_import(module)

    # TODO: Ensure it's an unsued name
    if existing_import:
        import_name = existing_import.asname or existing_import.name
        return import_name
    else:
        index = _find_slot_for_import(module)
        module.body.insert(index, astutils.import_("typing"))
        return "typing"


def _find_slot_for_import(module: ast.Module) -> int:
    # We need to ensure that we put the typing import
    # after any __future__ imports, as they need to
    # be the first thing in a file
    for x, node in enumerate(module.body):
        if (isinstance(node, ast.ImportFrom) and
                    len(node.names) == 1 and
                    node.names[0].name == "__future__"
                ):
            continue

        return x

    # if not spots are available, put it at the end
    return len(module.body)


def _find_existing_typing_import(module: ast.Module) -> ast.alias | None:
    for node in module.body:
        if not isinstance(node, ast.Import):
            continue

        for im in node.names:
            if im.name == "typing":
                return im

    return None
