import math
import turtle
import canvasvg


def sin_deg(number):
    number = math.sin(math.radians(number))
    return number


def cos_deg(number):
    number = math.cos(math.radians(number))
    return number


def tan_deg(number):
    number = math.tan(math.radians(number))
    return number


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


def solve_that_triangle(delta, theta, a, b, c):
    infinite = False

    if delta is None and theta is not None:  # No Delta Angle, Yes Theta Angle
        if a == 0 and b == 0:  # Tests for a case where C and delta are given
            print("C is given, A and B are not")
            delta = 180 - (theta + 90)
            b = c*math.sin(math.radians(theta))
            a = (c**2 - b**2) ** (1/2)

        else:
            try:
                if math.tan(b / a) > 0: print("b and a are both given")

                else:
                    print("b was missing")
                    b = a / math.tan(math.radians(theta))  # Using Trig, b is found

            except ZeroDivisionError:
                print("a was missing")
                a = b * math.tan(math.radians(theta))
            if c > 0: c = c
            else: c = (a ** 2 + b ** 2) ** (1 / 2)
            delta = 180 - (90 + theta)

    elif delta is None and theta is None:  # No Angle (two sides must be given)
        # CHECKS IF THERE IS LESS THAN 2 VALUES GIVEN
        zero_counter = 0
        for values in [a, b, c]:
            if values == 0:
                zero_counter += 1
        if zero_counter > 1:
            infinite = True

        if not infinite:
            try:
                if a/b > 0: print("a and b are both given")
                else:
                    print("a is missing")
                    a = (c**2 - b**2) ** (1/2)
                    print(a)

            except ZeroDivisionError:
                print("b is not given")
                b = (c**2 - a**2) ** (1/2)

            if c > 0: c = c
            else: c = (a**2 + b **2) ** (1/2)
            theta = math.degrees(math.atan(a/b))
            delta = 180 - (90 + theta)

    elif delta is not None and theta is not None:  # Both Theta and Delta Angles needs at least a side
        if a == 0 and b == 0 and c == 0:
            infinite = True

        if not infinite:
            try:
                if a/b > 0: print("a and b are both given")
                else:
                    print("b is given a is not")
                    a = b * math.tan(math.radians(theta))

            except ZeroDivisionError:
                print("b is not given")
                b = a/math.tan(math.radians(theta))
            if c > 0: c = c
            else: c = (a**2 + b**2) ** (1/2)

    elif delta is not None and theta is None:  # No Theta Angle, Yes Delta Angle

        if a == 0 and b == 0:  # Tests for a case where C and delta are given
            print("C is given, A and B are not")
            theta = 180 - (delta + 90)
            b = c*math.sin(math.radians(delta))
            a = (c**2 - b**2) ** (1/2)

        else:
            try:
                if math.tan(b / a) > 0: print("b and a are both given")

                else:
                    print("b was missing")
                    b = a * math.tan(math.radians(delta))  # Using Trig, b is found

            except ZeroDivisionError:
                print("a was missing")
                a = b / math.tan(math.radians(delta))

            if c > 0: c = c
            else: c = (a ** 2 + b ** 2) ** (1 / 2)
            theta = 180 - (90 + delta)

    if not infinite:
        # Finding exact equals proves to be too accurate, therefore, within the range of 1 apart, it should still
        # be accurate-enough™
        assert 1.0 >= round(c ** 2, 1) - round((a ** 2 + b ** 2), 1), \
            print("The values indicate an impossible triangle a {} b {} c {}".format(a, b, c))

        assert round(theta, 1) + round(delta, 1) + 90 == 180, \
            print("angles are bork theta {} delta {}".format(theta, delta))

        print("The triangle is comprised of a 90 degree angle a  theta {} degree angle and a delta {} degree angle"
              .format(theta, delta))

        print("The side lengths are y {} x {} and the distance {}".format(round(a, 1), round(b, 1), round(c, 1)))

        orga, orgb, orgc = a, b, c

        while a >= 1000 or b >= 1000 or c >= 1000:
            a, b, c, delta, theta = (1/2)*a, (1/2)*b, (1/2)*c, math.degrees(math.atan(b/a)), math.degrees(math.atan(a/b))
            if a < 100 or b < 100 or c < 100:
                a, b, c, delta, theta = 2*a, 2*b, 2*c, math.degrees(math.atan(b/a)), math.degrees(math.atan(a/b))
                break

        while a <= 100 or b <= 100 or c <= 100:
            if a > 1000 or b > 1000 or c >= 1000:
                a, b, c = (1/2)*a, (1/2)*b, (1/2)*c
                break
            a, b, c, delta, theta = 2*a, 2*b, 2*c, math.degrees(math.atan(b/a)), math.degrees(math.atan(a/b))

        draw_triangle(a=a, b=b, c=c, delta=delta, theta=theta, orga=orga, orgb=orgb, orgc=orgc)
        return False

    else:
        print("The triangle has infinite solutions")
        return True
