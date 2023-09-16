import ast
import os
import io

from svst import utils, output, parsing

from typing import List, Optional

from svst import constants


def parse_code(
    code: str,
    logging_level: str = constants.STANDARD_LOGGING_LEVEL,
    file_name: Optional[str] = None,
) -> List[output.OutputTypedDict]:
    """Parse code directly and return a list of output dictionaries."""

    tree = ast.parse(code)
    ast.increment_lineno(tree)
    ast.fix_missing_locations(tree)
    parsing.ParentNodeTransformer().visit(tree)
    visitor = parsing.StaticTypeEnforcer(file_name, logging_level)
    visitor.visit(tree)

    return visitor.output


def run(
    path_list: List[str],
    logging_level: str = constants.STANDARD_LOGGING_LEVEL,
    mypy: bool = False,
) -> List[str]:
    """Run path list."""

    path: str
    for path in path_list:
        root: str
        dirs: List[str]
        files: List[str]
        for root, dirs, files in os.walk(path):
            file: str
            for file in files:
                if utils.is_ignored_file(root, file):
                    continue

                file_path: str = os.path.join(root, file)

                file_buffer: io.TextIOWrapper
                with open(file_path, "r") as file_buffer:
                    svst_errors = parse_code(
                        file_buffer.read(), logging_level, file_path[2:]
                    )
                    for svst_error in svst_errors:
                        yield output.output_string_constructor(svst_error)

        if mypy:
            for line in utils.run_and_clean_mypy_output_in_path(path):
                yield line
