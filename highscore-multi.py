# basado en https://codereview.stackexchange.com/questions/191550/minesweeper-in-python-tkinter

# hecho por jdelvalle2002
import tkinter, configparser, os, random, tkinter.messagebox, tkinter.simpledialog, webbrowser, linecache

#estilo = None
valor = None
window = tkinter.Tk()
window.iconbitmap('icon.ico')
window.resizable(0,0)
inicio = tkinter.Frame(window, bd=25)
inicio.config(bg="lightblue") 
ancho = 440
alto = 500
window.geometry(f"{ancho}x{alto}")
window.title("Highscore - by jdelvalle2002")

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

def prepareWindow(estilo, t):
    global rows, cols, buttons, classicPlay, multiPlay, start
    res = tkinter.Button(window, text="Restart", command=restartGame).grid(row=0, column=0, columnspan=cols, sticky=tkinter.N+tkinter.W+tkinter.S+tkinter.E)
    hel = tkinter.Button(window, text="Help", command=help_button).grid(row=6, column=0, columnspan=cols, sticky=tkinter.N+tkinter.W+tkinter.S+tkinter.E)
    
    
    menu = tkinter.Button(window, text="Menu", command= gomenu).grid(row=7, column=0, columnspan=cols, sticky=tkinter.N+tkinter.W+tkinter.S+tkinter.E)
    buttons = []
    
    t.append(res)
    t.append(menu)
    t.append(hel)
    for x in range(0, rows):
        buttons.append([])
        for y in range(0, cols):
            if x==y or 4-x == y:
                b = tkinter.Button(window, bg= "cyan", text="-", font="Courier 16 bold", width=6, height=2, command=lambda estilo=estilo, x=x,y=y: clickOn(x,y,estilo))
            else:
                b = tkinter.Button(window, text="-", font="Courier 16 bold", width=6, height=2, command=lambda estilo=estilo,x=x,y=y: clickOn(x,y,estilo))
            #b.bind("<Button-3>", lambda e, x=x, y=y:onRightClick(x, y))
            b.grid(row=x+1, column=y, sticky=tkinter.N+tkinter.W+tkinter.S+tkinter.E)
            buttons[x].append(b)
    

def help_button():
    webbrowser.open("https://highscore-on-python.netlify.app/")
def clickOn(x,y, estilo):
    global rounds, buttons, valor, Board, ronda, dices, el_dado
    print(rounds)
    print(estilo)
    if estilo == "multi":
        valor = dices[rounds]
        buttons[x][y]["text"] = str(valor)
        Board.matriz[x][y] = valor
        buttons[x][y]['state'] = 'disabled'
        buttons[x][y].config(relief=tkinter.SUNKEN)
    if estilo == "classic":
        #valor = dado()
        buttons[x][y]["text"] = str(valor)
        Board.matriz[x][y] = valor
        buttons[x][y]['state'] = 'disabled'
        buttons[x][y].config(relief=tkinter.SUNKEN)
    rounds += 1
    if rounds == 25:
        ronda.config(text="")
        el_dado.config(text="")
        puntos_t = Board.contar_puntos()
        line = ""
        
        for lines in Board.msj:
            line += lines + "\n"
        tkinter.messagebox.showinfo("Game Over", f"{line} Puntaje final: {puntos_t}\nPulse Restart para volver a jugar")
    else:
        ronda_t = f"Ronda {rounds+1}"
    
        ronda.config(text=ronda_t)
        
        if estilo == "multi":
            valor = dices[rounds]
        elif estilo == "classic":
            valor = dado() 
        t = f"Dado: {valor}"
        el_dado.config(text= t)

    
def restartGame():
    global rounds, el_dado, ronda_t, Board, dices, el_dado, window, prepareWindow, estilo, valor
    Board.gen_tablero()
    rounds = 0
    valor_n = valor
    if estilo == "multi":
        valor = dices[rounds]
        t = f"Dado: {valor}"
        el_dado.config(text= t)
    elif estilo == "classic":
        valor = dado()
        t = f"Dado: {valor}"
        el_dado.config(text= t)
    ronda_t = f"Ronda {rounds+1}"
    ronda.config(text=ronda_t)
    
    estilo2 = estilo
    print(estilo2)
    prepareWindow(estilo2, things)



def multiPlay():
    global codigo, start, multi, valor, ronda, rounds, ronda_t, Board, codigo, prepareGame, prepareWindow, window, estilo, dices
    multi.destroy()
    classic.destroy()
    window.title(f"Highscore: Multiplayer - by jdelvalle2002")
    juegue = False
    estilo = "multi"
    def enter_code():
        global start, valor, dices
        obtener.destroy()
        ingresar.destroy()
        Code_e = tkinter.Entry(window)
        def g():
            def keep_going(c):
                global start, valor, dices
                estilo = "multi"
                window.title(f"Highscore: Multiplayer - by jdelvalle2002")
                a = linecache.getline("dados.txt", c)
                print("linea: ", a)
                a = a.split("-")
                el_codigo = a[0]
                dices = a[1]
                dices = dices.strip().split(";")
                dices = list(map(int, dices))
                codigo = tkinter.Label(window, text= f"Código: #{el_codigo}", fg='black', font=("Courier", 10, "bold"))
                codigo.place(x=165,y=470)
                codigo.config(text=f"Código: #{el_codigo}")
                start(estilo)
            el_codigo = int(Code_e.get())
            print("input", el_codigo)
            ing.destroy()
            intro.destroy()
            ing2.destroy()
            Code_e.destroy()
            keep_going(el_codigo)
        intro = tkinter.Button(text="Enter", bg = "cyan", font=("Courier", 10, "bold"), width= 5 , height=1, command=g)
        ing = tkinter.Label(window, text="Ingresa el código para jugar una",fg='black', font=("Courier", 12, "bold"))
        ing2 = tkinter.Label(window, text="partida multijugador (entre 1 y 5000)",fg='black', font=("Courier", 12, "bold"))
        ing.pack(pady=100)
        ing2.pack(pady=10)
        Code_e.pack(pady=10)
        intro.pack()

 
    def get_code():
        global start, valor, estilo, dices
        obtener.destroy()
        ingresar.destroy()
        window.title(f"Highscore: Multiplayer - by jdelvalle2002")
        l = random.randint(1,5000)
        a = linecache.getline("dados.txt", l)
        a = a.split("-")
        el_codigo = a[0]
        dices = a[1]
        dices = dices.strip().split(";")
        dices = list(map(int, dices))
        codigo = tkinter.Label(window, text= f"Código: #{el_codigo}", fg='black', font=("Courier", 10, "bold"))
        codigo.place(x=165,y=470)
        codigo.config(text=f"Código: #{l}")
        start(estilo)
    
    obtener = tkinter.Button(text="Obtener código", bg = "cyan", font=("Courier", 20, "bold"), width= 15 , height=2, command=get_code)
    obtener.pack(padx=60, pady=70)
    ingresar = tkinter.Button(text="Ingresar código", bg = "cyan", font=("Courier", 20, "bold"), width= 15 , height=2, command=enter_code)
    ingresar.pack(padx=60, pady=70)
    
    
  

def classicPlay():
    global codigo, start, multi, ronda, rounds, ronda_t, Board, codigo, prepareGame, prepareWindow, estilo
    multi.destroy()
    classic.destroy()
    estilo = "classic"
    window.title("Highscore: One Player - by jdelvalle2002")
    start(estilo)

def start(estilo):
    global rounds, ronda_t, Board, codigo, prepareGame, prepareWindow, ronda, el_dado, dado, valor, dices
    valor = None
    rounds = 0
    ronda_t = f"Ronda {rounds+1}"
    ronda = tkinter.Label(window, text= ronda_t, fg='black', font=("Courier", 20, "bold"))
    #ronda.pack()
    ronda.place(x=160,y=430)
    if estilo == "multi":
        valor = dices[rounds]
    elif estilo == "classic":
        valor = dado()    
    el_dado = tkinter.Label(window, text= f"Dado: {valor}", fg='black', font=("Courier", 20, "bold"))
    el_dado.place(x=160,y=395)
    Board = Tablero("P1")
    Board.gen_tablero()
    prepareWindow(estilo, things)


def gomenu():
    global things, buttons
    for i in range(5):
        for j in range(5):
            buttons[i][j].grid_remove()
            #print(buttons)
    for i in range(3):
        print(things[i])
        things[i].grid_remove()
    '''res.grid_remove()
    hel.grid_remove()
    menu.gridremove()
    for i in range(5):
        for j in range(5):
            buttons[i][j].grid_remove()
            print(buttons)'''    
    classic = tkinter.Button(text="One Player", bg = "cyan", font=("Courier", 20, "bold"), width= 15 , height=2, command=classicPlay)
    classic.pack(padx=60, pady=70)
    multi = tkinter.Button(text="Multiplayer", bg = "cyan", font=("Courier", 20, "bold"), width= 15 , height=2, command=multiPlay)
    multi.pack(padx=60, pady=70)


classic = tkinter.Button(text="One Player", bg = "cyan", font=("Courier", 20, "bold"), width= 15 , height=2, command=classicPlay)
classic.pack(padx=60, pady=70)

multi = tkinter.Button(text="Multiplayer", bg = "cyan", font=("Courier", 20, "bold"), width= 15 , height=2, command=multiPlay)

multi.pack(padx=60, pady=70)


#prepareWindow()
#prepareGame()


window.mainloop()
