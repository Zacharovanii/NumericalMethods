from flask import Flask, render_template, url_for
from Utils.expression import *
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Optional
from dotenv import load_dotenv
from os import getenv

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
                      default='1e-6')
    submit = SubmitField('Рассчитать!')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/multy_method', methods=["GET", "POST"])
def multy_method():
    form = FuncDataForm()
    if form.validate_on_submit():
        expression = Expression(form.func.data)
        a = float(form.a.data)
        b = float(form.b.data)
        eps = float(form.eps.data)
        try:
            newton = NewtonMethod(expression, a, b, eps=eps)
            newton_progress, newton_root = newton.findRoot()
            return render_template('multy_method.html', newton_root=newton_root,
                                   form=form, newton_progress=newton_progress)
        except ValueError as e:
            return render_template('multy_method.html', error=e, form=form)

    return render_template('multy_method.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
