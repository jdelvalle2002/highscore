# simulador del juego highscore
# juego con tabla de 5x5
# funcionando para un jugador
# copia que imprime los puntakjes
import random

class Tablero:
    def __init__(self, usuario):

        self.user = usuario
        self.p = 0 # puntaje
        self.matriz = []

    def gen_tablero(self):
        xd = []
        a = [" "," "," "," "," "]
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
    def colocar(self,pos,num):
        col = pos[0]
        fil = int(pos[1])
        col = "abcde".find(col)
        self.matriz[fil-1][col] = num
    def print_tablero(self):
        t = self.matriz[:]
        # print("Tablero actual")
        top = "#"*11
        print(top)
        for l in t:
            for i in range(len(l)):
                f = lambda x : str(x)
                c = l[i]
                l[i] = f(c)
            s = "|".join(l)
            s = "|"+s+"|"
            print(s)
        print(top)        

pos_lugares = ["a1","a2","a3","a4","a5","b1","b2","b3","b4","b5", 
"c1", "c2", "c3", "c4", "c5", "d1", "d2", "d3", "d4", "d5", "e1", "e2", "e3", "e4", "e5"]
def gen_tablero():
    xd = []
    a = [" "," "," "," "," "]
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



# acá sacamos los puntajes
def contar_puntos(tablero):
    # funciones aux
    puntos = 0
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
    def full_f(lista):
        full = False
        for x in lista:
            if lista.count(x) == 3:
                for y in lista:
                    if lista.count(y) == 2:
                        full = True
        return full
    def five(lista):
        for el in lista:
            if lista.count(el) == 5:
                return True
        return False
    def poker(lista):
        for el in lista:
            if lista.count(el) == 4:
                return True
        return False
    def trio(lista):
        for el in lista:
            if lista.count(el) == 3:
                return True
        return False                        
    def dospar(lista):
        full = False
        for x in lista:
            if lista.count(x) == 2:
                for y in lista:
                    if lista.count(y) == 2 and x != y:
                        full = True
        return full
    def par(lista):
        for x in lista:
            if lista.count(x) == 2:
                return True
        return False            
    e7 = escalas_7()
    en7 = escalas_no7()
    
    # filas
    quintetos = tablero[:]
    for i in range(5):
        columna = []
        for j in range(5):
            columna.append(tablero[j][i])
        quintetos.append(columna)    
    diag = []
    line = []
    line2 = []
    for i in range(5):
        p = tablero[i][i]
        p2 = tablero[-(i+1)][i]
        line.append(p)
        line2.append(p2)
    diag.append(line)
    diag.append(line2)    
    for fila in quintetos:
        f  = sorted(fila)
        # ojo, acá importa el orden en q se llaman las funciones
        pts = 0
        if f in e7:
            pts = 8
            puntos += pts   
        elif f in en7:
            pts = 12
            puntos += pts
        elif full_f(f): # acá los full 
            pts = 8
            puntos += pts
        elif five(f):
            pts = 10
            puntos += pts
        elif poker(f):
            pts = 6
            puntos += pts
        elif trio(f):
            pts = 3
            puntos += pts
        elif dospar(f):
            pts = 3
            puntos += pts
        elif par(f):
            pts = 1
            puntos += pts

        print(f"La fila/columna {fila} suma {pts} pts")                   
    # diagonales
    for fila in diag:
        f  = sorted(fila)
        # ojo, acá importa el orden en q se llaman las funciones
        pts = 0
        if f in e7:
            pts = 16
            puntos += pts   
        elif f in en7:
            pts = 24
            puntos += pts
        elif full_f(f): # acá los full 
            pts = 16
            puntos += pts
        elif five(f):
            pts = 20
            puntos += pts
        elif poker(f):
            pts = 12
            puntos += pts
        elif trio(f):
            pts = 6
            puntos += pts
        elif dospar(f):
            pts = 6
            puntos += pts
        elif par(f):
            pts = 2
            puntos += pts

        print(f"La diagonal {fila} suma {pts} pts")
    #print("Diagonales")
    #print(diag)
    #print("Filas y col")
    #print(quintetos)
    return puntos


# para contar partir primero por las que ocupan más espacio

#times = contar(valores)
#print(times)

Player1 = Tablero("Joaco")
Player1.gen_tablero()
used = [] # lista de posiciones usadas
disp = pos_lugares[:]
reminder = "Recuerda, las columnas son letras y las filas son números"
print("Inicia el Juego!")
print(reminder)   
Player1.print_tablero() 
for i in range(1,26):
    print(f"-+-+-+- RONDA {i} -+-+-+-")
    valor = dado()
    print(f"Salió el: {valor}")
    go = True
    while go:
        print("Posiciones diponibles:")
        print(disp)
        jug = input("En qué casillero quieres ponerlo?: ")
        coor = jug.strip().lower()
        if type(coor[1]) != int:
            coor = coor[::-1]
        if coor not in pos_lugares:
            print("Posición inválida, intenta de nuevo.")
        if coor in used:
            print(f"Ya colocaste un número en la posición {coor}.")
            print(reminder)
        else:
            Player1.colocar(coor, valor)
            print(f"Pusiste un {valor} en la posición {coor}.")
            disp.remove(coor)
            used.append(coor)
            print("Tablero actual")
            Player1.print_tablero()
            go = False
print("FIN DEL JUEGO\nContemos el puntaje...")
print("Tablero final del jugador")

Player1.print_tablero()
Player1.p = contar_puntos(Player1.matriz)
print("El puntaje es", Player1.p)
