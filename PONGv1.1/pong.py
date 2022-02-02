import turtle
from time import sleep
import winsound
import sys

def Window(wn): #funkcja tworząca ekran
    wn.title("Pong by Matthew")
    wn.bgcolor("black")
    wn.setup(width=800, height=600)
    wn.tracer(0)

class Start(): #klasa wyświetlająca menu po włączeniu gry
    def __init__(self):
        self.is_start = True
        self.s = turtle.Turtle()
        self.s.speed(0)
        self.s.color("white")
        self.s.penup()
        self.s.hideturtle()
        self.s.goto(0,0)
        self.s.write("START", align="center", font=("Courier", 60, "bold"))
        self.s.goto(0,-250)
        self.s.write("KEYBINDING:\n w/s and Up/Down -> moving paddles\n p -> PAUSE\n q -> exit the game\n z -> speed up the ball\n x -> slow down the ball\n\n PRESS SPACEBAR TO START", align="center", font=("Courier", 18, "bold"))

    def off_start(self):
        if self.is_start == True:
           self.is_start = False
           self.s.clear()

class Scoreboard(): #klasa odpowiedzialna za wyświetlanie punktacji
    def __init__(self):
        self.pen = turtle.Turtle()
        self.pen.speed(0)
        self.pen.color("white")
        self.pen.penup()
        self.pen.hideturtle()
        self.pen.goto(0,220)
        self.pen.write("0        0", align="center", font=("Courier", 48, "bold"))

    def Points(self, score_a, score_b):
        self.pen.clear()
        self.pen.write("{}        {}".format(score_a, score_b), align="center", font=("Courier", 48, "bold"))

class Pause(): #klasa odpowiedzialna za pauzę gry
    def __init__(self):
        self.is_paused = False
        self.p = turtle.Turtle()
        self.p.speed(0)
        self.p.color("white")
        self.p.penup()
        self.p.hideturtle()

    def toggle_pause(self):
        if self.is_paused == True:
            self.is_paused = False
            self.p.clear()
        else:
            self.is_paused = True
            self.p.goto(0,0)
            self.p.write("PAUSE", align="center", font=("Courier", 60, "bold"))
            self.p.goto(0,-250)
            self.p.write("KEYBINDING:\n w/s and Up/Down -> moving paddles\n p -> PAUSE\n q -> exit the game\n z -> speed up the ball\n x -> slow down the ball\n\n PRESS SPACEBAR TO START", align="center", font=("Courier", 18, "bold"))

class Quit():
    def __init__(self):
        self.running = True

    def omaewamoushindeiru(self):
        self.running = False

class Item(): #klasa zawierająca konstruktor, z której dziedziczą klasy paletka i piłka
    def __init__(self, OX, OY):
        self.item = turtle.Turtle()
        self.item.speed(0)
        self.item.shape("square")
        self.item.color("white")
        self.item.penup()
        self.item.goto(OX,OY)

class PongPaddle(Item): #klasa tworząca paletkę a oraz paletkę b
    def __init__(self, OX, OY, m):
        super().__init__(OX, OY)
        self.item.shapesize(stretch_wid = 5, stretch_len = 1)
        self.item.m = m

    def paddle_up(self):
        y = self.item.ycor()
        y += self.item.m
        if y < 260:
            self.item.sety(y)

    def paddle_down(self):
        y = self.item.ycor()
        y -= self.item.m
        if y > -260:
            self.item.sety(y)

    def y(self): #metoda zwraca ycor -> rozwiązanie problemu z pobieraniem wartości z obiektu (nie chciało się pobierać)
        return self.item.ycor()
     
class PongBall(Item):
    def __init__(self, OX, OY, a, b, pen):
        super().__init__(OX, OY)
        self.item.speed = 3
        self.item.is_faster = False
        self.item.is_slower = False
        self.item.dx = self.item.speed
        self.item.dy = -1* self.item.speed
        self.item.a = a
        self.item.b = b
        self.pen = pen
        self.score_a = 0
        self.score_b = 0

    def faster(self):
        if self.item.is_faster == True:
            self.item.is_faster = False
            if self.item.speed < 7:
                self.item.speed += 1
            self.item.dx = self.item.speed
            self.item.dy = self.item.speed
        else:
            self.item.is_faster = True

    def slower(self):
        if self.item.is_slower == True:
            self.item.is_slower = False
            if self.item.speed > 1:
                self.item.speed -= 1
            self.item.dx = self.item.speed
            self.item.dy = self.item.speed
        else:
            self.item.is_slower = True

    def Move(self): #ruch piłki
        self.item.setx(self.item.xcor() + self.item.dx)
        self.item.sety(self.item.ycor() + self.item.dy)

    def Megamind(self): #obliczenia dotyczące kolizji piłki ze ścianami i paletkami
        if self.item.ycor() > 290:
            self.item.sety(290)
            self.item.dy *= -1
            winsound.PlaySound("wall.wav", winsound.SND_ASYNC)

        if self.item.ycor() < -280:
            self.item.sety(-280)
            self.item.dy *= -1
            winsound.PlaySound("wall.wav", winsound.SND_ASYNC)

        if self.item.xcor() > 390:
            self.item.goto(0,0)
            self.item.dx *= -1
            self.score_a += 1
            self.pen.Points(self.score_a, self.score_b)
            winsound.PlaySound("score.wav", winsound.SND_ASYNC)

        if self.item.xcor() < -390:
            self.item.goto(0,0)
            self.item.dx *= -1
            self.score_b += 1
            self.pen.Points(self.score_a, self.score_b)
            winsound.PlaySound("score.wav", winsound.SND_ASYNC)

        if (self.item.xcor() > 330 and self.item.xcor() < 340) and (self.item.ycor() < self.item.b.y() + 60 and self.item.ycor() > self.item.b.y() - 60):
            self.item.setx(330)
            self.item.dx *= -1
            winsound.PlaySound("hit.wav", winsound.SND_ASYNC)

        if (self.item.xcor() < -330 and self.item.xcor() > -340) and (self.item.ycor() < self.item.a.y() + 60 and self.item.ycor() > self.item.a.y() - 60):
            self.item.setx(-330)
            self.item.dx *= -1
            winsound.PlaySound("hit.wav", winsound.SND_ASYNC)

def bind(wn, a, b, pauza, start, quit, ball): #przypisanie i nasłuchiwanie klawiszy
    wn.listen()
    wn.onkeypress(a.paddle_up, "w")
    wn.onkeypress(a.paddle_down, "s")
    wn.onkeypress(b.paddle_up, "Up")
    wn.onkeypress(b.paddle_down, "Down")
    wn.onkeypress(pauza.toggle_pause, "p")
    wn.onkeypress(start.off_start, "space")
    wn.onkeypress(quit.omaewamoushindeiru, "q")
    wn.onkeypress(ball.faster, "z")
    wn.onkeypress(ball.slower, "x")

def PongSilnik(window):
    paddle_a = PongPaddle(-350,0,50)
    paddle_b = PongPaddle(350,0,50)
    pen = Scoreboard()
    ball = PongBall(0,0, paddle_a, paddle_b, pen)
    pauza = Pause()
    start = Start()
    quit = Quit()

    bind(window, paddle_a, paddle_b, pauza, start, quit, ball)

    while quit.running:
        if not start.is_start:
            if not pauza.is_paused:
                window.update()
                sleep(0.01)
                paddle_a.item.m = 50
                paddle_b.item.m = 50
                ball.Move()
                ball.Megamind()
            else:
                paddle_a.item.m = 0
                paddle_b.item.m = 0
                window.update()
        else:
            paddle_a.item.m = 0
            paddle_b.item.m = 0
            window.update()

def Main():
    window = turtle.Screen()
    Window(window)
    PongSilnik(window)
    window.bye()

Main()