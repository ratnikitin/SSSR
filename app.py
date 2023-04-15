from flask import Flask, request, json, render_template
import sqlite3
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired


# class LoginForm(FlaskForm):
#     username = StringField('Логин', validators=[DataRequired()])
#     password = PasswordField('Пароль', validators=[DataRequired()])
#     remember_me = BooleanField('Запомнить меня')
#     submit = SubmitField('Войти')


app = Flask(__name__)
app.config['SECRET_KEY'] = 'SuperSecretKey'
# app.debug = True


# # СОЗДАТЬ ДБ
# @app.route('/')
# def index():
#     return render_template('html/carousel.html')
#
#
# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     form = LoginForm()
#     if form.validate_on_submit():
#         return render_template('html/sidebar.html')
#     return render_template('html/register.html', form=form)


@app.route("/")
def home():
    # return render_template('html/carousel.html')
    return render_template('carousel.html')


@app.route("/signin", methods=['POST'])
def signin():
    username = request.form['username']
    password = request.form['password']
    if username and password:
        # тут будет обработка паролья и почты
        validateUser(username, password)
        return render_template('sidebars.html')
        # return json.dumps({'validation' : validateUser(username, password)})
    # тут надо сделать чтобы при неправильном вводе данных или если вовсе учетной записи нет чтобы писало обэтом красным
    return json.dumps({'validation' : False})  # временно


def validateUser(username, password):
    print(username)
    print(password)
    return True


@app.route('/sign')
def sign():
    return render_template('signin.html')


@app.route('/reg')
def reg():
    return render_template('register.html')


@app.route('/sssr')
def sssr_main():
    return render_template('carousel.html')


if __name__ == '__main__':
    app.run(port=8080)
