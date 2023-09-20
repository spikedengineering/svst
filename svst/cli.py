import sys

from svst import api, output

from typing import List

import argparse


def main() -> None:
    """CLI command method.

    Args:
        --mypy: Run svst alongside mypy.
        --check: Only print error count.

    Usage Example:
        svst \--mypy .

    Prints:
        Error messages and error count.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--mypy", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("paths", nargs="+")
    arguments = parser.parse_args()

    error_messages: List[str] = api.run(arguments.paths, mypy=arguments.mypy)

    errors_count: int = 0
    for error_line in error_messages:
        errors_count += 1
        if not arguments.check:
            print(output.output_string_converter_terminal(error_line), file=sys.stderr)

    summary_message = (
        f"Found {errors_count} errors running svst and mypy."
        if arguments.mypy
        else f"Found {errors_count} errors running svst."
    )

    if errors_count:
        print(summary_message, file=sys.stderr)
        sys.exit(1)
    else:
        print(summary_message)
