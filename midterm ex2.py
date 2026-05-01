import turtle

# Set up the screen
screen = turtle.Screen()
screen.bgcolor("white")

# Create turtle object
pen = turtle.Turtle()
pen.speed(0)
pen.pensize(5)  # Thicker stem

# Function to draw the original smaller petals
def draw_petal():
    pen.color("red")
    pen.begin_fill()
    pen.circle(100, 60)
    pen.left(120)
    pen.circle(100, 60)
    pen.left(120)
    pen.end_fill()

# Draw flower (6 petals)
pen.penup()
pen.goto(0, 0)
pen.setheading(90)
pen.pendown()

for _ in range(6):
    draw_petal()
    pen.right(60)

# Draw stem (thicker)
pen.penup()
pen.goto(0, -25)
pen.setheading(-90)
pen.color("black")
pen.pendown()
pen.forward(300)

# Function to draw a leaf (variable size)
def draw_leaf(size=40):
    pen.begin_fill()
    pen.circle(size, 60)
    pen.left(120)
    pen.circle(size, 60)
    pen.left(120)
    pen.end_fill()

# Draw smaller left upper leaf
pen.penup()
pen.goto(0, -160)
pen.setheading(110)
pen.color("green")
pen.pensize(3)  # Thin leaf outline
pen.pendown()
draw_leaf(60)

# Draw bigger right upper leaf
pen.penup()
pen.goto(0, -158)
pen.setheading(20)
pen.pendown()
draw_leaf(90)

# lower leaves

pen.penup()
pen.goto(0, -230)
pen.setheading(20)
pen.pendown()
draw_leaf(80)

# Hide turtle and finish
pen.hideturtle()
screen.mainloop()
