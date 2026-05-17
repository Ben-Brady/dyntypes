from dyntypes import Union, Literal, TypegenFailureWarning
import pytest
import typing as t
from utils import test
import warnings


@test("Union: generates correctly")
def _():
    testcases = {
        "Normal Union": (Union([int, str, bool]), t.Union[int, str, bool]),
        "Single Value": (Union([int]), t.Union[int]),
    }
    for case, (actual, expected) in testcases.items():
        assert actual == expected, f"{case} failed: {actual=} {expected=}"


@test("Union: invalid union returns Never with warning")
def _():
    testcases = {
        "Empty Union": lambda: Union([]),
    }
    for case, func in testcases.items():
        with pytest.warns(TypegenFailureWarning):
            value = func()

        assert value == t.Never, f"{case} failed: expected=Never {value=} "


@test("Literal: generates correctly")
def _():
    testcases = {
        "integer": (Literal(1), t.Literal[1]),
        "str": (Literal("foo"), t.Literal["foo"]),
    }
    for case, (actual, expected) in testcases.items():
        assert actual == expected, f"{case} failed: {actual=} {expected=}"


@test("Literal: invalid literal returns Never with warning")
def _():
    testcases = {
        "Type": lambda: Literal(int),  # type: ignore
        "Ellpisis": lambda: Literal(...),  # type: ignore
        "Object": lambda: Literal(Exception),  # type: ignore
        "Complex Number": lambda: Literal(1j),  # type: ignore
    }
    for case, func in testcases.items():
        with pytest.warns(TypegenFailureWarning):
            value = func()

        assert value == t.Never, f"{case} failed: expected=Never {value=} "
