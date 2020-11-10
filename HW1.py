# Используя декоратор найти время исполнения функции
import random, time

def decorator(func):
    startTime = time.time()
    def wrapper(x):
        return func(x)
    print("work time: %f seconds" % (time.time() - startTime))
    return wrapper

def calculate(n):
    if n == 1 or n == 0:
        return 1
    else:
        return calculate(n - 1) + calculate(n - 2)

calculate = decorator(calculate)
rnd = int(random.random() * 100)
print(rnd)
print(calculate(rnd))
