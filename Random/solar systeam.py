import turtle
import math
import random

# ----------------------------- Setup Screen -----------------------------
screen = turtle.Screen()
screen.bgcolor("black")
screen.title("Turtle Solar System")
screen.setup(width=900, height=900)
screen.tracer(0)  # Turn off auto screen updates for smoother animation

# ----------------------------- Draw Stars -----------------------------
stars = turtle.Turtle()
stars.hideturtle()
stars.speed(0)
stars.color("white")
for _ in range(100):
    x = random.randint(-450, 450)
    y = random.randint(-450, 450)
    stars.penup()
    stars.goto(x, y)
    stars.dot(random.randint(1, 3))

# ----------------------------- Draw Sun -----------------------------
sun = turtle.Turtle()
sun.shape("circle")
sun.color("yellow")
sun.shapesize(3)  # Makes the sun larger
sun.penup()
sun.goto(0, 0)

# ----------------------------- Planet Class -----------------------------
class Planet:
    def __init__(self, color, radius, size, speed, label, elliptical=False, moon=False):
        self.turtle = turtle.Turtle()
        self.turtle.shape("circle")
        self.turtle.color(color)
        self.turtle.shapesize(size)
        self.turtle.penup()
        self.radius = radius
        self.angle = random.randint(0, 360)  # Start at random angle
        self.speed = speed
        self.label = label
        self.elliptical = elliptical
        self.moon = moon

        # Label turtle
        self.label_turtle = turtle.Turtle()
        self.label_turtle.hideturtle()
        self.label_turtle.color("white")
        self.label_turtle.penup()

        # Optional moon
        if moon:
            self.moon_turtle = turtle.Turtle()
            self.moon_turtle.shape("circle")
            self.moon_turtle.color("gray")
            self.moon_turtle.shapesize(0.3)
            self.moon_turtle.penup()
            self.moon_angle = 0

    def move(self):
        # Elliptical or circular orbit
        a = self.radius
        b = self.radius * 0.6 if self.elliptical else self.radius

        # Calculate position
        x = a * math.cos(math.radians(self.angle))
        y = b * math.sin(math.radians(self.angle))

        self.turtle.goto(x, y)

        # Update label
        self.label_turtle.goto(x + 10, y + 10)
        self.label_turtle.clear()
        self.label_turtle.write(self.label, font=("Arial", 8, "normal"))

        # Update moon if exists
        if self.moon:
            moon_x = x + 15 * math.cos(math.radians(self.moon_angle))
            moon_y = y + 15 * math.sin(math.radians(self.moon_angle))
            self.moon_turtle.goto(moon_x, moon_y)
            self.moon_angle += 6

        self.angle = (self.angle + self.speed) % 360

# ----------------------------- Create Planets -----------------------------
planets = [
    Planet(color="gray", radius=40, size=0.3, speed=2.5, label="Mercury"),
    Planet(color="orange", radius=60, size=0.6, speed=1.9, label="Venus"),
    Planet(color="blue", radius=85, size=0.8, speed=1.5, label="Earth", moon=True),
    Planet(color="red", radius=110, size=0.6, speed=1.2, label="Mars"),
    Planet(color="orange", radius=160, size=1.2, speed=0.8, label="Jupiter", elliptical=True),
    Planet(color="gold", radius=200, size=1.0, speed=0.6, label="Saturn", elliptical=True),
    Planet(color="light blue", radius=240, size=0.9, speed=0.4, label="Uranus", elliptical=True),
    Planet(color="blue", radius=280, size=0.9, speed=0.3, label="Neptune", elliptical=True),
    # Optional:
    # Planet(color="white", radius=320, size=0.3, speed=0.2, label="Pluto", elliptical=True)
]

# ----------------------------- Animate -----------------------------
def update():
    for planet in planets:
        planet.move()
    screen.update()
    screen.ontimer(update, 50)  # Update every 50 ms (~20 FPS)

update()
screen.mainloop()
