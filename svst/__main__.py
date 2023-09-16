import sys

import api

from typing import List


arguments = sys.argv[1:]

if arguments[0] == "--mypy":
    run_with_mypy: bool = True
    arguments = arguments[1:]
else:
    run_with_mypy: bool = False

errors_count: int = 0
error_messages: List[str] = api.run(arguments, mypy=run_with_mypy)
for error_line in error_messages:
    errors_count += 1
    print(error_line)

print(f"Found {errors_count} errors running", "svst and mypy." if run_with_mypy else "svst.")

