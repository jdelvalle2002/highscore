# basado en https://codereview.stackexchange.com/questions/191550/minesweeper-in-python-tkinter

# hecho por jdelvalle2002
from tkinter import *
import configparser, os, random, tkinter.messagebox, tkinter.simpledialog, webbrowser, linecache



def generar(alto, ancho, titulo):
    window = tkinter.Tk()
    window.title(titulo)
    window.geometry(f"{ancho}x{alto}")
    return window
alto = 560
ancho = 470    
main = generar(alto,ancho,"Highscore: Menu - by jdelvalle2002")    
# segunda = generar_ventana(600,600,"Highscore - by jdelvalle2002")

padX = 110
padY = 120
def help_button():
    webbrowser.open("https://highscore-on-python.netlify.app/")
def dado():
    a = random.randint(1,6)
    b = random.randint(1,6)
    valor = a+b
    return valor
#prepare default values
things = []
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

##########
def clickOn(x,y,app):
        
    if app.estilo == "multi":
        app.valor = app.dices[app.rounds]
        app.buttons[x][y]["text"] = str(app.valor)
        Board.matriz[x][y] = app.valor
        app.buttons[x][y]['state'] = 'disabled'
        app.buttons[x][y].config(relief=tkinter.SUNKEN)
    if app.estilo == "classic":
        #valor = dado()
        app.buttons[x][y]["text"] = str(app.valor)
        Board.matriz[x][y] = app.valor
        app.buttons[x][y]['state'] = 'disabled'
        app.buttons[x][y].config(relief=tkinter.SUNKEN)
    app.rounds += 1
    if app.rounds == 25:
        app.ronda.config(text="")
        app.el_dado.config(text="")
        puntos_t = Board.contar_puntos()
        line = ""
        for lines in Board.msj:
            line += lines + "\n"
        if app.estilo == "classic":
            tkinter.messagebox.showinfo("Game Over", f"{line} Puntaje final: {puntos_t}\nPulse Restart para volver a jugar")
        elif app.estilo == "multi":
            app.res["state"]= "disabled"
            app.res.config(relief=tkinter.SUNKEN) 
            tkinter.messagebox.showinfo("Game Over", f"{line} Puntaje final: {puntos_t}\nVuelve a insertar un código para jugar denuevo")   
    else:
        ronda_t = f"Ronda {app.rounds+1}"
        #print(ronda_t)
        app.ronda.config(text=ronda_t)
        
        if app.estilo == "multi":
            app.valor = app.dices[app.rounds]
        elif app.estilo == "classic":
            app.valor = dado()
            #print(app.valor) 
        t = f"Dado: {app.valor}"
        #print(t, "click")
        app.el_dado.config(text= t)


class Juego():
    def __init__(self, main) -> None:
        self.main = main
        self.main.title("Highscore - by jdelvalle2002")
        self.one = Button(self.main, text="One Player", bg = "cyan", font=("Courier", 20, "bold"), width= 15 , height=2, command=self.classicPlay)
        self.multi = Button(self.main, text="Multiplayer", bg = "cyan", font=("Courier", 20, "bold"), width= 15 , height=2, command=self.multiPlay)
        self.one.grid(pady=(padY,0), padx=padX)
        self.multi.grid(pady=(padY,0), padx=padX)
        self.estilo = None
        self.rounds = 0
        self.valor = None
        self.opt = []
        self.ronda = ""
        self.buttons = []

    def gen5x5(self):
        self.buttons = []
        for x in range(0, 5):
            self.buttons.append([])
            for y in range(0, 5):
                if x==y or 4-x == y:
                    b = tkinter.Button(self.main, bg= "cyan", text="-", font="Courier 18 bold", width=6, height=2, command=lambda app=app, x=x,y=y: clickOn(x,y,app))
                else:
                    b = tkinter.Button(self.main, text="-", font="Courier 18 bold", width=6, height=2, command=lambda app=app, x=x,y=y: clickOn(x,y,app))
                b.grid(row=x+1, column=y+1, sticky=tkinter.N+tkinter.W+tkinter.S+tkinter.E)
                self.buttons[x].append(b)
    def genopt(self):
        self.rounds = 0
        #self.relleno = Label(self.main, text= "", fg='black', font=("Courier", 20, "bold"))
        #self.relleno.grid(row=0, column=1, columnspan=cols, sticky=tkinter.N+tkinter.W+tkinter.S+tkinter.E)
        self.res = Button(self.main, text="Restart", command=self.restartJuego)
        self.res.grid(row=0, column=1, columnspan=cols, sticky=tkinter.N+tkinter.W+tkinter.S+tkinter.E)
        self.hel = Button(self.main, text="Help", command=help_button)
        self.hel.grid(row=6, column=1, columnspan=cols, sticky=tkinter.N+tkinter.W+tkinter.S+tkinter.E)
        self.menu = Button(self.main, text="Menu", command= self.gomenu)
        self.menu.grid(row=7, column=1, columnspan=cols, sticky=tkinter.N+tkinter.W+tkinter.S+tkinter.E)
        self.el_dado = Label(self.main, text= f"Dado: {self.valor}", fg='black', font=("Courier", 20, "bold"))
        self.el_dado.grid(row=8, column=1, columnspan=5, sticky=tkinter.N+tkinter.W+tkinter.S+tkinter.E)
        self.ronda = Label(self.main, text= f"Ronda {self.rounds+1}", fg='black', font=("Courier", 20, "bold"))
        self.ronda.grid(row=10, column=1, columnspan=5, sticky=tkinter.N+tkinter.W+tkinter.S+tkinter.E)
        self.opt = [self.res, self.ronda, self.menu, self.hel, self.el_dado]#, self.relleno]
        if self.estilo == "multi":
            self.codigo = Label(self.main, text="", fg='black', font=("Courier", 10, "bold"))
            self.codigo.grid(row=11, column=1, columnspan=5, sticky=tkinter.N+tkinter.W+tkinter.S+tkinter.E)
            self.opt.append(self.codigo)
    def restartJuego(self):
        for i in range(5):
            for j in range(5):
                self.buttons[i][j].grid_remove()
                self.buttons[i][j].destroy()
        for opt in self.opt:
            opt.grid_remove()    
            opt.destroy()
        self.gen5x5()
        self.genopt()
        if self.estilo == "multi":
            self.codigo.config(text=f"Código: #{self.el_codigo}")

        self.rounds=0
        if self.estilo == "classic":
            self.valor = dado()
        elif self.estilo == "multi":
            self.valor = self.dices[self.rounds]    
        self.ronda.config(text=f"Ronda {self.rounds+1}")
        self.el_dado.config(text= f"Dado: {self.valor}")

    
    def classicPlay(self):
        self.main.title(f"Highscore: One Player - by jdelvalle2002")
        self.estilo = "classic"
        self.one.destroy()
        self.multi.destroy()
        self.gen5x5()
        self.genopt()
        self.valor = dado()
        self.el_dado.config(text= f"Dado: {self.valor}")
        self.rounds = 0
    def multiPlay(self):
        self.main.title(f"Highscore: Multiplayer - by jdelvalle2002")
        self.estilo = "multi"
        self.one.destroy()
        self.multi.destroy() 
        self.Code_e = Entry(self.main)
        self.rounds = 0
        def g():
            def keep_going(c):
                self.estilo = "multi"
                
                random.seed(self.el_codigo)
                self.dices = [dado() for i in range(25)]
                self.gen5x5()
                self.genopt()
                self.valor = self.dices[self.rounds]
                self.el_dado.config(text= f"Dado: {self.valor}")
                self.codigo.config(text=f"Código: #{c}")
            self.el_codigo = self.Code_e.get()
            #print("input", el_codigo)
            #self.ing.grid_remove()
            self.ing0.destroy()
            self.ing.destroy()
            #self.intro.grid_remove()
            self.intro.destroy()
            #self.ing2.grid_remove()
            self.ing2.destroy()
            #self.Code_e.grid_remove()
            self.Code_e.destroy()
            keep_going(self.el_codigo)
        self.intro = Button(self.main,text="Enter", bg = "cyan", font=("Courier", 12), width= 6 , height=1, command=g)
        self.ing = Label(self.main, text="Ingresa el código para jugar una",fg='black', font=("Courier", 14, "bold"))
        self.ing2 = Label(self.main, text="partida multijugador",fg='black', font=("Courier", 14, "bold"))
        self.ing0 = Label(self.main, text="",fg='black', font=("Courier", 14, "bold"))
        self.ing0.grid(row=0,column=1, padx=60, pady=(200,0))
        self.ing.grid(row=1, column=1, padx=55)
        self.ing2.grid(row=2, column=1)
        self.Code_e.grid(row=3, column=1, pady=10)
        self.intro.grid(row=4, column=1)
        #self.ing.columnconfigure(1,pad=70)
        
    def set_inicio(self):
        self.one = Button(self.main, text="One Player", bg = "cyan", font=("Courier", 20, "bold"), width= 15 , height=2, command=self.classicPlay)
        self.multi = Button(self.main, text="Multiplayer", bg = "cyan", font=("Courier", 20, "bold"), width= 15 , height=2, command=self.multiPlay)
        self.one.grid(pady=(padY,0), padx=padX)
        self.multi.grid(pady=(padY,0), padx=padX)
        self.ronda=0
    def gomenu(self):
        for i in range(5):
            for j in range(5):
                self.buttons[i][j].grid_remove()
                self.buttons[i][j].destroy()
        #print(len(self.opt))
        for opt in self.opt:
            opt.grid_remove()
            opt.destroy()
        self.set_inicio()    
        
        


app = Juego(main)
Board = Tablero("P1")
if __name__ == "__main__":
    app.rounds = 0
    Board.gen_tablero()
main.mainloop()