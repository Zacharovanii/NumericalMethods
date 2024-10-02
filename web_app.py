from os import getenv

from dotenv import load_dotenv
from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Optional

from Utils.expression import *

load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = getenv('SECRET_KEY')


class FuncDataForm(FlaskForm):
    func = StringField('Функция:',
                       validators=[DataRequired(message='Заполните все поля')])
    a = StringField('Левая граница:',
                    validators=[Optional()])
    b = StringField('Правая граница',
                    validators=[Optional()])
    eps = StringField('Погрешность:',
                      validators=[DataRequired(message='Заполните все поля')],
                      default='1e-4')
    submit = SubmitField('Рассчитать!')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/multy_method', methods=["GET", "POST"])
def multy_method():
    form = FuncDataForm()
    if form.validate_on_submit():
        expression = Expression(form.func.data)
        F1 = expression.getF1Latex()
        F2 = expression.getF2Latex()
        a = form.a.data
        b = form.b.data
        if not a or not b:
            a, b, ABLatex = expression.findAB()
        else:
            a, b, ABLatex = float(a), float(b), None
        eps = float(form.eps.data)
        try:
            newton = NewtonMethod(expression, a, b, eps=eps)
            newton_progress, newton_root = newton.findRoot()
            sideAB = newton.getFlagForChord()
            chord = ChordMethod(expression, a, b, sideAB, eps=eps)
            chord_progress, chord_root = chord.findRoot()
            return render_template('multy_method.html', ABLatex=ABLatex,
                                   newton_root=newton_root, newton_progress=newton_progress,
                                   chord_root=chord_root, chord_progress=chord_progress,
                                   form=form, F1=F1, F2=F2
                                   )
        except ValueError as e:
            return render_template('multy_method.html', error=e, form=form)

    return render_template('multy_method.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
