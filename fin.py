import math
import time
import turtle

W, H = 900, 600
BG, TXT = "#0b1020", "#f5f5f5"

screen = turtle.Screen()
screen.setup(W, H)
screen.bgcolor(BG)
screen.title("Merci de votre attention !")
screen.tracer(0)


def make_pen(color=TXT, size=2):
    t = turtle.Turtle(visible=False)
    t.speed(0)
    t.color(color)
    t.pensize(size)
    t.penup()
    return t


def goto(t, x, y):
    t.penup()
    t.goto(x, y)
    t.pendown()


# ---------- Texte tapé lettre par lettre ----------
def type_text(text, x, y, font, color=TXT, delay=0.06):
    t = make_pen(color)
    for i in range(len(text) + 1):
        t.clear()
        t.goto(x, y)
        t.write(text[:i], align="left", font=font)
        screen.update()
        time.sleep(delay)
    return t


# ---------- Atome (modèle de Bohr) ----------
atom = make_pen("#4da6ff", 2)
ORBITS = [(0, 1.0, 0.0), (60, 1.4, 2.1), (120, 1.8, 4.2)]  # angle, vitesse, phase
A, B = 150, 55
CX, CY = 0, -50


def ellipse_point(a, b, tilt, u):
    x, y = a * math.cos(u), b * math.sin(u)
    r = math.radians(tilt)
    return CX + x * math.cos(r) - y * math.sin(r), CY + x * math.sin(r) + y * math.cos(r)


def draw_atom(t):
    atom.clear()
    atom.color("#4da6ff")
    for tilt, _, _ in ORBITS:
        first = True
        for k in range(61):
            p = ellipse_point(A, B, tilt, 2 * math.pi * k / 60)
            if first:
                goto(atom, *p)
                first = False
            else:
                atom.goto(p)
        atom.penup()
    # noyau (protons rouges / neutrons gris)
    for i, c in enumerate(["#ff4d4d", "#bbbbbb", "#ff4d4d", "#bbbbbb", "#ff4d4d", "#bbbbbb"]):
        ang = i * math.pi / 3
        atom.goto(CX + 7 * math.cos(ang), CY + 7 * math.sin(ang))
        atom.dot(14, c)
    # électrons
    for tilt, speed, phase in ORBITS:
        atom.goto(*ellipse_point(A, B, tilt, speed * t + phase))
        atom.dot(12, "#00e5ff")


# ---------- Programme ----------
type_text("Merci de votre attention !", -250, 200, ("Arial", 32, "bold"))
fin = make_pen("#ffd166")

start = time.time()
running = True


def frame():
    if not running:
        return
    t = time.time() - start
    draw_atom(t)
    # "FIN" qui pulse
    fin.clear()
    size = int(40 + 6 * math.sin(t * 3))
    fin.goto(0, 120 - size // 2)
    fin.write("FIN", align="center", font=("Arial", size, "bold"))
    screen.update()
    screen.ontimer(frame, 30)


def stop():
    global running
    running = False
    screen.bye()


screen._root.protocol("WM_DELETE_WINDOW", stop)
frame()
screen.mainloop()