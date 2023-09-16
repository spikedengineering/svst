from svst import api, output


def test_parse_code_simple_code(
    simple_code_no_errors, simple_code_1_error, simple_code_2_errors
):
    logging_level: str = "ERROR"

    assert api.parse_code(simple_code_no_errors, logging_level) == []

    assert api.parse_code(simple_code_1_error, logging_level) == [
        output.output_structure_constructor(None, 4, "b", "global", logging_level)
    ]

    assert api.parse_code(simple_code_2_errors, logging_level) == [
        output.output_structure_constructor(None, 3, "a", "global", logging_level),
        output.output_structure_constructor(None, 4, "b", "global", logging_level),
    ]


def test_parse_code_for_code(for_code_no_errors, for_code_1_error):
    assert api.parse_code(for_code_no_errors) == []

    logging_level: str = "WARNING"

    assert api.parse_code(for_code_1_error, logging_level) == [
        output.output_structure_constructor(None, 5, "i", "global", logging_level)
    ]


def test_parse_code_for_dict_code(
    for_dict_code_no_errors,
    for_dict_code_1_error,
    for_dict_code_1_other_error,
    for_dict_code_2_errors,
    for_dict_code_3_errors,
):
    logging_level = "ERROR"

    assert api.parse_code(for_dict_code_no_errors) == []

    assert api.parse_code(for_dict_code_1_error, logging_level) == [
        output.output_structure_constructor(None, 11, "value", "global", logging_level)
    ]

    assert api.parse_code(for_dict_code_1_other_error, logging_level) == [
        output.output_structure_constructor(None, 11, "key", "global", logging_level)
    ]

    assert api.parse_code(for_dict_code_2_errors, logging_level) == [
        output.output_structure_constructor(None, 9, "key", "global", logging_level),
        output.output_structure_constructor(None, 9, "value", "global", logging_level),
    ]

    assert api.parse_code(for_dict_code_3_errors, logging_level) == [
        output.output_structure_constructor(
            None, 3, "test_dict", "global", logging_level
        ),
        output.output_structure_constructor(None, 9, "key", "global", logging_level),
        output.output_structure_constructor(None, 9, "value", "global", logging_level),
    ]
