def indent_one_tab(parent_code_block: str, code_multi_line_string: str) -> str:
    """Ident one tab over a code string, and be able to inject a parent code block
    before the indentation start.

    This method was created for tests purpose.

    Args:
        parent_code_block: code block to be placed in the first line without any indentation.
        code_multi_line_string: code block to be indented.

    Returns:
        Code str with the parent_code_block on top and all the code_multi_line_string indented below.
    """

    string: str = parent_code_block + "\n"

    line: str
    for line in code_multi_line_string.splitlines():
        string += "    " + line + "\n"

    return string
