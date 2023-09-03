from svst import api
from svst.parsing import output_structure_constructor


def test_parse_code():
    code = """
a: int = 1
b = 2  # line 4
    """

    assert api.parse_code(code) == [
        output_structure_constructor(None, 4, "error", "b", "global")
    ]
