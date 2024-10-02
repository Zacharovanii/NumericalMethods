from sympy import symbols, diff, latex
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
            f_a = float(self.F(0))
            f_b = float(self.F(1))
            ABLatex = [
                f"f(0) = {f_a}",
                f"f(1) = {f_b}"
            ]
            return 0, 1, ABLatex
        while a != 10:
            a += 1
            b += 1
            if self.F(a) * self.F(b) < 0:
                lst.append([a, b])
        lst_filter = [abs(i[0] + i[1]) for i in lst]
        lst_min = lst_filter.index(min(lst_filter))
        res = lst[lst_min]
        a, b = res[0], res[1]
        f_a = self.F(a)
        f_b = self.F(b)
        ABLatex = [
            f"f({a}) = {f_a}",
            f"f({b}) = {f_b}"
        ]
        return ABLatex

    @staticmethod
    def chooseSegment(a, b, c, a_val, b_val, c_val, flag, l):
        a_hat = '+' if a_val >= 0 else '-'
        b_hat = '+' if b_val >= 0 else '-'
        c_hat = '+' if c_val >= 0 else '-'
        a = str(round(a, l))
        b = str(round(b, l))
        c = str(round(c, l))
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

    def getF1Latex(self):
        return f"f^{r'{\prime}'} = {latex(self.diffExpr_1)}"

    def getF2Latex(self):
        return f"f^{r'{\prime\prime}'} = {latex(self.diffExpr_2)}"


class ChordMethod:
    def __init__(self, expression: Expression, a, b, flag, eps=1e-2):
        self.x = symbols('x')
        self.F = expression.F
        self.a = a
        self.b = b
        self.eps = eps
        self.chordEqLatex = r'x = a - \frac{\left(b - a\right) f(a)}{f(b) - f(a)}'
        self.afterCommaLen = len(str(eps))
        if flag == 'a':
            self.flagAB = 'a'
            self.c2F = lambda a, b, a_values, b_values: a - (a_values * (b - a)) / (b_values - a_values)
            self.chordEqLatex = r'x = a - \frac{\left(b - a\right) f(a)}{f(b) - f(a)}'
        elif flag == 'b':
            self.flagAB = 'b'
            self.c2F = lambda a, b, a_values, b_values: b - (b_values * (b - a)) / (b_values - a_values)
            self.chordEqLatex = r'x = b - \frac{\left(a - b\right) f(b)}{f(b) - f(a)}'

    def getChordEqLatex(self, a, b, a_val, b_val, x):
        l = self.afterCommaLen
        f_a = str(round(a_val, l))
        if a_val < 0:
            f_a = f"({f_a})"
        f_b = str(round(b_val, l))
        a = str(round(a, l))
        b = str(round(b, l))
        x = str(round(x, l))
        if self.flagAB == 'a':
            chordLatex = f"x = {a}{r' - \frac{\left('}{b} - {a}{r'\right) '}{f_a}{'}{'}{f_b} - {f_a}{'}'} = {x}"
            return chordLatex
        elif self.flagAB == 'b':
            chordLatex = f"x = {b}{r' - \frac{\left('}{a} - {b}{r'\right) '}{f_a}{'}{'}{f_b} - {f_a}{'}'} = {x}"
            return chordLatex

    def chooseSegment(self, a, b, c, a_val, b_val, c_val, flag):
        l = self.afterCommaLen
        a_hat = '+' if a_val >= 0 else '-'
        b_hat = '+' if b_val >= 0 else '-'
        c_hat = '+' if c_val >= 0 else '-'
        a = str(round(a, l))
        b = str(round(b, l))
        c = str(round(c, l))
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
        progress_lst.append([f"Идем{r'\:'}по{r'\:'}стороне: {self.flagAB}",
                             self.chordEqLatex])
        if F(a) * F(b) >= 0:
            raise Exception("Initial approximation error")
        if self.flagAB == 'a':
            c1 = a
        elif self.flagAB == 'b':
            c1 = b
        while True:
            a_values = float(F(a))
            b_values = float(F(b))
            # progress_lst.append()
            c2 = self.c2F(a, b, a_values, b_values)
            c_values = float(F(c2))
            if abs(c1 - c2) < eps:
                return progress_lst, round(c1, self.afterCommaLen)
            if (a_values < 0 < c_values) or (a_values > 0 > c_values):
                temp = [
                    self.getChordEqLatex(a, b, a_values, b_values, c2),
                    self.chooseSegment(a, b, c2, a_values, b_values, c_values, 'right')
                ]
                progress_lst.append(temp)
                b = c2
            else:
                temp = [
                    self.getChordEqLatex(a, b, a_values, b_values, c2),
                    self.chooseSegment(a, b, c2, a_values, b_values, c_values, 'left')
                ]
                progress_lst.append(temp)
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
        self.flagAB = None
        self.chooseABLatex = r'f(c) * f^{\prime\prime}(c) > 0'
        self.afterCommaLen = len(str(eps))

    def chooseAB(self):
        aF = self.F(self.a)
        aF2 = self.F2(self.a)
        bF = self.F(self.b)
        bF2 = self.F2(self.b)

        if aF * aF2 >= 0:
            side = r"Идем\:по\:стороне\:a"
            self.flagAB = 'a'
            chooseLatex = [
                self.chooseABLatex,
                r'Если\:c\:=\:a:',
                f'{float(aF)} * {float(aF2)} > 0',
                r'Если\:c\:=\:b:',
                f'{float(bF)} * {float(bF2)} > 0',
                side,
                r'x = c - \frac{f(c)}{f^{\prime}(c)}'
            ]

            return self.a, chooseLatex

        elif bF * bF2 >= 0:
            side = r"Идем\:по\:стороне\:b"
            self.flagAB = 'b'
            chooseLatex = [
                self.chooseABLatex,
                r'Если\:c\:=\:a:',
                f'{float(aF)} * {float(aF2)} > 0',
                r'Если\:c\:=\:b:',
                f'{float(bF)} * {float(bF2)} > 0',
                side,
                r'x = c - \frac{f(c)}{f^{\prime}(c)}'
            ]

            return self.b, chooseLatex

    def newtonFormulaLatex(self, c, cF, cF1, x, iteration):
        l = self.afterCommaLen
        c = format(round(c, l), f'.{l}f').rstrip('0').rstrip('.')
        cF = format(round(cF, l), f'.{l}f').rstrip('0').rstrip('.')
        cF1 = format(round(cF1, l), f'.{l}f').rstrip('0').rstrip('.')
        x = format(round(x, l), f'.{l}f').rstrip('0').rstrip('.')
        formulaLatex = f"x{r'^{('}{iteration}{'}'} = {c} - {r'\frac{'}{cF}{'}{'}{cF1}{'}'} = {x}"
        # formulaLatex = r'x = ' + c + r' - \frac{' + cF + '}{' + cF1 + '}' + f" = {x}"
        return formulaLatex

    def getFlagForChord(self):
        if self.flagAB == 'a':
            return 'b'
        return 'a'

    def findRoot(self):
        x_0, latex = self.chooseAB()
        a = self.a
        b = self.b
        progress_lst = []
        progress_lst.append(latex)
        counter = 1
        while True:
            f = self.F(x_0)
            f1 = self.F1(x_0)
            x = x_0 - f/f1
            if (self.F(a) < 0 < self.F(x)) or (self.F(a) > 0 > self.F(x)):
                temp = [
                    self.newtonFormulaLatex(float(x_0), float(f), float(f1), float(x), counter),
                    self.expr.chooseSegment(float(a), float(b), float(x), float(self.F(a)),
                                            float(self.F(b)), float(self.F(x)), 'right', self.afterCommaLen)
                ]
                progress_lst.append(temp)
                b = x

            else:
                temp = [
                    self.newtonFormulaLatex(float(x_0), float(f), float(f1), float(x), counter),
                    self.expr.chooseSegment(float(a), float(b), float(x), float(self.F(a)),
                                            float(self.F(b)), float(self.F(x)), 'left', self.afterCommaLen)
                ]
                progress_lst.append(temp)
                a = x

            if abs(x - x_0) < self.eps:
                return progress_lst, round(x, self.afterCommaLen)
            x_0 = x
            counter += 1


if __name__ == "__main__":
    f = Expression('x**3 + x**2 - 1')
    # newton = NewtonMethod(f, a, b)
    # newton_progress, newton_root = newton.findRoot()
    # sideAB = newton.getFlagForChord()
    # chord = ChordMethod(f, a, b, sideAB)
    # chord_progress, chord_root = chord.findRoot()
    print(f.findAB())
    # print(res.findRoot())
