import ast
import os
import io
import tokenize

from typing import Iterator, List, Tuple, Optional

from mypy import api as mypy_api

from svst import utils, output, parsing, constants


def get_lines_to_ignore(code: str) -> List[int]:
    """Read lines to ignore in a string of source code.

    Args:
        code: String of source code.

    Returns:
        List of lines to ignore.

    """
    type_ignore_string: str = "type: ignore"

    tokens: Iterator[tokenize.TokenInfo] = tokenize.tokenize(io.BytesIO(code.encode("utf-8")).readline)

    lines_to_ignore: List[int] = []
    token: tokenize.TokenInfo
    for token in tokens:
        if token.type == tokenize.COMMENT:
            if token.string.strip().endswith(
                type_ignore_string
            ) or token.string.endswith(f"{type_ignore_string}[{constants.ERROR_NAME}]"):
                lines_to_ignore.append(token.start[0])

    return lines_to_ignore


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
    tree: ast.Module = ast.parse(code, file_name or "<unknown>")
    lines_to_ignore: List[int] = get_lines_to_ignore(code)

    checker: parsing.VariableAnnotationChecker = parsing.VariableAnnotationChecker(
        file_name
    )
    checker.visit(tree)

    return [
        error_message
        for error_message in checker.error_messages
        if error_message["line_number"] not in lines_to_ignore
    ]


def mypy_run(
    path: str,
) -> Iterator[str]:
    """Use mypy api to analyse a path.

    Args:
        path: File or directory path string.

    Yields:
        `mypy` error string.
    """
    results: Tuple[str, str, int] = mypy_api.run([path])

    error_message: str
    for error_message in results[0].split("\n")[
        :-2
    ]:  # 2 lines removed at the end to clean the output
        yield error_message


def iter_python_files(path: str) -> Iterator[str]:
    """Yield the python files of a path that are not ignored by the configuration.

    Args:
        path: File or directory path string.

    Yields:
        File path strings.
    """
    if os.path.isfile(path):
        if not utils.is_ignored_file(os.path.dirname(path), os.path.basename(path)):
            yield path
        return

    root: str
    dirs: List[str]
    files: List[str]
    for root, dirs, files in os.walk(path):
        file: str
        for file in sorted(files):
            if not utils.is_ignored_file(root, file):
                yield os.path.join(root, file)


def run(
    path_list: List[str],
    mypy: bool = False,
) -> Iterator[str]:
    """Run path list.

    Args:
        path_list: List of file or directory path strings.
        mypy: Run mypy for the same `path_list`.

    Yields:
        str: {file_name}:{line_number}: error: Variable "{variable_name}" is missing a
        standalone variable type annotation in the scope "{variable_scope}"  [no-untyped-var]
    """

    path: str
    for path in path_list:
        file_path: str
        for file_path in iter_python_files(path):
            file_buffer: io.TextIOWrapper
            with open(file_path, "r", encoding="utf-8") as file_buffer:
                code: str = file_buffer.read()

            syntax_error: SyntaxError
            try:
                svst_errors: List[output.OutputTypedDict] = parse_code(code, file_path)
            except SyntaxError as syntax_error:
                yield f"{file_path}:{syntax_error.lineno}: error: {syntax_error.msg}  [syntax]"
                continue

            svst_error: output.OutputTypedDict
            for svst_error in svst_errors:
                yield output.output_string_constructor(svst_error)

        if mypy:
            line: str
            for line in mypy_run(path):
                yield line
