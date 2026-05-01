import turtle

screen = turtle.Screen()
screen.bgcolor("Gray")

t = turtle.Turtle()
t.speed(10)
t.pensize(2)
t.color("blue")

t.penup()
t.goto(0, -100) 
t.pendown()
t.circle(100)

numPearls = 20
angleBetweenPearls = 360  / numPearls

for _ in range(numPearls):
 t.penup() # Lift the pen to move without drawing
 t.goto(0, 0) # Move to the center of the circle
 t.forward(100) # Move forward to the circle's edge
 t.pendown() # Put the pen down to draw the pearl
 t.dot(10) # Draw the pearl with a dot
 t.penup() # Lift the pen to move back without drawing
 t.goto(0, 0) # Move back to the center of the circle
 t.right(angleBetweenPearls)

turtle.done()    