import re

from typing import List, Tuple, Optional

from mypy import api as mypy_api

from config import read_configuration


def is_ignored_file(root: str, file: str) -> bool:
    """Return if the file is ignored by the configuration."""

    if not file.endswith(".py"):
        return True

    config = read_configuration()
    if not config:
        return False

    for prefix_path in config["ignore_path_prefix"].split("\n")[1:]:
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

    # # Remove Summary to Group Errors
    # match_deleting_content: Optional[re.Match[str]] = re.search(
    #     r"Found [0-9]+ errors in [0-9]+ " r"files \(checked [0-9]+ source files\)",
    #     error_messages,
    # )
    # if match_deleting_content:
    #     deleting_content: str = match_deleting_content.group()
    #     error_messages = error_messages.replace(deleting_content + "\n", "")
    #
    # return error_messages


def ident_one_tab(parent_code_block, code_multi_line_string):
    string: str = parent_code_block + "\n"

    line: str
    for line in code_multi_line_string.splitlines():
        string += "    " + line + "\n"

    return string
