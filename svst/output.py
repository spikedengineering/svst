from typing import Optional
from typing_extensions import TypedDict

import re


class OutputTypedDict(TypedDict):
    file_name: Optional[str]
    line_number: int
    variable_name: str
    variable_scope: str


def output_structure_constructor(
    file_name: Optional[str],
    line_number: int,
    variable_name: str,
    variable_scope: str,
) -> OutputTypedDict:
    """Constructor for dictionary output.

    Args:
        file_name: Name of the file being analysed. None when parse_code is used on bare str.
        line_number: int number of the line where the error occurred.
        variable_name: Name of the variable where the error occurred.
        variable_scope: Scope of the variable where the error occurred.

    Returns:
        OutputTypedDict(TypedDict):
            file_name: Optional[str],
            line_number: int,
            variable_name: str,
            variable_scope: str
    """

    return {
        "file_name": file_name,
        "line_number": line_number,
        "variable_name": variable_name,
        "variable_scope": variable_scope,
    }


def output_string_constructor(
    output_structure: OutputTypedDict,
) -> str:
    """Constructor for string output.

    Args:
        output_structure:
            file_name: Optional[str],
            line_number: int,
            variable_name: str,
            variable_scope: str

    Returns:
        str: {file_name}:{line_number}: error: Variable "{variable_name}" is missing a
        standalone variable type annotation in the scope "{variable_scope}"  [no-untyped-var]
    """

    return (
        f"{output_structure['file_name']}:{output_structure['line_number']}: "
        f"error: {output_structure['variable_name']} is missing a type annotation in the "
        f"scope \"{output_structure['variable_scope']}\"  [no-untyped-var]"
    )


def output_string_converter_terminal(output_string: str):
    """Converts a plain error string into a colored printable one.

    Args:
        output_string: Plain `svst` error output string.

    Returns:
        Colored printable string.
    """

    match = re.search(
        r"^(\.)?(.+:)([0-9]+:)(.+:)(.+?(?=\[|))(\[[a-z\-]+\])?$", output_string
    )
    if not match:
        return output_string

    message: str = f"{match.group(2)}{match.group(3)}\033[31m{match.group(4)}\033[0m{match.group(5)}\033[33m{match.group(6)}\033[0m"

    return message
