# src/types_example.py

# Изменяемые типы
my_list = [1, 2, 3]
my_dict = {"a": 1, "b": 2}
my_list.append(4)
my_dict["c"] = 3


# Неизменяемые типы
x = 10
y = x
x += 5


# Мини-класс с числами
class TypesExample:
    def __init__(self):
        self.nums = [1, 2, 3]
    def add(self, n):
        self.nums.append(n)

