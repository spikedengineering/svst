import ast
import os
import io

from svst import utils, output, parsing

from typing import List, Tuple, Optional

from mypy import api as mypy_api


def parse_code(
    code: str,
    file_name: Optional[str] = None,
) -> List[output.OutputTypedDict]:
    """Parse code directly and return a list of output dictionaries.

    Args:
        code: String of python code.
        file_name: Path of the file being analysed.

    Returns:
        A list of OutputTypedDict that contain the info of the svst error.
    """

    tree = ast.parse(code)
    ast.increment_lineno(tree)
    ast.fix_missing_locations(tree)
    parsing.ParentNodeTransformer().visit(tree)
    visitor = parsing.StaticTypeEnforcer(file_name)
    visitor.visit(tree)

    return visitor.output


def mypy_run(
    path: str,
) -> List[str]:
    """Use mypy api to analyse a path.

    Args:
        path: File or directory path string.

    Yields:
        `mypy` error string.
    """
    results: Tuple[str, str, int] = mypy_api.run([path])

    for error_message in results[0].split("\n")[
        :-2
    ]:  # 2 lines removed at the end to clean the output
        yield error_message


def run(
    path_list: List[str],
    mypy: bool = False,
) -> List[str]:
    """Run path list.

    Args:
        path_list: List of path strings.
        mypy: Run mypy for the same `path_list`.

    Yields:
        str: {file_name}:{line_number}: error: Variable "{variable_name}" is missing a
        standalone variable type annotation in the scope "{variable_scope}"  [no-untyped-var]
    """

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
                    svst_errors = parse_code(file_buffer.read(), file_path)

                    for svst_error in svst_errors:
                        yield output.output_string_constructor(svst_error)

        if mypy:
            for line in mypy_run(path):
                yield line
