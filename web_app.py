from flask import Flask, render_template
from Utils.expression import *

app = Flask(__name__)


@app.route('/<string:func>')
def index(func):
    print(func)
    expr = Expression(str(func))
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)