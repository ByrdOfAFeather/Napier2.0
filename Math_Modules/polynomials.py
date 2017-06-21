import sympy
from sympy.parsing.sympy_parser import parse_expr


def factor(func):
    func = parse_expr(func)
    return sympy.pretty(sympy.factor(func))


def get_dem_roots(func):
    func = parse_expr(func)
    return sympy.pretty(sympy.polys.polyroots.roots(func))


def simplify(func):
    func = parse_expr(func)
    return sympy.simplify(func)
