from svst import output


def test_output_structure_constructor():
    file_name: str = "filename.py"
    line_number: int = 1
    variable_name: str = "a"
    variable_scope: str = "global"

    assert output.output_structure_constructor(
        file_name, line_number, variable_name, variable_scope
    ) == {
        "file_name": file_name,
        "line_number": line_number,
        "variable_name": variable_name,
        "variable_scope": variable_scope,
    }


def test_output_string_constructor():
    file_name: str = "filename.py"
    line_number: int = 1
    variable_name: str = "a"
    variable_scope: str = "global"

    output_structure: output.OutputTypedDict = output.output_structure_constructor(
        file_name, line_number, variable_name, variable_scope
    )

    assert output.output_string_constructor(output_structure) == (
        f'{file_name}:{line_number}: error: Variable "{variable_name}" is '
        f"missing a standalone variable type annotation in the "
        f'scope "{variable_scope}"  [no-untyped-var]'
    )
