import fractions as f


def get_float_from_fraction(number):
    float_value = float(sum(f.Fraction(s) for s in number.split()))
    return float_value


def format_msg(message, name):
    message = message.replace(">{}".format(name), "")
    return message
