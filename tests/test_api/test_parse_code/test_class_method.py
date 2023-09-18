from svst import api, output

from tests import utils


def test_parse_code_simple_method_code(simple_code_1_error, simple_code_2_errors):
    logging_level: str = "ERROR"

    code: str = utils.indent_one_tab(
        "class SomeClass:",
        utils.indent_one_tab("def some_method():", simple_code_1_error),
    )

    assert api.parse_code(code, logging_level) == [
        output.output_structure_constructor(None, 6, "b", "some_method", logging_level)
    ]

    code: str = utils.indent_one_tab(
        "class SomeClass:",
        utils.indent_one_tab("def some_method():", simple_code_2_errors),
    )

    assert api.parse_code(code, logging_level) == [
        output.output_structure_constructor(None, 5, "a", "some_method", logging_level),
        output.output_structure_constructor(None, 6, "b", "some_method", logging_level),
    ]


def test_parse_code_for_method_code(for_code_no_errors, for_code_1_error):
    code: str = utils.indent_one_tab(
        "class SomeClass:",
        utils.indent_one_tab("def some_method():", for_code_no_errors),
    )
    assert api.parse_code(code) == []

    logging_level: str = "ERROR"

    code: str = utils.indent_one_tab(
        "class SomeClass:", utils.indent_one_tab("def some_method():", for_code_1_error)
    )

    assert api.parse_code(code, logging_level) == [
        output.output_structure_constructor(None, 7, "i", "some_method", logging_level)
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

    logging_level = "ERROR"

    code: str = utils.indent_one_tab(
        "class SomeClass:",
        utils.indent_one_tab("def some_method():", for_dict_code_1_error),
    )

    assert api.parse_code(code, logging_level) == [
        output.output_structure_constructor(
            None, 13, "value", "some_method", logging_level
        )
    ]

    code: str = utils.indent_one_tab(
        "class SomeClass:",
        utils.indent_one_tab("def some_method():", for_dict_code_1_other_error),
    )

    assert api.parse_code(
        code,
        logging_level,
    ) == [
        output.output_structure_constructor(
            None, 13, "key", "some_method", logging_level
        )
    ]

    code: str = utils.indent_one_tab(
        "class SomeClass:",
        utils.indent_one_tab("def some_method():", for_dict_code_2_errors),
    )

    assert api.parse_code(code, logging_level) == [
        output.output_structure_constructor(
            None, 11, "key", "some_method", logging_level
        ),
        output.output_structure_constructor(
            None, 11, "value", "some_method", logging_level
        ),
    ]

    code: str = utils.indent_one_tab(
        "class SomeClass:",
        utils.indent_one_tab("def some_method():", for_dict_code_3_errors),
    )

    assert api.parse_code(code, logging_level) == [
        output.output_structure_constructor(
            None, 5, "test_dict", "some_method", logging_level
        ),
        output.output_structure_constructor(
            None, 11, "key", "some_method", logging_level
        ),
        output.output_structure_constructor(
            None, 11, "value", "some_method", logging_level
        ),
    ]
