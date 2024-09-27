import math
import sympy
from sympy import print_latex


def find_root(equation, a, b, err):
    if equation(a) * equation(b) >= 0:
        raise Exception("Initial approximation error")
    c1 = a
    while True:
        a_values = equation(a)
        b_values = equation(b)
        c2 = a - (a_values * (a - b)) / (a_values - b_values)
        c_values = equation(c2)
        if abs(c1 - c2) < err:
            return c2
        if (a_values < 0 < c_values) or (a_values > 0 > c_values):
            b = c2
        else:
            a = c2
        c1 = c2


def F(x): return x ** 2 - math.exp(x)


a = -1
b = 1
err = 0.1

root = find_root(F, a, b, err)
print(root)
print(F(root))
sympy.preview(r'$$\frac{5}{a^{2}}$$', viewer='file', filename='test.png')