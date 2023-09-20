from svst import api, output


def test_parse_code_simple_code(
    simple_code_no_errors, simple_code_1_error, simple_code_2_errors
):
    assert api.parse_code(simple_code_no_errors) == []

    assert api.parse_code(simple_code_1_error) == [
        output.output_structure_constructor(None, 4, "b", "global")
    ]

    assert api.parse_code(simple_code_2_errors) == [
        output.output_structure_constructor(None, 3, "a", "global"),
        output.output_structure_constructor(None, 4, "b", "global"),
    ]


def test_parse_code_for_code(for_code_no_errors, for_code_1_error):
    assert api.parse_code(for_code_no_errors) == []

    logging_level: str = "WARNING"

    assert api.parse_code(for_code_1_error) == [
        output.output_structure_constructor(None, 5, "i", "global")
    ]


def test_parse_code_for_dict_code(
    for_dict_code_no_errors,
    for_dict_code_1_error,
    for_dict_code_1_other_error,
    for_dict_code_2_errors,
    for_dict_code_3_errors,
):
    assert api.parse_code(for_dict_code_no_errors) == []

    assert api.parse_code(for_dict_code_1_error) == [
        output.output_structure_constructor(None, 11, "value", "global")
    ]

    assert api.parse_code(for_dict_code_1_other_error) == [
        output.output_structure_constructor(None, 11, "key", "global")
    ]

    assert api.parse_code(for_dict_code_2_errors) == [
        output.output_structure_constructor(None, 9, "key", "global"),
        output.output_structure_constructor(None, 9, "value", "global"),
    ]

    assert api.parse_code(for_dict_code_3_errors) == [
        output.output_structure_constructor(None, 3, "test_dict", "global"),
        output.output_structure_constructor(None, 9, "key", "global"),
        output.output_structure_constructor(None, 9, "value", "global"),
    ]
