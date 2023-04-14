from flask import Flask, request, render_template
import sqlite3
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


app = Flask(__name__)
app.config['SECRET_KEY'] = 'SuperSecretKey'


# СОЗДАТЬ ДБ
@app.route('/')
def index():
    return render_template('html/carousel.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return render_template('html/sidebar.html')
    return render_template('html/register.html', form=form)