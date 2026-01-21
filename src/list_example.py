# src/list_example.py


class ListExample:
    def __init__(self, items=None):
        """Конструктор принимает список. Если ничего не передано — создаёт пустой список."""
        if items is None:
            items = []
        self.items = items

    def get_items(self):
        """Возвращает текущий список"""
        return self.items

    def filter_long_strings(self):
        """Возвращает строки длиной больше 5 символов"""
        return [s for s in self.items if len(s) > 5]


# ---------------------------
# Пример работы прямо при запуске
# ---------------------------
if __name__ == "__main__":
    fruits = ListExample(["apple", "banana", "cherry", "kiwi", "strawberry"])
    print("Все фрукты:", fruits.get_items())
    print("Длинные фрукты:", fruits.filter_long_strings())
