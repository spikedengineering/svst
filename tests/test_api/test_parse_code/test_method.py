from svst import api
from svst.parsing import output_structure_constructor


def test_parse_code_simple_method_code():
    code: str = """
def some_method():
    a: int = 1
    b = 2  # line 5
    """

    logging_level: str = "ERROR"

    assert api.parse_code(code, logging_level) == [
        output_structure_constructor(None, 5, "b", "some_method", logging_level)
    ]

    code: str = """
def some_method():
    a = 1
    b = 2
    """

    logging_level: str = "ERROR"

    assert api.parse_code(code, logging_level) == [
        output_structure_constructor(None, 4, "a", "some_method", logging_level),
        output_structure_constructor(None, 5, "b", "some_method", logging_level),
    ]


def test_parse_code_for_method_code():
    code: str = """
def some_method():
    i: int

    for i in range(1,5):
        print(i)
    """

    assert api.parse_code(code) == []

    code: str = """
def some_method():
    i

    for i in range(1,5):
        print(i)
    """

    logging_level: str = "WARNING"

    assert api.parse_code(code, logging_level) == [
        output_structure_constructor(None, 6, "i", "some_method", logging_level)
    ]


def test_parse_code_for_dict_items_method_code():
    code: str = """
def some_method():
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
def some_method():
    test_dict: Dict[str, int] = {
        "key_a": 1,
        "key_b": 2,
        "key_c": 3,
    }

    key: str

    for key, value in test_dict.items():
        print(key, value)
        """

    logging_level = "ERROR"

    assert api.parse_code(code, logging_level) == [
        output_structure_constructor(None, 12, "value", "some_method", logging_level)
    ]

    code: str = """
def some_method():
    test_dict: Dict[str, int] = {
        "key_a": 1,
        "key_b": 2,
        "key_c": 3,
    }

    value: int

    for key, value in test_dict.items():
        print(key, value)
    """

    logging_level = "ERROR"

    assert api.parse_code(code, logging_level) == [
        output_structure_constructor(None, 12, "key", "some_method", logging_level)
    ]

    code: str = """
def some_method():
    test_dict: Dict[str, int] = {
        "key_a": 1,
        "key_b": 2,
        "key_c": 3,
    }

    for key, value in test_dict.items():
        print(key, value)
    """

    logging_level = "ERROR"

    assert api.parse_code(code, logging_level) == [
        output_structure_constructor(None, 10, "key", "some_method", logging_level),
        output_structure_constructor(None, 10, "value", "some_method", logging_level),
    ]
