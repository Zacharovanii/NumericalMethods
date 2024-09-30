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
        if self.F(0) * self.F(1) < 0:
            return 0, 1
        while a != 10:
            a += 1
            b += 1
            if self.F(a) * self.F(b) < 0:
                lst.append([a, b])
        lst_filter = [abs(i[0] + i[1]) for i in lst]
        lst_min = lst_filter.index(min(lst_filter))
        res = lst[lst_min]
        return res

    @staticmethod
    def chooseSegment(a, b, c, a_val, b_val, c_val, flag):
        a_hat = '+' if a_val >= 0 else '-'
        b_hat = '+' if b_val >= 0 else '-'
        c_hat = '+' if c_val >= 0 else '-'
        a = str(a)[:8]
        b = str(b)[:8]
        c = str(c)[:8]
        left = r'[\stackrel{' + a_hat + '}{' + a + r'}:\stackrel{' + c_hat + '}{' + c + '}]'
        right = r'[\stackrel{' + c_hat + '}{' + c + r'}:\stackrel{' + b_hat + '}{' + b + '}]'
        if flag == 'left':
            left = r'\bcancel{' + left + '}'
        elif flag == 'right':
            right = r'\bcancel{' + right + '}'
        return fr"{left}{right}"

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
    def __init__(self, expression: Expression, a, b, flag, eps=1e-2):
        self.x = symbols('x')
        self.F = expression.F
        self.a = a
        self.b = b
        self.eps = eps
        self.chordEqLatex = r'x = a - \frac{\left(b - a\right) f(a)}{f(b) - f(a)}'
        if flag == 'a':
            self.c2F = lambda a, b, a_values, b_values: a - (a_values * (b - a)) / (b_values - a_values)
            self.chordEqLatex = r'x = a - \frac{\left(b - a\right) f(a)}{f(b) - f(a)}'
        elif flag == 'b':
            self.c2F = lambda a, b, a_values, b_values: b - (b_values * (a - b)) / (b_values - a_values)
            self.chordEqLatex = r'x = b - \frac{\left(a - b\right) f(b)}{f(b) - f(a)}'

    @staticmethod
    def getChordEqLatex(a, b, a_val, b_val):
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
            progress_lst.append(self.getChordEqLatex(a, b, a_values, b_values))
            c2 = self.c2F(a, b, a_values, b_values)
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


class NewtonMethod:
    def __init__(self, expression: Expression, x_a, x_b, eps=1e-4):
        self.x = symbols('x')
        self.expr = expression
        self.F = expression.F
        self.F2 = expression.F2
        self.F1 = expression.F1
        self.a = x_a
        self.b = x_b
        self.eps = eps
        self.chooseABLatex = r'f(c) * f^{\prime\prime}(c) > 0'

    def chooseAB(self):
        aF = self.F(self.a)
        aF2 = self.F2(self.a)
        bF = self.F(self.b)
        bF2 = self.F2(self.b)
        chooseLatex = [
            'Если: c = a',
            f'{aF} * {aF2} > 0',
            'Если: c = b',
            f'{bF} * {bF2} > 0'
        ]
        if self.F(self.a) * self.F2(self.a) >= 0:
            return self.a, chooseLatex
        elif self.F(self.b) * self.F2(self.b) >= 0:
            return self.b, chooseLatex


    @staticmethod
    def newtonFormulaLatex(c, cF, cF1, x):
        c = str(c)[:7]
        cF = str(cF)[:7]
        cF1 = str(cF1)[:7]
        x = str(x)[:7]
        formulaLatex = r'x = ' + c + r' - \frac{' + cF + '}{' + cF1 + '}' + f" = {x}"
        return formulaLatex

    def findRoot(self):
        x_0, latex = self.chooseAB()
        print(x_0)
        a = self.a
        b = self.b
        progress_lst = []
        progress_lst.append(latex)
        while True:
            f = self.F(x_0)
            f1 = self.F1(x_0)
            x = x_0 - f/f1
            if (self.F(a) < 0 < self.F(x)) or (self.F(a) > 0 > self.F(x)):
                temp = [
                    self.newtonFormulaLatex(float(x_0), float(f), float(f1), float(x)),
                    self.expr.chooseSegment(float(a), float(b), float(x), float(self.F(a)),
                                            float(self.F(b)), float(self.F(x)), 'right')
                ]
                progress_lst.append(temp)
                b = x

            else:
                temp = [
                    self.newtonFormulaLatex(float(x_0), float(f), float(f1), float(x)),
                    self.expr.chooseSegment(float(a), float(b), float(x), float(self.F(a)),
                                            float(self.F(b)), float(self.F(x)), 'left')
                ]
                progress_lst.append(temp)
                a = x

            if abs(x - x_0) < self.eps:
                return progress_lst, x
            x_0 = x


if __name__ == "__main__":
    f = Expression('2x**3 + 9x**2 - 4')
    a, b = f.findAB()
    res = NewtonMethod(f, a, b)
    c, x = res.findRoot()
    print(c)
    # print(res.findRoot())
