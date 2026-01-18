class Student:
    def __init__(self, name, age, grades):
        self.name = name
        self.age = age
        self.grades = grades

def get_avg_grades(student):
    total = sum(student.grades)
    count = len(student.grades)
    return total / count

