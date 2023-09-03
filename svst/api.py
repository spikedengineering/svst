import ast

from typing import Dict, List, Union

from svst.parsing import ParentNodeTransformer, StaticTypeEnforcer


def parse_code(code: str) -> List[Dict[str, Union[str, int]]]:
    tree = ast.parse(code)
    ast.increment_lineno(tree)
    ast.fix_missing_locations(tree)
    ParentNodeTransformer().visit(tree)
    visitor = StaticTypeEnforcer()
    visitor.visit(tree)

    # todo: print visitor.output with the print_formater

    return visitor.output


# parse_code("parsing.py")
