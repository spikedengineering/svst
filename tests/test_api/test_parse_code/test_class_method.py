from svst import api, output

from tests import utils


def test_parse_code_simple_method_code(simple_code_1_error, simple_code_2_errors):
    code: str = utils.indent_one_tab(
        "class SomeClass:",
        utils.indent_one_tab("def some_method():", simple_code_1_error),
    )

    assert api.parse_code(code) == [
        output.output_structure_constructor(None, 5, "b", "SomeClass.some_method")
    ]

    code: str = utils.indent_one_tab(
        "class SomeClass:",
        utils.indent_one_tab("def some_method():", simple_code_2_errors),
    )

    assert api.parse_code(code) == [
        output.output_structure_constructor(None, 4, "a", "SomeClass.some_method"),
        output.output_structure_constructor(None, 5, "b", "SomeClass.some_method"),
    ]


def test_parse_code_for_method_code(for_code_no_errors, for_code_1_error):
    code: str = utils.indent_one_tab(
        "class SomeClass:",
        utils.indent_one_tab("def some_method():", for_code_no_errors),
    )

    assert api.parse_code(code) == []

    code: str = utils.indent_one_tab(
        "class SomeClass:", utils.indent_one_tab("def some_method():", for_code_1_error)
    )

    assert api.parse_code(code) == [
        output.output_structure_constructor(None, 6, "i", "SomeClass.some_method")
    ]


def test_parse_code_for_dict_method_code(
    for_dict_code_no_errors,
    for_dict_code_1_error,
    for_dict_code_1_other_error,
    for_dict_code_2_errors,
    for_dict_code_3_errors,
):
    code: str = utils.indent_one_tab(
        "class SomeClass:",
        utils.indent_one_tab("def some_method():", for_dict_code_no_errors),
    )

    assert api.parse_code(code) == []

    code: str = utils.indent_one_tab(
        "class SomeClass:",
        utils.indent_one_tab("def some_method():", for_dict_code_1_error),
    )

    assert api.parse_code(code) == [
        output.output_structure_constructor(None, 12, "value", "SomeClass.some_method")
    ]

    code: str = utils.indent_one_tab(
        "class SomeClass:",
        utils.indent_one_tab("def some_method():", for_dict_code_1_other_error),
    )

    assert api.parse_code(
        code,
    ) == [output.output_structure_constructor(None, 12, "key", "SomeClass.some_method")]

    code: str = utils.indent_one_tab(
        "class SomeClass:",
        utils.indent_one_tab("def some_method():", for_dict_code_2_errors),
    )

    assert api.parse_code(code) == [
        output.output_structure_constructor(None, 10, "key", "SomeClass.some_method"),
        output.output_structure_constructor(None, 10, "value", "SomeClass.some_method"),
    ]

    code: str = utils.indent_one_tab(
        "class SomeClass:",
        utils.indent_one_tab("def some_method():", for_dict_code_3_errors),
    )

    assert api.parse_code(code) == [
        output.output_structure_constructor(None, 4, "test_dict", "SomeClass.some_method"),
        output.output_structure_constructor(None, 10, "key", "SomeClass.some_method"),
        output.output_structure_constructor(None, 10, "value", "SomeClass.some_method"),
    ]
