from typing import Dict, Optional

from svst.constants import STANDARD_LOGGING_LEVEL


def output_structure_constructor(
    file_name: Optional[str],
    line_number: int,
    variable_name: str,
    variable_scope: str,
    logging_level: str = STANDARD_LOGGING_LEVEL,
) -> Dict:
    return {
        "file_name": file_name,
        "line_number": line_number,
        "variable_name": variable_name,
        "variable_scope": variable_scope,
        "logging_level": logging_level,
    }


def output_structure_text_constructor(
    output_structure: Dict,
) -> str:
    string = (
        f"{output_structure['file_name']}:{output_structure['line_number']}: "
        f"error: Variable \"{output_structure['variable_name']}\" is missing "
        f"a standalone variable type annotation in the "
        f"scope \"{output_structure['variable_scope']}\"  [no-untyped-var]"
    )

    # todo: logging

    return string
