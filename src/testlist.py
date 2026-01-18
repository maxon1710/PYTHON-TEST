number = list(range(15))

for n in number:
    if n > 7:
        print(f"Далее значние больше доступного = {n}")
        break
    print(n)

print()

number1 = [f"str {n}" for n in range(8)]
for n in number1:
    print(n)
