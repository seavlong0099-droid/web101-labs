import turtle

# Setup screen
SCREEN_W, SCREEN_H = 420, 720
turtle.setup(width=SCREEN_W, height=SCREEN_H)
screen = turtle.Screen()
screen.title("Flower with Colored Petals")
screen.bgcolor("white")

pen = turtle.Turtle()
pen.speed(0)
pen.hideturtle()

# Offset to shift origin to bottom-left
OFFSET_X = -SCREEN_W // 2
OFFSET_Y = -SCREEN_H // 2

def move_to(x, y):
    pen.up()
    pen.goto(OFFSET_X + x, OFFSET_Y + y)
    pen.down()

def draw_circle(x, y, radius, color):
    move_to(x, y - radius)
    pen.color(color)
    pen.begin_fill()
    pen.circle(radius)
    pen.end_fill()

def draw_stem(x, y, width, height, color):
    pen.color(color)
    pen.up()
    pen.goto(OFFSET_X + x - width // 2, OFFSET_Y + y)
    pen.down()
    pen.begin_fill()
    for _ in range(2):
        pen.forward(width)
        pen.left(90)
        pen.forward(height)
        pen.left(90)
    pen.end_fill()

def draw_leaf(x, y, size, color):
    pen.color(color)
    pen.up()
    pen.goto(OFFSET_X + x, OFFSET_Y + y)
    pen.down()
    pen.begin_fill()
    pen.circle(size, 90)
    pen.left(90)
    pen.circle(size, 90)
    pen.left(90)
    pen.end_fill()
    pen.setheading(0)

# Positions
CENTER_X, CENTER_Y = 210, 480
CENTER_RADIUS = 30
PETAL_RADIUS = 60
STEM_WIDTH = 15
STEM_HEIGHT = 240
LEAF_SIZE = 40

# Draw petals: up-right, up-left, lower-right, lower-left
# Petal positions are shifted diagonally from center
petal_positions = {
    "up_right": (CENTER_X + PETAL_RADIUS * 0.7, CENTER_Y + PETAL_RADIUS * 0.7),
    "up_left": (CENTER_X - PETAL_RADIUS * 0.7, CENTER_Y + PETAL_RADIUS * 0.7),
    "lower_right": (CENTER_X + PETAL_RADIUS * 0.7, CENTER_Y - PETAL_RADIUS * 0.7),
    "lower_left": (CENTER_X - PETAL_RADIUS * 0.7, CENTER_Y - PETAL_RADIUS * 0.7)
}

petal_colors = {
    "up_right": "#d7263d",    # red
    "up_left": "#8f3f7f",     # purple
    "lower_right": "#1f4e79", # blue
    "lower_left": "#ff8c1a"   # orange
}

# Draw petals
for key in petal_positions:
    x, y = petal_positions[key]
    draw_circle(x, y, PETAL_RADIUS, petal_colors[key])

# Draw center (small yellow)
draw_circle(CENTER_X, CENTER_Y, CENTER_RADIUS, "#ffea00")

# Draw stem below center
draw_stem(CENTER_X, CENTER_Y - CENTER_RADIUS, STEM_WIDTH, STEM_HEIGHT, "#0b8a2e")

# Draw one leaf on stem (left side)
draw_leaf(CENTER_X - STEM_WIDTH*2, CENTER_Y - CENTER_RADIUS - STEM_HEIGHT//3, LEAF_SIZE, "#7fd64a")

turtle.done()
