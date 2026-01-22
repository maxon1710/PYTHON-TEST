class Person:
    def __init__(self, name):
        self.__name = name

    @property
    def name(self):
        return self.__name

    def display_info(self):
        print(f"Name: {self.__name}")

class Employee(Person):
    def work(self):
        print(f"{self.name} works")

Tom  = Employee("Tom")
print(Tom.name)
print()
Tom.display_info()
Tom.work()
