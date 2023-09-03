from typing import Dict

from svst import parsing


def test_output_structure_constructor():
    assert parsing.output_structure_constructor(None, 1, "a", "global", "DEBUG") == {
        "file_name": None,
        "line_number": 1,
        "variable_name": "a",
        "variable_scope": "global",
        "logging_level": "DEBUG",
    }

    assert parsing.output_structure_constructor(
        "filename.py", 2, "b", "some_method", "DEBUG"
    ) == {
        "file_name": "filename.py",
        "line_number": 2,
        "variable_name": "b",
        "variable_scope": "some_method",
        "logging_level": "DEBUG",
    }


def test_output_structure_text():
    file_name: str = "filename.py"
    line_number: int = 1
    variable_name: str = "error"
    variable_scope: str = "a"

    output_structure: Dict = parsing.output_structure_constructor(
        file_name, line_number, variable_name, variable_scope, "DEBUG"
    )

    assert parsing.output_structure_text_constructor(output_structure) == (
        f'{file_name}:{line_number}: error: Variable "{variable_name}" is '
        f"missing a standalone variable type annotation in the "
        f'scope "{variable_scope}"  [no-untyped-var]'
    )
