from abc import ABC, abstractmethod
import turtle


class Screen:
    def __init__(self, name, width, height, color, speed=10) -> None:
        
        self.creation = turtle.Screen()
        self.creation.title(name)
        self.creation.bgcolor(color)
        self.creation.setup(width=width, height=height)

    def mainloop(self) -> None:
        self.creation.mainloop()


class Tortoise(ABC):
    def __init__(self, player_name):
        self.player_name = player_name
        self.creation = turtle.Turtle()

    @abstractmethod
    def shape_fillup(self, *args):
        pass

class BallMovement(ABC):
    @abstractmethod
    def start_movement(self) -> None: ...
    @abstractmethod
    def check_out_of_bounds(self) -> None: ...
    @abstractmethod
    def check_wall_rebound(self) -> None: ...

class BallRebound(ABC):
    @abstractmethod
    def rebound(self) -> None: ...

class WallRebound(BallRebound):

    def upper_wall_rebound(self) -> None: ...
    def lower_wall_rebound(self) -> None: ...

class PlayerRebound(BallRebound):
    
    def left_player_rebound(self) -> None: ...
    def right_player_rebound(self) -> None: ...

class PlayerMovement(ABC):
    @abstractmethod
    def mov_up(self) -> None: ...
    @abstractmethod
    def mov_down(self) -> None: ...


class Jugador(Tortoise, PlayerMovement):
    def __init__(self, player_name):
        super().__init__(player_name)

    def shape_fillup(self, color: str, speed: int = 4):
        self.creation.shape('square')
        #Para que la pala SEA la tortuga, necesito hacer un shapesize. Si hago el pendown/penup
        #lo que hace es dejar rastro del movimiento, pero no lo convierte en el objeto
        self.creation.shapesize(stretch_wid=5, stretch_len=1.2)
        self.creation.pencolor(color)
        self.creation.fillcolor(color)
        self.creation.speed(speed)

    def player_placement(self, position: str = None) -> None:

        if position.lower()=='left':
            self.creation.penup()
            self.creation.goto(-320, 0)
            self.creation.pendown()

        if position.lower()=='right':
            self.creation.penup()
            self.creation.goto(310, 0)
            self.creation.pendown()

    def mov_up(self):
        self.creation.penup()
        y=self.creation.ycor()
        self.creation.sety(y+5)
        if y > 200:
            self.creation.sety(200)
        self.creation.pendown()

    def mov_down(self):
        self.creation.penup()
        y=self.creation.ycor()
        self.creation.sety(y-5)
        if y < -180:
            self.creation.sety(-200)
        self.creation.pendown()

class Ball(Tortoise, BallMovement):
    def __init__(self, player_name):
        super().__init__(player_name)
        self.speed_x=6
        self.speed_y=6

    def shape_fillup(self, shape: str , color: str, pensize: int, speed: int =None):
        self.creation.shape(shape) # "arrow", "classic", "turtle", "circle", "square", "triangle"
        self.creation.color(color)
        self.creation.pensize(pensize)
        self.creation.speed(speed)
        #falta la parte de rellenar la forma y crear una clase para jugadores con un fillup de rectángulos
    
    def start_movement(self):
        self.creation.penup()
        self.creation.setheading(0)

    def goto_centre(self):
        self.creation.goto(0,0)

    def move(self):
        x = self.creation.xcor() + self.speed_x
        y = self.creation.ycor() + self.speed_y
        self.creation.setpos(x,y)

    def check_left_rebound(self, jugador: Jugador):
        x = self.creation.xcor()
        y = self.creation.ycor()
        player_y = jugador.creation.ycor()
        paddle_bottom= player_y - 50
        paddle_top = player_y + 50
        if x <= -300 and paddle_top >= y >= paddle_bottom and self.speed_x < 0:
            self.speed_x *= -1

    def check_right_rebound(self, jugador: Jugador):
        x = self.creation.xcor()
        y = self.creation.ycor()
        player_y = jugador.creation.ycor()
        paddle_bottom= player_y - 50
        paddle_top = player_y + 50
        if x > 300 and paddle_top >= y >= paddle_bottom and self.speed_x > 0:
            self.speed_x *= -1

    def check_wall_rebound(self):
        y=self.creation.ycor()
        if 220 < y or -220 > y:
            self.speed_y *= -1

    def check_out_of_bounds(self):
        x=self.creation.xcor()
        if -310 > x or x > 310:
            self.goto_centre()
            self.speed_x *= -1





        



jugador1 = Jugador('jugador1')
jugador1.shape_fillup("#E90A0A")
jugador1.player_placement('right')

jugador2 = Jugador('jugador2')
jugador2.shape_fillup("#1D0AE9")
jugador2.player_placement('left')

ball = Ball('PingPong Ball')
ball.shape_fillup('circle',"#15E90A", 2, 7)

pantalla =Screen('mi_pantalla', 640, 480, "#F7F4EC")
pantalla.creation.listen()
pantalla.creation.onkey(jugador2.mov_up, "w")
pantalla.creation.onkey(jugador2.mov_down, "s")
pantalla.creation.onkey(jugador1.mov_up, "Up")
pantalla.creation.onkey(jugador1.mov_down, "Down")

def game_loop():
    ball.start_movement()
    ball.move()
    ball.check_left_rebound(jugador2)
    ball.check_right_rebound(jugador1)
    ball.check_wall_rebound()
    ball.check_out_of_bounds()
    pantalla.creation.ontimer(game_loop, 16)

game_loop()
pantalla.mainloop()






