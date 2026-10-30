import pytest

from svst import api


def errors(code: str):
    return [
        (error["line_number"], error["variable_name"], error["variable_scope"])
        for error in api.parse_code(code)
    ]


def test_annotation_does_not_leak_between_functions():
    code: str = """
def f() -> None:
    y: int = 1

def g() -> None:
    y = 2
"""
    assert errors(code) == [(6, "y", "g")]


def test_argument_name_does_not_leak_to_other_functions():
    code: str = """
def f(path: str) -> None:
    pass

def g() -> None:
    path = "a"
"""
    assert errors(code) == [(6, "path", "g")]


def test_annotation_after_assignment():
    code: str = """
x = 1
x: int = 2
"""
    assert errors(code) == [(2, "x", "global")]


@pytest.mark.parametrize(
    "code, expected",
    [
        ("a: int\na, *rest = [1, 2]\n", [(2, "rest", "global")]),
        ("if (n := 10) > 5:\n    pass\n", [(1, "n", "global")]),
        ("with open('f') as f:\n    pass\n", [(1, "f", "global")]),
        ("try:\n    pass\nexcept Exception as e:\n    pass\n", [(3, "e", "global")]),
        ("match 1:\n    case [p, *ps]:\n        pass\n", [(2, "p", "global"), (2, "ps", "global")]),
        (
            "async def f() -> None:\n    async for i in g():\n        pass\n"
            "    async with g() as c:\n        pass\n",
            [(2, "i", "f"), (4, "c", "f")],
        ),
        ("def f() -> None:\n    [y := i for i in range(3)]\n", [(2, "y", "f")]),
    ],
)
def test_bindings_are_checked(code, expected):
    assert errors(code) == expected


@pytest.mark.parametrize(
    "code",
    [
        "e: Exception\ntry:\n    pass\nexcept Exception as e:\n    pass\n",
        "n: int\nif (n := 10) > 5:\n    pass\n",
        "x: int = 0\ndef f() -> None:\n    global x\n    x = 1\n",
        "def f() -> None:\n    x: int = 0\n    def g() -> None:\n        nonlocal x\n        x = 1\n",
        "def f(x: int) -> None:\n    x = 2\n",
        "class A:\n    def m(self) -> None:\n        self.x = 1\n",
        "class A:\n    @classmethod\n    def m(cls) -> None:\n        pass\n",
        "D: int = 1\ndef f(a: int = D) -> None:\n    pass\n",
        "squares: list = [i * i for i in range(3)]\n",
        "f: object = lambda q: q\n",
    ],
)
def test_no_false_positives(code):
    assert errors(code) == []


def test_function_arguments():
    code: str = """
class A:
    @staticmethod
    def m(a, *args, b: int, **kwargs) -> None:
        pass
"""
    assert errors(code) == [
        (4, "a", "A.m"),
        (4, "args", "A.m"),
        (4, "kwargs", "A.m"),
    ]


def test_type_ignore_comment():
    code: str = """
a = 1  # type: ignore
b = 2  # type: ignore[no-untyped-var]
c = 3
"""
    assert errors(code) == [(4, "c", "global")]
