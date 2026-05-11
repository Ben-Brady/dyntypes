from dyntypes.resolve import is_literal_type, is_literal_value, value_to_ast
from utils import test

@test("is_literal_value: accepts valid literals")
def _():
    testcases = [
        123,
        "asdasd",
        False,
        True,
        None
    ]
    for case in testcases:
        assert is_literal_value(case), f"{case} was said to not be a literal"

@test("is_literal_value: doesn't accept invalid literals")
def _():
    testcases = [
        1j,
        {1: 1, 2:2, 3:3},
        {1,2,3},
        [1,2,3]
    ]
    for case in testcases:
        assert not is_literal_value(case), f"{case} was said to not be a literal"
