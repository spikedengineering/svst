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
    """Constructor for dictionary output.

    Args:
        file_name: Name of the file being analysed. None when parse_code is used on bare str.
        line_number: int number of the line where the error occurred.
        variable_name: Name of the variable where the error occurred.
        variable_scope: Scope of the variable where the error occurred.
        logging_level: str of logging level configuration.

    Returns:
        A Dict that contains the info of the svst errors:

       {
           "file_name": "some_file.py",
           "line_number": 6,
           "variable_name": "yet_another_variable",
           "variable_scope": "some_method",
           "logging_level": "DEBUG",
       }

       This dictionary is the first layer of svst errors construction.
    """

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
    """Constructor for string output.

    Args:
        output_structure: {
           "file_name": "some_file.py",
           "line_number": 6,
           "variable_name": "yet_another_variable",
           "variable_scope": "some_method",
           "logging_level": "DEBUG",
       }

    Returns:
        str: {file_name}:{line_number}: error: Variable "{variable_name}" is missing a
        standalone variable type annotation in the scope "{variable_scope}"  [no-untyped-var]
    """

    return (
        f"{output_structure['file_name']}:{output_structure['line_number']}: "
        f"error: Variable \"{output_structure['variable_name']}\" is missing "
        f"a standalone variable type annotation in the "
        f"scope \"{output_structure['variable_scope']}\"  [no-untyped-var]"
    )
