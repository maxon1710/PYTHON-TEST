import random
import time

i = 0
while i < 1000:
    load = random.randint(0, 100)
    if load < 85:
        print(f"Нагрузка - {load}%")
    elif 85 < load < 100:
        print(f"Нагрузка — {load}% Крылышки в опасности!")
    elif load == 100:
        print(f"Нагрузка - {load}% ПОЗДРАВЛЯЮ, НАМ ПИЗДА!")
        break

    time.sleep(0.05)
    i += 1
