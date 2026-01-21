import pytest


def test_div_zero():
    print("Проверяем деление на 0")
    with pytest.raises(ZeroDivisionError):
        print("Сейчас будет 1/0")
        1 / 0
    print("Исключение поймано усешно")
