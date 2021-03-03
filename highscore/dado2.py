import random
def dado():
    a = random.randint(1,6)
    b = random.randint(1,6)
    valor = a+b
    return valor
a = dado()
print("valor:", a)