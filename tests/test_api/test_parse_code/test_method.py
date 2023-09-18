from svst import api, output

from tests import utils


def test_parse_code_simple_method_code(simple_code_1_error, simple_code_2_errors):
    logging_level: str = "ERROR"

    assert api.parse_code(
        utils.indent_one_tab("def some_method():", simple_code_1_error), logging_level
    ) == [
        output.output_structure_constructor(None, 5, "b", "some_method", logging_level)
    ]

    assert api.parse_code(
        utils.indent_one_tab("def some_method():", simple_code_2_errors), logging_level
    ) == [
        output.output_structure_constructor(None, 4, "a", "some_method", logging_level),
        output.output_structure_constructor(None, 5, "b", "some_method", logging_level),
    ]


def test_parse_code_for_method_code(for_code_no_errors, for_code_1_error):
    assert (
        api.parse_code(utils.indent_one_tab("def some_method():", for_code_no_errors))
        == []
    )

    logging_level: str = "ERROR"

    assert api.parse_code(
        utils.indent_one_tab("def some_method():", for_code_1_error), logging_level
    ) == [
        output.output_structure_constructor(None, 6, "i", "some_method", logging_level)
    ]


def test_parse_code_for_dict_method_code(
    for_dict_code_no_errors,
    for_dict_code_1_error,
    for_dict_code_1_other_error,
    for_dict_code_2_errors,
    for_dict_code_3_errors,
):
    assert (
        api.parse_code(
            utils.indent_one_tab("def some_method():", for_dict_code_no_errors)
        )
        == []
    )

    logging_level = "ERROR"

    assert api.parse_code(
        utils.indent_one_tab("def some_method():", for_dict_code_1_error), logging_level
    ) == [
        output.output_structure_constructor(
            None, 12, "value", "some_method", logging_level
        )
    ]

    assert api.parse_code(
        utils.indent_one_tab("def some_method():", for_dict_code_1_other_error),
        logging_level,
    ) == [
        output.output_structure_constructor(
            None, 12, "key", "some_method", logging_level
        )
    ]

    assert api.parse_code(
        utils.indent_one_tab("def some_method():", for_dict_code_2_errors),
        logging_level,
    ) == [
        output.output_structure_constructor(
            None, 10, "key", "some_method", logging_level
        ),
        output.output_structure_constructor(
            None, 10, "value", "some_method", logging_level
        ),
    ]

    assert api.parse_code(
        utils.indent_one_tab("def some_method():", for_dict_code_3_errors),
        logging_level,
    ) == [
        output.output_structure_constructor(
            None, 4, "test_dict", "some_method", logging_level
        ),
        output.output_structure_constructor(
            None, 10, "key", "some_method", logging_level
        ),
        output.output_structure_constructor(
            None, 10, "value", "some_method", logging_level
        ),
    ]
