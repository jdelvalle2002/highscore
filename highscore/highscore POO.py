# simulador del juego highscore
# juego con tabla de 5x5

import random

class Tablero:
    def __init__(self, usuario):

        self.user = usuario
        self.p = 0 # puntaje
        self.matriz = []

    def gen_tablero(self):
        xd = []
        a = [0,0,0,0,0]
        i = 0
        while i < 5:
            xd.append(a[:])
            i += 1
        self.matriz = xd
    def dado(self):
        import random
        a = random.randint(1,6)
        b = random.randint(1,6)
        valor = a + b
        return valor    







pos_lugares = ["a1","a2","a3","a4","a5","b1","b2","b3","b4","b5", 
"c1", "c2", "c3", "c4", "c5", "d1", "d2", "d3", "d4", "d5", "e1", "e2", "e3", "e4", "e5"]
def gen_tablero():
    xd = []
    a = [0,0,0,0,0]
    i = 0
    while i < 5:
        xd.append(a[:])
        i += 1
    return xd    

def dado():
    a = random.randint(1,6)
    b = random.randint(1,6)
    valor = a+b
    return valor
def contar(lista):
    veces = []
    for i in range(2,13):
        t = lista.count(i)
        veces.append(t)
    return veces    


def escalas_7():
    lista = []
    for i in range(3,8):
        esc = range(i,i+5)
        lista.append(list(esc))
    return lista

def escalas_no7():
    lista = []
    for i in [2,8]:
        esc = range(i,i+5)
        lista.append(list(esc))
    return lista

def unpar(fila):
    pass

escalas7 = escalas_7()
print(escalas7)
escalasNo7 = escalas_no7()
print(escalasNo7)
# acá sacamos los puntajes
def contar_puntos(tablero):
    # filas
    for fila in tablero:
        if fila in x:
            pass
    # columnas
    # diagonales
    pass


times = contar(valores)
#print(times)


while True:
    lol = 0
    break