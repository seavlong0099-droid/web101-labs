import turtle

def draw_square(size, color, fill_color=None):
    turtle.color(color)
    if fill_color:
        turtle.fillcolor(fill_color)
        turtle.begin_fill()
    for _ in range(4):
        turtle.forward(size)
        turtle.right(90)
    if fill_color:
        turtle.end_fill()

def draw_square_pattern(num_squares, size, color, fill_color=None):
    for _ in range(num_squares):
        draw_square(size, color, fill_color)
        turtle.right(15)  # rotate 15 degrees after each square

# Main program
num_squares = int(input("How many squares to draw? "))
color = input("What color to use? ")
fill = input("Do you want to fill the squares? (yes/no) ").lower()

fill_color = None
if fill == 'yes':
    fill_color = input("Enter fill color: ")

turtle.speed(0)  # fast drawing
draw_square_pattern(num_squares, 100, color, fill_color)
turtle.hideturtle()
turtle.done()
