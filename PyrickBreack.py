import turtle

# Screen setup
wn = turtle.Screen()
wn.title("Ball Buster")
wn.bgcolor("black")
wn.setup(width=600, height=600)
wn.tracer(0)  # Manually update the screen for better control over animations

# Paddle class definition
class Paddle(turtle.Turtle):
    def __init__(self):
        super().__init__(shape="square")
        self.color("white")
        self.shapesize(stretch_wid=1, stretch_len=6)
        self.penup()
        self.goto(0, -250)
        self.speed("fastest")  # Set the turtle speed to the maximum possible
        self.moving_left = False
        self.moving_right = False

    def move(self):
        if self.moving_left:
            x = self.xcor() - 3
            if x < -250:
                x = -250
            self.setx(x)
        if self.moving_right:
            x = self.xcor() + 3
            if x > 250:
                x = 250
            self.setx(x)

    def go_left(self):
        self.moving_left = True

    def stop_left(self):
        self.moving_left = False

    def go_right(self):
        self.moving_right = True

    def stop_right(self):
        self.moving_right = False

# Ball class definition
class Ball(turtle.Turtle):
    def __init__(self, clear_message_callback):
        super().__init__(shape="circle")
        self.color("red")
        self.penup()
        self.goto(0, -100)
        self.dx = 0  # Initialize with no movement
        self.dy = 0  # Initialize with no movement
        self.moving = False  # Track whether the ball is moving
        self.clear_message = clear_message_callback  # Method to clear the message

    def move(self):
        if self.moving:
            self.setx(self.xcor() + self.dx)
            self.sety(self.ycor() + self.dy)

            # Bounce off walls
            if self.xcor() > 290 or self.xcor() < -290:
                self.dx *= -1
            if self.ycor() > 290:
                self.dy *= -1

    def launch_ball(self):
        if not self.moving:
            self.dx = 1  # Set initial horizontal speed
            self.dy = 1  # Set initial vertical speed
            self.moving = True
            self.clear_message()  # Clear the message when the ball is launched

# Brick class definition
class Brick(turtle.Turtle):
    def __init__(self, x, y, color):
        super().__init__()
        self.penup()
        self.shape("square")
        self.shapesize(stretch_wid=1, stretch_len=3)
        self.color("white", color)  # Outline color white, fill color as specified
        self.goto(x, y)

# Game management class
class BrickBreaker:
    def __init__(self):
        self.paddle = Paddle()
        self.ball = Ball(self.clear_message)  # Pass the clear_message method
        self.bricks = []
        self.create_bricks()
        self.message = turtle.Turtle(visible=False)
        self.message.color("white")
        self.message.penup()
        self.message.goto(0, 250)  # Position message well above the highest row of bricks
        self.display_message("Press Space to Bust Some Balls", True)

    def create_bricks(self):
        colors = ["red", "yellow", "green", "blue", "orange"]
        start_x = -280
        for y in range(50, 250, 21):
            color = colors[(y // 21) % len(colors)]
            for x in range(start_x, 281, 61):
                brick = Brick(x, y, color)
                self.bricks.append(brick)

    def display_message(self, msg, large=False):
        self.message.clear()
        font = ("Arial", 24, "bold") if large else ("Arial", 14, "normal")
        self.message.write(msg, align="center", font=font)

    def clear_message(self):
        self.message.clear()

    def run(self):
        while True:
            wn.update()
            self.paddle.move()
            self.ball.move()

            # Paddle collision
            if self.ball.ycor() < -240 and self.ball.ycor() > -250 and self.paddle.xcor() - 60 < self.ball.xcor() < self.paddle.xcor() + 60:
                self.ball.sety(-240)  # Position the ball just above the paddle
                self.ball.dy *= -1

            # Brick collision
            for brick in self.bricks:
                if brick.distance(self.ball) < 20:
                    self.ball.dy *= -1
                    brick.hideturtle()  # Hide the brick
                    self.bricks.remove(brick)
                    break  # Exit the loop to avoid modifying the list during iteration

            # Bottom wall collision
            if self.ball.ycor() < -290:
                self.ball.goto(0, -100)  # Reset ball position
                self.ball.dx = 0
                self.ball.dy = 0
                self.ball.moving = False
                self.display_message("Press Space to Bust Some Balls", True)

# Keyboard bindings and event handling
game = BrickBreaker()
wn.listen()
wn.onkeypress(game.paddle.go_left, "Left")
wn.onkeyrelease(game.paddle.stop_left, "Left")
wn.onkeypress(game.paddle.go_right, "Right")
wn.onkeyrelease(game.paddle.stop_right, "Right")
wn.onkeypress(game.ball.launch_ball, "space")
game.run()
wn.mainloop()
