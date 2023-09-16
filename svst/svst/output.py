from typing import Optional
from typing_extensions import TypedDict

from svst import constants


class OutputTypedDict(TypedDict):
    file_name: Optional[str]
    line_number: int
    variable_name: str
    variable_scope: str
    logging_level: str


def output_structure_constructor(
    file_name: Optional[str],
    line_number: int,
    variable_name: str,
    variable_scope: str,
    logging_level: str = constants.STANDARD_LOGGING_LEVEL,
) -> OutputTypedDict:
    """Constructor for dictionary output."""

    return {
        "file_name": file_name,
        "line_number": line_number,
        "variable_name": variable_name,
        "variable_scope": variable_scope,
        "logging_level": logging_level,
    }


def output_string_constructor(
    output_structure: OutputTypedDict,
) -> str:
    """Constructor for string output."""

    return (
        f"{output_structure['file_name']}:{output_structure['line_number']}: "
        f"error: Variable \"{output_structure['variable_name']}\" is missing "
        f"a standalone variable type annotation in the "
        f"scope \"{output_structure['variable_scope']}\"  [no-untyped-var]"
    )
