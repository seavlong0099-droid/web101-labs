import turtle

# Set up the screen
screen = turtle.Screen()
screen.bgcolor("white")

# Create turtle
t = turtle.Turtle()
t.speed(0)
t.penup()

# Starting position
start_x = -150
start_y = -150

# Number of lines
num_lines = 20

# Colors for the pyramid zones
colors = ['red', 'yellow', 'green']

# Thickness of each bar (height of each step)
bar_height = 15

# Width factor for each step
width_factor = 15

# Vertical gap between rectangles
gap = 3

for i in range(num_lines, 0, -1):
    # Select fill color based on line index
    if i > 13:
        t.fillcolor(colors[0])  # red
    elif i > 7:
        t.fillcolor(colors[1])  # yellow
    else:
        t.fillcolor(colors[2])  # green

    # Set outline color to white
    t.pencolor("white")

    # Calculate x and y to position each bar with a small gap
    x = start_x + (num_lines - i) * width_factor / 2
    y = start_y + (num_lines - i) * (bar_height + gap)

    # Draw filled rectangle with white outline
    t.goto(x, y)
    t.pendown()
    t.begin_fill()
    for _ in range(2):
        t.forward(i * width_factor)  # width depends on line number
        t.left(90)
        t.forward(bar_height)  # thickness of the bar
        t.left(90)
    t.end_fill()
    t.penup()

t.hideturtle()
turtle.done()
