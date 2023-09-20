from svst import api
from svst import output


def test_run_file_simple_code():
    code: str = """
a: int = 1
b = 2  # line 4
    """

    assert api.parse_code(code) == [
        output.output_structure_constructor(None, 4, "b", "global")
    ]

    code: str = """
a = 1
b = 2
    """

    assert api.parse_code(code) == [
        output.output_structure_constructor(None, 3, "a", "global"),
        output.output_structure_constructor(None, 4, "b", "global"),
    ]


def test_run_file_for_code():
    code: str = """
i: int

for i in range(1,5):
    print(i)
    """

    assert api.parse_code(code) == []

    code: str = """
i

for i in range(1,5):
    print(i)
    """

    logging_level: str = "WARNING"

    assert api.parse_code(code) == [
        output.output_structure_constructor(None, 5, "i", "global")
    ]


def test_run_file_for_dict_items_code():
    code: str = """
test_dict: Dict[str, int] = {
    "key_a": 1,
    "key_b": 2,
    "key_c": 3,
}

key: str
value: int

for key, value in test_dict.items():
    print(key, value)
    """

    assert api.parse_code(code) == []

    code: str = """
test_dict: Dict[str, int] = {
    "key_a": 1,
    "key_b": 2,
    "key_c": 3,
}

key: str

for key, value in test_dict.items():
    print(key, value)
    """

    assert api.parse_code(code) == [
        output.output_structure_constructor(None, 11, "value", "global")
    ]

    code: str = """
test_dict: Dict[str, int] = {
    "key_a": 1,
    "key_b": 2,
    "key_c": 3,
}

value: int

for key, value in test_dict.items():
    print(key, value)
    """

    assert api.parse_code(code) == [
        output.output_structure_constructor(None, 11, "key", "global")
    ]

    code: str = """
test_dict: Dict[str, int] = {
    "key_a": 1,
    "key_b": 2,
    "key_c": 3,
}

for key, value in test_dict.items():
    print(key, value)
    """

    assert api.parse_code(code) == [
        output.output_structure_constructor(None, 9, "key", "global"),
        output.output_structure_constructor(None, 9, "value", "global"),
    ]
