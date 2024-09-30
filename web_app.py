from flask import Flask, render_template
from Utils.expression import *

app = Flask(__name__)


@app.route('/')
def main_page():
    return render_template('main.html')


@app.route('/<string:func>')
def index(func):
    print(func)
    expr = Expression('2x**3 + 9x**2 - 4')
    a, b = expr.findAB()
    chord = NewtonMethod(expr, a, b)
    prog, res = chord.findRoot()
    return render_template('index.html', formulas=prog)


if __name__ == '__main__':
    app.run(debug=True)