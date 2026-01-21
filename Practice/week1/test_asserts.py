def f():
    return 4


def test_function():
    print("Функция вернула:", f())
    assert f() == 4
