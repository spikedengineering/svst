import sys

import api


arguments = sys.argv[1:]

if arguments[0] == "--mypy":
    run_with_mypy: bool = True
    arguments = arguments[1:]
else:
    run_with_mypy: bool = False

for line in api.run(arguments, mypy=run_with_mypy):
    print(line)
