import turtle

screen = turtle.Screen()
screen.bgcolor("Gray")

t = turtle.Turtle()
t.speed(10)
t.pensize(2)

for i in range(7):
    t.forward(50)
    t.left(90)
    t.forward(50)
    t.right(90)



turtle.done()    