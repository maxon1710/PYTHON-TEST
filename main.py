from src.car_example import Car
from src.DayWeek import day_of_week
from src.lead_example import Lead
from src.list_example import ListExample
from src.StudentTest import Student, get_avg_grades
from src.types_example import TypesExample, my_dict, my_list


def main():
    # 1) День недели
    n = int(input("Введите число от 1 до 7: "))
    print(day_of_week(n))

    print()

    # 2) Студенты
    student1 = Student("Max", 20, [5, 5, 4])
    student2 = Student("Anna", 19, [4, 4, 5])
    student3 = Student("Ivan", 21, [3, 4, 4])

    students = [student1, student2, student3]

    for student in students:
        avg = get_avg_grades(student)

        if student.name == "Max":
            if avg > 4.1:
                print("true")
            else:
                print("false")

    print()

    # 3) Чётность
    a = int(input("Введите число: "))

    if a % 2 == 0:
        print("Чётное")
    else:
        print("Нечётное")

    print()

    # 4) Машины
    car1 = Car("Toyota", "Camry", 2020)
    car2 = Car("Honda", "Civic", 2018)
    car3 = Car("Ford", "Mustang", 2021)

    car1.print_car_info()
    car2.print_car_info()
    car3.print_car_info()

    print()

    # 5) Lead
    lead = Lead("Alice")
    print("Before:", lead.name)
    lead.change_name("Bob")
    print("After:", lead.name)

    print()

    # 6) ListExample
    fruits = ListExample(["apple", "banana", "cherry", "strawberry"])
    print(fruits.get_items())

    print()

    # 7) TypesExample
    print("Список:", my_list)
    print("Словарь:", my_dict)

    x = 10
    y = x
    x += 5
    print("x =", x, "y =", y)

    te = TypesExample()
    print("Из класса:", te.nums)
    te.add(10)
    print("После добавления:", te.nums)


if __name__ == "__main__":
    main()
