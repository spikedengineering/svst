import pytest


@pytest.fixture
def simple_code_no_errors():
    return """
a: int = 1
b: int = 2  # line 4
"""


@pytest.fixture
def simple_code_1_error():
    return """
a: int = 1
b = 2  # line 4
"""


@pytest.fixture
def simple_code_2_errors():
    return """
a = 1
b = 2
"""


@pytest.fixture
def for_code_no_errors():
    return """
i: int

for i in range(1,5):
    print(i)
"""


@pytest.fixture
def for_code_1_error():
    return """
i

for i in range(1,5):
    print(i)
"""


@pytest.fixture
def for_dict_code_no_errors():
    return """
test_dict: Dict[str, int] = {
    "key_a": 1,
    "key_b": 2,
    "key_c": 3,
}

key: str
value: int

for key, value in test_dict.items():
    print(key, value)
"""


@pytest.fixture
def for_dict_code_1_error():
    return """
test_dict: Dict[str, int] = {
    "key_a": 1,
    "key_b": 2,
    "key_c": 3,
}

key: str

for key, value in test_dict.items():
    print(key, value)
"""


@pytest.fixture
def for_dict_code_1_other_error():
    return """
test_dict: Dict[str, int] = {
    "key_a": 1,
    "key_b": 2,
    "key_c": 3,
}

value: int

for key, value in test_dict.items():
    print(key, value)
"""


@pytest.fixture
def for_dict_code_2_errors():
    return """
test_dict: Dict[str, int] = {
    "key_a": 1,
    "key_b": 2,
    "key_c": 3,
}

for key, value in test_dict.items():
    print(key, value)
"""


@pytest.fixture
def for_dict_code_3_errors():
    return """
test_dict = {
    "key_a": 1,
    "key_b": 2,
    "key_c": 3,
}

for key, value in test_dict.items():
    print(key, value)
"""
