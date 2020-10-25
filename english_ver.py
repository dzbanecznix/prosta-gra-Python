from time import sleep
import os
import msvcrt
import random

clear = lambda: os.system('cls')

try:
    dane = open("C:\\ASCIIMinoritySigns\\highscore.txt", "r").read()
    ustawienia = open("C:\\ASCIIMinoritySigns\\ustawienia.txt", "r").readlines()
except FileNotFoundError:
    os.chdir("C:\\")
    os.mkdir("ASCIIMinoritySigns")
    f = open("C:\\ASCIIMinoritySigns\\highscore.txt", "w")
    f.write("0")
    f = open("C:\\ASCIIMinoritySigns\\ustawienia.txt", "w")
    f.write('height of map: 5 \nspawn period: 3\n# signs per period: 2\nplayer sign: "O"\nempty sign: "."')          
    f.close()
    dane = open("C:\\ASCIIMinoritySigns\\highscore.txt", "r").read()
    ustawienia = open("C:\\ASCIIMinoritySigns\\ustawienia.txt", "r").readlines()
highscore = int(dane)
sps = {}
pos = {}
names = []
background = ustawienia[4][13:14]
mapx = 40
mapy = int(ustawienia[0][15:])
fps = 25
easyness = int(ustawienia[1][14:])
num = mapx//easyness
naraz = int(ustawienia[2][20:])

def shs(ile):
    with open("C:\\ASCIIMinoritySigns\\highscore.txt", "w") as f:
        print(str(ile), file = f)
    highscore = ile
def st(x, y):
    return(str(x)+"_"+str(y))
def ds(st):
    mli = [0]
    for zn in st:
        if zn == "_":
            mli.append(0)
        else:
            mli[len(mli)-1] *= 10
            mli[len(mli)-1] += int(zn)
    return(mli)
def ns(name, sym, x, y):
    sps[st(x, y)] = sym
    pos[name] = st(x, y)
    names.append(name)
def ms(name, dx, dy):
    sym = sps[pos[name]]
    sps[pos[name]] = background
    intpos = ds(pos[name])
    intpos[0] += dx
    intpos[1] += dy
    if intpos[0] >= 0 and intpos[0] <= mapx - 1 and intpos[1] >= 0 and intpos[1] <= mapy - 1:
        pos[name] = st(intpos[0], intpos[1])
    else:
        intpos[0] -= dx
        intpos[1] -= dy
        pos[name] = st(intpos[0], intpos[1])
    sps[pos[name]] = sym
def gs(name, newx, newy):
    sym = sps[pos[name]]
    sps[pos[name]] = background
    pos[name] = st(newx, newy)
    sps[pos[name]] = sym
def zaj(x, y):
    s = st(x, y)
    for n in names:
        if pos[n] == s:
            return(sps[s])
    return(background)
def domap():
    clear()
    mapka = ""
    for y in range(mapy):
        for x in range(mapx):
            mapka += zaj(x, y)
        mapka += "\n"
    print(mapka)
def czekajnaklawisz():
        while not msvcrt.kbhit():
            sleep(0)
        key = msvcrt.getch()
        if key == b'r':
            run()
        elif key != b'q':
            czekajnaklawisz()    
def run():
    global sps, pos, names
    sps = {} #sprites
    pos = {}
    names = []
    klatki = 0
    sprites = 0
    ns("steve", ustawienia[3][14:15], 3, mapy//2)
    for i in range(num * naraz):
        ns(str(i), "<", 39 + i, mapy + 1)
    ualive = True
    while ualive:
        klatki += 1
        if msvcrt.kbhit():
            key = msvcrt.getch()
            if(key == b's' or key == b'P'):
                ms("steve", 0, 1)
            if(key == b'w' or key == b'H'):
                ms("steve", 0, -1)
        for i in range(num * naraz):
            if(ds(pos[str(i)])[0] > 1):
                ms(str(i), -1, 0)
            if(pos["steve"] == pos[str(i)]):
                ualive = False
        if(klatki % easyness == 0):
            rand = [-1]
            i = 0
            while i < naraz:
                i += 1
                r = -1
                while r in rand:
                    r = random.randint(0, mapy - 1)
                rand.append(r)
                gs(str(sprites), 39, r)
                sprites = (sprites + 1)%(num*naraz)
        sleep(1/fps)
        domap()
    wynik = klatki // easyness
    if wynik > highscore:
        shs(wynik)
    print("GAME OVER! score:", wynik, "high score:", highscore, )
    sleep(0.5)
    print('r - restart\nq - quit')
    czekajnaklawisz()
run()    
