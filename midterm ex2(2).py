import turtle

# Setup screen
screen = turtle.Screen()
screen.setup(600, 600)
screen.bgcolor("white")

t = turtle.Turtle()
t.speed(0)
t.hideturtle()

# Function to draw filled circle
def draw_circle(color, x, y, radius):
    t.penup()
    t.goto(x, y - radius)
    t.pendown()
    t.color(color)
    t.begin_fill()
    t.circle(radius)
    t.end_fill()

# Function to draw filled triangle (for leaves)
def draw_triangle(color, points):
    t.penup()
    t.goto(points[0])
    t.pendown()
    t.color(color)
    t.begin_fill()
    for point in points[1:]:
        t.goto(point)
    t.goto(points[0])
    t.end_fill()

# Function to draw rectangle (for stem)
def draw_rectangle(color, x, y, width, height):
    t.penup()
    t.goto(x, y)
    t.pendown()
    t.color(color)
    t.begin_fill()
    for _ in range(2):
        t.forward(width)
        t.left(90)
        t.forward(height)
        t.left(90)
    t.end_fill()

# Draw longer stem
draw_rectangle("green", 95, -50, 10, 200)

# Draw leaves lower on stem
draw_triangle("limegreen", [(100, -50), (50, 30), (100, -10)])
draw_triangle("limegreen", [(100, -50), (150, 30), (100, -10)])

# Petal radius
r = 50

# Petals (perfectly symmetrical)
draw_circle("red", 50, 190, r)        # top-left
draw_circle("purple", 150, 190, r)    # top-right
draw_circle("darkviolet", 50, 110, r) # bottom-left
draw_circle("orange", 150, 110, r)    # bottom-right

# Center (slightly smaller)
draw_circle("yellow", 100, 150, 40)

turtle.done()
