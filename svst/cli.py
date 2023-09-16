import sys

from svst import api

from typing import List

import argparse


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mypy", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("paths", nargs="+")

    arguments = parser.parse_args()

    errors_count: int = 0
    error_messages: List[str] = api.run(arguments.paths, mypy=arguments.mypy)
    for error_line in error_messages:
        errors_count += 1
        if not arguments.check:
            print(error_line)

    summary_message = (
        f"Found {errors_count} errors running svst and mypy."
        if arguments.mypy
        else f"Found {errors_count} errors running svst."
    )

    if errors_count:
        sys.exit(summary_message)
    else:
        print(summary_message)
