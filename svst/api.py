import ast
import os
import io
import tokenize

from typing import Iterator, List, Tuple, Optional

from mypy import api as mypy_api

from svst import utils, output, parsing, constants


def get_lines_to_ignore(code):
    lines_to_ignore = set()
    tokens = tokenize.tokenize(io.BytesIO(code.encode("utf-8")).readline)

    type_ignore_string_prefix: str = "type: ignore"
    for tok in tokens:
        if tok.type == tokenize.COMMENT:
            if tok.string.strip().endswith(
                type_ignore_string_prefix
            ) or tok.string.endswith(
                f"{type_ignore_string_prefix}[{constants.ERROR_NAME}]"
            ):
                lines_to_ignore.add(tok.start[0])

    return lines_to_ignore


def parse_code(
    code: str,
    file_name: Optional[str] = None,
) -> Iterator[output.OutputTypedDict]:
    """Parse code directly and return a list of output dictionaries.

    Args:
        code: String of python code.
        file_name: Path of the file being analysed.

    Returns:
        A list of OutputTypedDict that contain the info of the svst error.
    """
    tree = ast.parse(code, file_name)
    lines_to_ignore = get_lines_to_ignore(code)

    checker = parsing.VariableAnnotationChecker(file_name)
    checker.visit(tree)

    for error_message in checker.error_messages:
        if error_message["line_number"] not in lines_to_ignore:
            yield error_message


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
