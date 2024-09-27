from sympy import symbols, diff
from sympy.parsing.sympy_parser import parse_expr


class Expression:
    def __init__(self, expression: str):
        self.x = symbols('x')
        self.expr = parse_expr(expression, transformations='all', evaluate=False)
        self.diffExpr_1 = diff(self.expr, self.x)
        self.diffExpr_2 = diff(self.diffExpr_1, self.x)

    def findAB(self):
        a = -10
        b = -9
        lst = []
        while a != 10:
            a += 1
            b += 1
            if self.F(a) * self.F(b) < 0:
                lst.append([a, b])
        lst_filter = [abs(i[0] + i[1]) for i in lst]
        lst_min = lst_filter.index(min(lst_filter))
        res = lst[lst_min]
        return res

    def F(self, x):
        return self.expr.subs(self.x, x)

    def F1(self, x):
        return self.diffExpr_1.subs(self.x, x)

    def F2(self, x):
        return self.diffExpr_2.subs(self.x, x)

    def getExpression(self):
        return self.expr

    def getDiff1(self):
        return self.diffExpr_1

    def getDiff2(self):
        return self.diffExpr_2


class ChordMethod:
    def __init__(self, expression: Expression, a, b, eps=1e-2):
        self.x = symbols('x')
        self.F = expression.F
        self.a = a
        self.b = b
        self.eps = eps
        self.chordEqLatex = r'x = a - \frac{\left(b - a\right) f(a)}{f(b) - f(a)}'

    @staticmethod
    def getChordEq(a, b, a_val, b_val):
        f_a = str(a_val)
        f_b = str(b_val)
        a = str(a)
        b = str(b)
        return 'x = ' + a + r' - \frac{\left(' + b + ' - ' + a + r'\right) ' + f_a + '}{' + f_b + ' - ' + f_a + '}'

    @staticmethod
    def chooseSegment(a, b, c, a_val, b_val, c_val, flag):
        a_hat = '+' if a_val >= 0 else '-'
        b_hat = '+' if b_val >= 0 else '-'
        c_hat = '+' if c_val >= 0 else '-'
        a = str(a)
        b = str(b)
        c = str(c)
        left = r'[\stackrel{' + a_hat + '}{' + a + r'}:\stackrel{' + c_hat + '}{' + c + '}]'
        right = r'[\stackrel{' + c_hat + '}{' + c + r'}:\stackrel{' + b_hat + '}{' + b + '}]'
        if flag == 'left':
            left = r'\bcancel{' + left + '}'
        elif flag == 'right':
            right = r'\bcancel{' + right + '}'
        return fr"{left}{right}"

    def findRoot(self):
        F = self.F
        a = self.a
        b = self.b
        eps = self.eps
        progress_lst = []
        if F(a) * F(b) >= 0:
            raise Exception("Initial approximation error")
        c1 = a
        while True:
            a_values = float(F(a))
            b_values = float(F(b))
            progress_lst.append(self.getChordEq(a, b, a_values, b_values))
            c2 = a - (a_values * (a - b)) / (a_values - b_values)
            c_values = float(F(c2))
            if abs(c1 - c2) < eps:
                return progress_lst, c2
            if (a_values < 0 < c_values) or (a_values > 0 > c_values):
                progress_lst.append(self.chooseSegment(a, b, c2, a_values, b_values, c_values, 'right'))
                b = c2
            else:
                progress_lst.append(self.chooseSegment(a, b, c2, a_values, b_values, c_values, 'left'))
                a = c2
            c1 = c2


if __name__ == "__main__":
    f = Expression('5x**3 - 20x + 3')
    print(f.findAB())
    a, b = f.findAB()
    res = ChordMethod(f, a, b)

    print(res.findRoot())
