import turtle
import canvasvg

# TODO: Clean up this nasty code, and add more functions to solve more shapes.


def draw_triangle(**kwargs):
    try:
        t = turtle.Turtle()
        wn = turtle.Screen()
    except Exception as e:
        t = turtle.Turtle()
        wn = turtle.Screen()
    t.hideturtle()

    # Draws the triangle
    t.forward(kwargs['b'])
    t.left(180 - kwargs['theta'])
    t.forward(kwargs['c'])
    t.left(180 - kwargs['delta'])
    t.forward(kwargs['a'])
    t.left(90)
    t.penup()

    # Draws B at the mid point of B
    t.forward((1/2) * kwargs['b'])
    t.right(90)
    t.forward(60)
    t.write(round(kwargs['orgb'], 1), move=False, align="left", font=("Arial", 16, "normal"))
    t.right(180)
    t.forward(60)
    t.left(90)
    t.forward((1/2)*kwargs['b'])
    t.right(90)

    # Draws A at the mid point of A
    t.forward((1/2)*kwargs['a'])
    t.left(90)
    t.forward(60)
    t.write(round(kwargs['orga'], 1), move=False, align="left", font=("Arial", 16, "normal"))
    t.right(180)
    t.forward(60)

    # Draws the C at the mid point of C
    t.left(90)
    t.forward((1/2)*kwargs['a'])
    t.right(180-kwargs['delta'])
    t.forward((1/2)*kwargs['c'])
    t.left(45)
    t.forward(60)
    t.write(round(kwargs['orgc'], 1), move=False, align="left", font=("Arial", 16, "normal"))
    t.left(180)
    t.forward(60)

    # Draws Theta at the 1/3 point of C
    #t.right(180 + kwargs['theta'])
    #t.forward((1/3)*kwargs['c'])
    #t.right(kwargs['theta'])
    #t.forward()
    #t.stamp()
    canvasvg.saveall("image.svg", t.screen.getcanvas())

    wn.clear()
    wn.bye()