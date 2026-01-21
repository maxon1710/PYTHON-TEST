numbers = [3, 15, -7, 22, 8, 4, 19, 0, 11]

max_value = numbers[0]  # берём первое число за базу

for num in numbers:
    if num > max_value:
        max_value = num

print("Максимальное число:", max_value)
