class Student:
    def __init__(self, name, age, grades):
        self.name = name
        self.age = age
        self.grades = grades


def get_avg_grades(student):
    return sum(student.grades) / len(student.grades)


def describe_student(student):
    match student:
        case Student(name="Max", age=_, grades=_):
            return "TOP student"

        case Student(name=_, age=age, grades=_) if age < 20:
            return "Young student"

        case Student(name=_, age=_, grades=grades) if get_avg_grades(student) > 4.5:
            return "Excellent"

        case _:
            return "Normal"


students = [
    Student("Max", 20, [5, 5, 4]),
    Student("Anna", 19, [4, 4, 5]),
    Student("Ivan", 21, [3, 4, 4]),
]

for s in students:
    print(s.name, "->", describe_student(s))
