import turtle
import math

# Screen setup
wn = turtle.Screen()
wn.title("Ball Buster")
wn.bgcolor("black")
wn.setup(width=600, height=600)
wn.tracer(0)  # Turn off automatic screen updates for smoother animations

# Paddle class definition
class Paddle(turtle.Turtle):
    def __init__(self):
        """Initialize the paddle with shape, color, size, and initial position."""
        super().__init__(shape="square")
        self.color("white")
        self.shapesize(stretch_wid=1, stretch_len=6)
        self.penup()
        self.goto(0, -250)
        self.speed("fastest")  # Set to maximum speed for instant response
        self.moving_left = False
        self.moving_right = False

    def move(self):
        """Move the paddle left or right based on the current direction flags."""
        if self.moving_left:
            x = self.xcor() - 3
            if x < -250:
                x = -250  # Limit the paddle's movement within the screen
            self.setx(x)
        if self.moving_right:
            x = self.xcor() + 3
            if x > 250:
                x = 250  # Limit the paddle's movement within the screen
            self.setx(x)

    def go_left(self):
        """Set the paddle to move left."""
        self.moving_left = True

    def stop_left(self):
        """Stop moving the paddle left."""
        self.moving_left = False

    def go_right(self):
        """Set the paddle to move right."""
        self.moving_right = True

    def stop_right(self):
        """Stop moving the paddle right."""
        self.moving_right = False

# Ball class definition
class Ball(turtle.Turtle):
    def __init__(self, clear_message_callback):
        """Initialize the ball with shape, color, size, and initial position."""
        super().__init__(shape="circle")
        self.color("red")
        self.penup()
        self.goto(0, -100)
        self.dx = 0
        self.dy = 0
        self.moving = False
        self.clear_message = clear_message_callback
        self.speed = 2.0  # Set a constant speed
        self.max_speed = 3.0  # Set the maximum speed the ball can achieve

    def move(self):
        """
        Move the ball, handle wall collisions, and maintain a constant speed.
        
        This function updates the ball's position based on its velocity (dx, dy),
        checks for collisions with the walls, and adjusts direction if needed.
        """
        if self.moving:
            # Update ball position
            self.setx(self.xcor() + self.dx)
            self.sety(self.ycor() + self.dy)

            # Check for wall collisions and reverse direction if necessary
            if self.xcor() > 290 or self.xcor() < -290:
                self.dx *= -1  # Reverse horizontal direction

            if self.ycor() > 290:
                self.dy *= -1  # Reverse vertical direction

            # Re-normalize speed to maintain consistency
            self.normalize_speed()

    def normalize_speed(self):
        """
        Ensure the ball maintains a consistent speed after each move.
        
        Normalize the speed to the set speed while ensuring it does not exceed the max_speed.
        """
        magnitude = math.sqrt(self.dx**2 + self.dy**2)
        if magnitude != 0:
            # Adjust the speed to not exceed the maximum speed
            if magnitude > self.max_speed:
                self.dx = (self.dx / magnitude) * self.max_speed
                self.dy = (self.dy / magnitude) * self.max_speed
            else:
                self.dx = (self.dx / magnitude) * self.speed
                self.dy = (self.dy / magnitude) * self.speed

    def launch_ball(self):
        """Launch the ball at a 45-degree angle when the game starts."""
        if not self.moving:
            angle = math.radians(45)  # Launch at 45 degrees
            self.dx = self.speed * math.cos(angle)
            self.dy = self.speed * math.sin(angle)
            self.moving = True
            self.clear_message()  # Clear the start message when the ball is launched

# Brick class definition
class Brick(turtle.Turtle):
    def __init__(self, x, y, color):
        """Initialize a brick with position and color."""
        super().__init__()
        self.penup()
        self.shape("square")
        self.shapesize(stretch_wid=1, stretch_len=3)
        self.color("white", color)
        self.goto(x, y)

# Game management class
class BrickBreaker:
    def __init__(self):
        """Initialize the game, create paddle, ball, and bricks, and set up messages."""
        self.paddle = Paddle()
        self.ball = Ball(self.clear_message)
        self.bricks = []
        self.create_bricks()  # Create the grid of bricks
        self.message = turtle.Turtle(visible=False)
        self.message.color("white")
        self.message.penup()
        self.message.goto(0, 250)
        self.display_message("Press Space to Bust Some Balls", True)

    def create_bricks(self):
        """Create a grid of bricks with alternating colors."""
        colors = ["red", "yellow", "green", "blue", "orange"]
        start_x = -280
        for y in range(50, 250, 21):  # Create rows of bricks
            color = colors[(y // 21) % len(colors)]
            for x in range(start_x, 281, 61):  # Create columns of bricks
                brick = Brick(x, y, color)
                self.bricks.append(brick)

    def display_message(self, msg, large=False):
        """Display a message on the screen."""
        self.message.clear()
        font = ("Arial", 24, "bold") if large else ("Arial", 14, "normal")
        self.message.write(msg, align="center", font=font)

    def clear_message(self):
        """Clear the current message from the screen."""
        self.message.clear()

    def run(self):
        """
        Main game loop for updating the screen and handling collisions.
        
        This function continuously updates the game state, checks for collisions
        between the ball and paddle/bricks, and manages the ball's movement.
        """
        while True:
            wn.update()  # Update the screen with new positions
            self.paddle.move()  # Move the paddle based on input
            self.ball.move()  # Move the ball

            # Paddle collision
            if self.ball.ycor() < -240 and self.ball.ycor() > -250 and self.paddle.xcor() - 60 < self.ball.xcor() < self.paddle.xcor() + 60:
                self.ball.sety(-240)
                self.ball.dy *= -1  # Reverse vertical direction when hitting the paddle

            # Brick collision
            for brick in self.bricks:
                if brick.distance(self.ball) < 20:
                    self.ball.dy *= -1  # Reverse vertical direction on hitting a brick
                    brick.hideturtle()  # Hide the brick
                    self.bricks.remove(brick)  # Remove the brick from the list
                    break

            # Bottom wall collision
            if self.ball.ycor() < -290:
                # Reset ball position if it goes below the paddle
                self.ball.goto(0, -100)
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
