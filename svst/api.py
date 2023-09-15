import ast
import os
import io
import re

from typing import Dict, List, Union, Tuple, Optional

from svst.constants import (
    STANDARD_LOGGING_LEVEL,
    IGNORED_FILE_NAMES,
    IGNORED_INSIDE_DIRECTORY,
    IGNORED_PATH_STARTS_WITH,
)

from svst.parsing import ParentNodeTransformer, StaticTypeEnforcer

from svst.output import output_structure_text_constructor

from mypy import api as mypy_api


def parse_code(
    code: str, logging_level: str = STANDARD_LOGGING_LEVEL
) -> List[Dict[str, Union[str, int]]]:
    tree = ast.parse(code)
    ast.increment_lineno(tree)
    ast.fix_missing_locations(tree)
    ParentNodeTransformer().visit(tree)
    visitor = StaticTypeEnforcer(logging_level=logging_level)
    visitor.visit(tree)

    return visitor.output


def run(
    path: str,
    logging_level: str = STANDARD_LOGGING_LEVEL,
    mypy: bool = False,
):
    error_messages: List[str] = []

    root: str
    dirs: List[str]
    files: List[str]
    for root, dirs, files in os.walk(path):
        file: str
        for file in files:
            for pre_path in IGNORED_PATH_STARTS_WITH:
                if root.startswith(pre_path):
                    continue
                continue

            for directory in IGNORED_INSIDE_DIRECTORY:
                if directory in root:
                    continue

            if file in IGNORED_FILE_NAMES:
                continue

            if file.endswith(".py"):
                file_name: str = os.path.join(root, file)

                file_buffer: io.TextIOWrapper
                with open(file_name, "r") as file_buffer:
                    error_messages = []
                    svst_errors = parse_code(file_buffer.read(), logging_level)
                    for svst_error in svst_errors:
                        error_messages += output_structure_text_constructor(svst_error)

            if mypy:
                results: Tuple[str, str, int] = mypy_api.run([path])

                error_messages += results[0]

                # Remove Summary to Group Errors
                match_deleting_content: Optional[re.Match[str]] = re.search(
                    r"Found [0-9]+ errors in [0-9]+ files "
                    r"\(checked [0-9]+ source files\)",
                    error_messages,
                )
                if match_deleting_content:
                    deleting_content: str = match_deleting_content.group()
                    error_messages = error_messages.replace(deleting_content + "\n", "")

            return error_messages
