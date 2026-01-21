import pytest


def add(a, b):
    return a + b


@pytest.mark.parametrize(
    "a, b, expected",
    [
        pytest.param(1, 1, 2, id="1+1=2"),
        pytest.param(2, 3, 5, id="2+3=5"),
        pytest.param(10, 5, 15, id="10+5=15"),
    ],
)
def test_add(a, b, expected):
    assert add(a, b) == expected
