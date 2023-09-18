import re

from typing import List, Tuple, Optional

from mypy import api as mypy_api

from svst.config import read_configuration


config = read_configuration()


def is_ignored_file(root: str, file: str) -> bool:
    """Return if the file is ignored by the configuration.

    Args:
        root: Directory path str.
        file: Name of the file.

    Returns:
        If the file needs to be ignored based on the configurations.
    """

    if not file.endswith(".py"):
        return True

    if not config:
        return False

    for prefix_path in (
        [item for item in config["ignore_path_prefix"].split("\n") if item]
        if "ignore_path_prefix" in config
        else []
    ):
        if root.replace("./", "", 1).startswith(prefix_path):
            return True

    for directory in (
        [item for item in config["ignore_directory"].split("\n") if item]
        if "ignore_directory" in config
        else []
    ):
        if directory in root:
            return True

    if (
        file in [item for item in config["ignored_file_names"].split("\n") if item]
        if "ignored_file_names" in config
        else []
    ):
        return True

    return False


def run_and_clean_mypy_output_in_path(
    path: str,
) -> List[str]:
    """Use mypy api to analyse a directory or file.

    Args:
        path: file or directory path str.

    Returns:
        str:
    """
    results: Tuple[str, str, int] = mypy_api.run([path])

    for error_message in results[0].split("\n")[:-2]:
        yield error_message


def indent_one_tab(parent_code_block: str, code_multi_line_string: str) -> str:
    """Ident one tab over a code string, and be able to inject a parent code block
    before the indentation start.

    This method was created for tests purpose.

    Args:
        parent_code_block: code block to be placed in the first line without any indentation.
        code_multi_line_string: code block to be indented.

    Returns:
        Code str with the parent_code_block on top and all the code_multi_line_string indented below.
    """

    string: str = parent_code_block + "\n"

    line: str
    for line in code_multi_line_string.splitlines():
        string += "    " + line + "\n"

    return string
