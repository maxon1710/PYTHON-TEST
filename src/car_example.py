class Car:
    def __init__(self, brand, model, year):
        self.brand = brand
        self.model = model
        self.year = year

    def print_car_info(self):
        print(f"Brand: {self.brand}, Model: {self.model}, Year: {self.year}")


# Создаём объекты
car1 = Car("Toyota", "Camry", 2020)
car2 = Car("Honda", "Civic", 2018)
car3 = Car("Ford", "Mustang", 2021)
