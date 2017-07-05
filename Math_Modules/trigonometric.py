import math
from Math_Modules import shapfun
import turtle
import canvasvg


def sin_deg(number):
    """Simply returns the sin in degrees of a number"""
    number = math.sin(math.radians(number))
    return number


def cos_deg(number):
    """Simply returns the cos in degrees of a number"""
    number = math.cos(math.radians(number))
    return number


def tan_deg(number):
    """Simply returns the tan in degrees of a number"""
    number = math.tan(math.radians(number))
    return number


def solve_right_triangle(delta, theta, a, b, c):
    """Solves a right triangle and draws the image *Does not return any value other than a t/f statement
    delta - int/float
    theta - int/float
    a - int/float
    b - int/float
    c - int/float"""
    infinite = False  # Simply used to tell the bot if it should send a image or not, return value of function

    if delta is None and theta is not None:  # No Delta Angle, Yes Theta Angle
        if a == 0 and b == 0:  # Tests for a case where C and delta are given
            delta = 180 - (theta + 90)
            b = c*math.sin(math.radians(theta))
            a = (c**2 - b**2) ** (1/2)

        else:
            try:
                if math.tan(b / a) > 0: pass # If this returns True then c is the only value that needs to be calculated
                else: b = a / math.tan(math.radians(theta))  # We can assume a is given if there is no error
            except ZeroDivisionError: a = b * math.tan(math.radians(theta))

            c = (a ** 2 + b ** 2) ** (1 / 2)
            delta = 180 - (90 + theta)

    elif delta is None and theta is None:  # No Angle (two sides must be given)
        zero_counter = 0
        for values in [a, b, c]:  # Iterates through the current values and finds the 0s
            if values == 0:
                zero_counter += 1
        if zero_counter > 1:  # More than a single 0 implies only a single side is given, unable to be solved
            infinite = True

        if not infinite:
            # The reason we don't check for c here is that we have to have two sides, if a or b is missing c is given.
            try:
                if a/b > 0: pass # If this returns True then c is the only value that needs to be solved for
                else: a = (c**2 - b**2) ** (1/2)
            except ZeroDivisionError: b = (c**2 - a**2) ** (1/2)

            if c > 0: c = c
            else: c = (a**2 + b **2) ** (1/2)
            theta = math.degrees(math.atan(a/b))
            delta = 180 - (90 + theta)

    elif delta is not None and theta is not None:  # Both Theta and Delta Angles needs at least a side
        if a == 0 and b == 0 and c == 0: infinite = True

        if c > 0:
            a = c * math.sin(math.radians(theta))
            b = c * math.cos(math.radians(theta))

        elif not infinite:
            try:
                if a/b > 0: pass # simple test to show that a and b are real values
                else: a = b * math.tan(math.radians(theta))  # If a error is not thrown the numerator has to be 0

            except ZeroDivisionError: b = a/math.tan(math.radians(theta))  # If the denominator is 0, b is known missing.
            else: c = (a**2 + b**2) ** (1/2)

    elif delta is not None and theta is None:  # No Theta Angle, Yes Delta Angle

        if a == 0 and b == 0:  # Tests for a case where C and delta are given
            theta = 180 - (delta + 90)
            b = c*math.sin(math.radians(delta))
            a = (c**2 - b**2) ** (1/2)
        else:
            try:
                if math.tan(b / a) > 0:pass  # a and b are both given
                else: b = a * math.tan(math.radians(delta))
            except ZeroDivisionError: a = b / math.tan(math.radians(delta))

            c = (a ** 2 + b ** 2) ** (1 / 2)
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

        # Regularization
        orga, orgb, orgc = a, b, c
        while a >= 1000 or b >= 1000 or c >= 1000:  # Used to ensure that triangles aren't to big.
            a, b, c, delta, theta = (1/2)*a, (1/2)*b, (1/2)*c, math.degrees(math.atan(b/a)), math.degrees(math.atan(a/b))
            if a < 100 or b < 100 or c < 100:
                a, b, c, delta, theta = 2*a, 2*b, 2*c, math.degrees(math.atan(b/a)), math.degrees(math.atan(a/b))
                break

        while a <= 100 or b <= 100 or c <= 100:  # Used to ensure triangles aren't to small .
            if a > 1000 or b > 1000 or c >= 1000:
                a, b, c = (1/2)*a, (1/2)*b, (1/2)*c
                break
            a, b, c, delta, theta = 2*a, 2*b, 2*c, math.degrees(math.atan(b/a)), math.degrees(math.atan(a/b))

        shapfun.draw_triangle(a=a, b=b, c=c, delta=delta, theta=theta, orga=orga, orgb=orgb, orgc=orgc)
        return False  # Returns that the triangle was not impossible to solve
    else: return True # Returns that the triangle was impossible to solve


