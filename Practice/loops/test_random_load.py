import random

def test_random_load():
    load = random.randint(1, 100)
    print("Нагрузка:", load)
    assert load <= 70
