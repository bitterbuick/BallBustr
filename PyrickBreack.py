"""Simple brick-breaker style game using the turtle module."""

import turtle
import math
import time

# Constants for speed limits
MAX_BALL_SPEED = 1.5
PADDLE_SPEED = MAX_BALL_SPEED + 0.5
TARGET_FPS = 60
FRAME_TIME = 1.0 / TARGET_FPS

# Screen setup
wn = turtle.Screen()
wn.title("Ball Buster")
wn.bgcolor("black")
wn.setup(width=600, height=600)
wn.tracer(0)  # Manually update the screen for better control over animations

# Border drawing
border = turtle.Turtle(visible=False)
border.color("white")
border.penup()
border.goto(-300, 290)  # Start slightly outside the outermost bricks
border.pendown()
for _ in range(4):
    border.forward(600)
    border.right(90)
border.penup()

# Paddle class definition
class Paddle(turtle.Turtle):
    """
    Paddle class represents the player's paddle that can be moved left or right.
    """
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
        """
        Move the paddle left or right based on user input.
        """
        if self.moving_left:
            x = self.xcor() - PADDLE_SPEED
            if x < -250:
                x = -250
            self.setx(x)
        if self.moving_right:
            x = self.xcor() + PADDLE_SPEED
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
    """
    Ball class represents the ball in the game, which can move and bounce off surfaces.
    """
    def __init__(self, clear_message_callback):
        super().__init__(shape="circle")
        self.color("red")
        self.penup()
        self.goto(0, -100)
        self.dx = 0
        self.dy = 0
        self.moving = False
        self.clear_message = clear_message_callback

    def move(self):
        """
        Move the ball and handle bouncing off walls.
        """
        if self.moving:
            self.setx(self.xcor() + self.dx)
            self.sety(self.ycor() + self.dy)

            # Bounce off left and right walls
            if self.xcor() > 290 or self.xcor() < -290:
                self.dx *= -1
            # Bounce off the top wall
            if self.ycor() > 290:
                self.dy *= -1

    def launch_ball(self):
        """
        Start the ball movement with an initial velocity.
        """
        if not self.moving:
            self.dx = 1
            self.dy = 1
            self.moving = True
            self.clear_message()

    def avoid_last_brick(self, brick):
        """Continuously steer the ball away from the last brick each frame.

        Predicts where the ball will be when it reaches the brick's y-level.
        If that predicted position lands on the brick, rotates the velocity
        vector by a tiny amount until the trajectory clears the brick.
        Because it's applied gradually and stops as soon as the ball is off
        course, the deflection is imperceptible to the player.
        """
        if not self.moving or self.dy <= 0 or abs(self.dy) < 0.1:
            return
        # Only act when ball is below the brick and heading toward it
        height_diff = brick.ycor() - self.ycor()
        if height_diff <= 0 or height_diff > 150:
            return

        steps = height_diff / self.dy
        predicted_x = self.xcor() + self.dx * steps

        # Correct for wall bounces in the prediction
        for _ in range(6):
            if predicted_x > 290:
                predicted_x = 580 - predicted_x
            elif predicted_x < -290:
                predicted_x = -580 - predicted_x
            else:
                break

        # Brick half-width is 30; add a small margin so the miss is clean
        miss_margin = 36
        if not (brick.xcor() - miss_margin < predicted_x < brick.xcor() + miss_margin):
            return  # Already off course — nothing to do

        # Rotate velocity vector by 0.4° away from the brick
        angle = math.atan2(self.dy, self.dx)
        speed = math.sqrt(self.dx ** 2 + self.dy ** 2)
        if predicted_x <= brick.xcor():
            angle -= math.radians(0.4)  # nudge left
        else:
            angle += math.radians(0.4)  # nudge right
        self.dx = speed * math.cos(angle)
        self.dy = speed * math.sin(angle)

    def adjust_speed(self):
        """
        Ensure the ball's speed does not exceed the maximum allowed speed.
        """
        speed = math.sqrt(self.dx**2 + self.dy**2)
        if speed > MAX_BALL_SPEED:
            factor = MAX_BALL_SPEED / speed
            self.dx *= factor
            self.dy *= factor

# Brick class definition
class Brick(turtle.Turtle):
    """
    Brick class represents each brick in the game.
    """
    def __init__(self, x, y, color):
        super().__init__()
        self.penup()
        self.shape("square")
        self.shapesize(stretch_wid=1, stretch_len=3)
        self.color("white", color)  # Outline color white, fill color as specified
        self.goto(x, y)

# Game management class
class BrickBreaker:
    """
    BrickBreaker class manages the game state, including bricks, paddle, and ball.
    """
    def __init__(self):
        self.paddle = Paddle()
        self.ball = Ball(self.clear_message)
        self.bricks = []
        self.create_bricks()
        self.message = turtle.Turtle(visible=False)
        self.message.color("white")
        self.message.penup()
        self.message.goto(0, 250)
        self.display_message("Press Space to Bust Some Balls", True)

    def create_bricks(self):
        """
        Create bricks and arrange them in rows with different colors.
        """
        colors = ["red", "yellow", "green", "blue", "orange"]
        start_x = -270
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
        """
        Main game loop — runs at a fixed frame rate so ball speed is
        consistent regardless of how many bricks remain on screen.
        """
        while True:
            frame_start = time.time()

            wn.update()
            self.paddle.move()
            self.ball.move()
            self.ball.adjust_speed()

            # Steer ball away from the last brick each frame
            if len(self.bricks) == 1:
                self.ball.avoid_last_brick(self.bricks[0])

            # Paddle collision
            if (
                self.ball.ycor() < -240
                and self.ball.ycor() > -250
                and self.paddle.xcor() - 60 < self.ball.xcor() < self.paddle.xcor() + 60
            ):
                self.ball.sety(-240)
                hit_pos = self.ball.xcor() - self.paddle.xcor()
                self.ball.dy *= -1
                self.ball.dx = 2 * (hit_pos / 60)
                self.ball.adjust_speed()

            # Brick collision
            for brick in self.bricks:
                if (
                    brick.xcor() - 30 < self.ball.xcor() < brick.xcor() + 30
                    and brick.ycor() - 10 < self.ball.ycor() < brick.ycor() + 10
                ):
                    self.ball.dy *= -1
                    brick.hideturtle()
                    self.bricks.remove(brick)
                    break

            # Bottom wall collision
            if self.ball.ycor() < -290:
                self.ball.goto(0, -100)
                self.ball.dx = 0
                self.ball.dy = 0
                self.ball.moving = False
                self.display_message("Press Space to Bust Some Balls", True)

            # Cap to TARGET_FPS so ball speed is tied to real time, not loop speed
            elapsed = time.time() - frame_start
            sleep_time = FRAME_TIME - elapsed
            if sleep_time > 0:
                time.sleep(sleep_time)

# Keyboard bindings and event handling
game = BrickBreaker()
wn.listen()
wn.onkeypress(game.paddle.go_left, "Left")
wn.onkeyrelease(game.paddle.stop_left, "Left")
wn.onkeypress(game.paddle.go_right, "Right")
wn.onkeyrelease(game.paddle.stop_right, "Right")
wn.onkeypress(game.ball.launch_ball, "space")
# Start the main game loop. This function contains its own ``while True`` so
# it blocks here and keeps the turtle window open.
game.run()
