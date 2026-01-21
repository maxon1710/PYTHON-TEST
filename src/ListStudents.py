numList = [0, 1, 2]
engList = ["zero", "one", "two"]
espList = ["cero", "uno", "dos"]

print(list(zip(numList, engList, espList)))

for num, eng, esp in zip(numList, engList, espList):
    print(f"{num} is {eng} in English and {esp} in Spanish.")

Eng = list(zip(engList, espList, numList))
Eng.sort()
a, b, c = zip(*Eng)

print(a)
print(b)
print(c)

upperCase = ["A", "B", "C", "D"]
lowerCase = ["a", "b", "c", "d"]
for i, (upper, lower) in enumerate(zip(upperCase, lowerCase), 1):
    print(f"{i}: {upper} and {lower}.")


def gen(n):
    while True:
        yield n
        n += 2


print()

G = gen(3)

print(next(G))
print(next(G))
print(next(G))
print(next(G))
print(next(G))
print(next(G))
print(next(G))
print(next(G))
