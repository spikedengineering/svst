import re

from typing import List, Tuple, Optional

from mypy import api as mypy_api

from svst.config import read_configuration


config = read_configuration()


def is_ignored_file(root: str, file: str) -> bool:
    """Return if the file is ignored by the configuration."""

    if not file.endswith(".py"):
        return True

    if not config:
        return False

    for prefix_path in config["ignore_path_prefix"].split("\n")[1:]:  # todo
        if root.replace("./", "", 1).startswith(prefix_path):
            return True

    for directory in config["ignore_directory"].split("\n")[1:]:
        if directory in root:
            return True

    if file in config["ignored_file_names"].split("\n")[1:]:
        return True

    return False


def run_and_clean_mypy_output_in_path(
    path: str,
) -> List[str]:
    results: Tuple[str, str, int] = mypy_api.run([path])

    for error_message in results[0].split("\n")[:-2]:
        yield error_message


def ident_one_tab(parent_code_block, code_multi_line_string):
    string: str = parent_code_block + "\n"

    line: str
    for line in code_multi_line_string.splitlines():
        string += "    " + line + "\n"

    return string
