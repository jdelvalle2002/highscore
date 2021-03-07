# basado en https://codereview.stackexchange.com/questions/191550/minesweeper-in-python-tkinter

# juego hecho por jdelvalle2002

import tkinter, configparser, os, random, tkinter.messagebox, tkinter.simpledialog, webbrowser
from tkinter.font import BOLD
from tkinter.constants import LEFT

window = tkinter.Tk()
window.geometry("440x480")
window.title("Highscore - by jdelvalle2002")
def dado():
    a = random.randint(1,6)
    b = random.randint(1,6)
    valor = a+b
    return valor
#prepare default values

rows = 5
cols = 5


class Tablero:
    def __init__(self, usuario):

        self.user = usuario
        self.p = 0 # puntaje
        self.matriz = []
        self.msj = []

    def gen_tablero(self):
        xd = []
        a = [" "," "," "," "," "]
        i = 0
        while i < 5:
            xd.append(a[:])
            i += 1
        self.matriz = xd

    def print_tablero(self):
        def fill(s):
            if len(s) < 2:
                return " "+s
            else:
                return s    
        t = self.matriz[:]
        # print("Tablero actual")
        top = "#"*16
        second = "    a  b  c  d  e"
        print(top)
        print(second)
        co = 1
        for l in t:
            for i in range(len(l)):
                f = lambda x : fill(str(x))
                c = l[i]
                l[i] = f(c)

            s = "|".join(l)
            s = str(co) + ") |"+s+"|"
            print(s)
            co += 1
        print(top)   
    def contar_puntos(self):
        tablero = self.matriz
        mensajes = []
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
                columna.append(tablero[j][i]) ##### .strip()
            quintetos.append(columna)    
        diag = []
        line = []
        line2 = []
        for i in range(5):
            p = tablero[i][i]#.strip()
            p2 = tablero[-(i+1)][i]#.strip()
            line.append(p)
            line2.append(p2)    
        diag.append(line)
        diag.append(line2)
        #diag.append(["2","4","6","5","3"]) #debug
        for fila in quintetos:
            f  = sorted(list(map(int,fila)))
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
            m = f"La fila/columna {fila} suma {pts} pts"    
            mensajes.append(m)
            #print(m)                   
        # diagonales
        for fila in diag:
            f  = sorted(list(map(int,fila)))
            #print(f)
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
            m = f"La diagonal {fila} suma {pts} pts"
            mensajes.append(m)
            #print(m)
        #print("Diagonales")
        #print(diag)
        #print("Filas y col")
        #print(quintetos)
        self.msj = mensajes
        return puntos


def prepareWindow():
    global rows, cols, buttons
    res = tkinter.Button(window, text="Restart", command=restartGame).grid(row=0, column=0, columnspan=cols, sticky=tkinter.N+tkinter.W+tkinter.S+tkinter.E)
    hel = tkinter.Button(window, text="Help", command=help_button).grid(row=6, column=0, columnspan=cols, sticky=tkinter.N+tkinter.W+tkinter.S+tkinter.E)
    # res.place(relx=0.5, rely=0.5, anchor=CENTER)
    buttons = []
    for x in range(0, rows):
        buttons.append([])
        for y in range(0, cols):
            if x==y or 4-x == y:
                b = tkinter.Button(window, bg= "cyan", text="-", font="Courier 16 bold", width=6, height=2, command=lambda x=x,y=y: clickOn(x,y))
            else:
                b = tkinter.Button(window, text="-", font="Courier 16 bold", width=6, height=2, command=lambda x=x,y=y: clickOn(x,y))
            #b.bind("<Button-3>", lambda e, x=x, y=y:onRightClick(x, y))
            b.grid(row=x+1, column=y, sticky=tkinter.N+tkinter.W+tkinter.S+tkinter.E)
            buttons[x].append(b)

def help_button():
    webbrowser.open("https://highscore-on-python.netlify.app/")
def clickOn(x,y):
    global rounds, buttons, colors, rows, cols, valor, Board, ronda, el_dado
    
    buttons[x][y]["text"] = str(valor) #str(field[x][y])
    
    #buttons[x][y].config(disabledforeground=colors[field[x][y]])

    buttons[x][y]['state'] = 'disabled'
    buttons[x][y].config(relief=tkinter.SUNKEN)
    Board.matriz[x][y] = valor
    #Board.print_tablero()
    
    rounds += 1
    ronda_t = f"Ronda {rounds}"
    #print(ronda_t)
    ronda.config(text=ronda_t)
    #ronda.place(x=160,y=435)
    valor = dado()
    t = f"Dado: {valor}"
    el_dado.config(text= t)
    if rounds == 26:
        ronda.config(text="")
        el_dado.config(text="")
        puntos_t = Board.contar_puntos()
        line = ""
        for lines in Board.msj:
            line += lines + "\n"
        tkinter.messagebox.showinfo("Game Over", f"{line} Puntaje final: {puntos_t}\nPulse Restart para volver a jugar")
  
    
def restartGame():
    global gameover, rounds, el_dado, ronda_t, Board
    Board.gen_tablero()
    rounds = 1        
    
    ronda_t = f"Ronda {rounds}"
    ronda.config(text=ronda_t)
    valor = dado()
    t = f"Dado: {valor}"
    el_dado.config(text= t)
    prepareWindow()
    prepareGame()

def prepareGame():
    global rows, cols,  field
    field = []
    for x in range(0, rows):
        field.append([])
        for y in range(0, cols):
            #add button and init value for game
            field[x].append(0)
rounds = 1
ronda_t = f"Ronda {rounds}"
ronda = tkinter.Label(window, text= ronda_t, fg='black', font=("Courier", 20, "bold"), justify= LEFT)
ronda.pack()
ronda.place(x=160,y=435)           
valor = dado()
el_dado = tkinter.Label(window, text= f"Dado: {valor}", fg='black', font=("Courier", 20, "bold"), justify= LEFT)
el_dado.place(x=160,y=385)
Board = Tablero("P1")
Board.gen_tablero()

prepareWindow()
prepareGame()

#Board.print_tablero()
window.mainloop()
