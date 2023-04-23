from flask import Flask, request, json, render_template
import db_session
from db_session import User

db_session.global_init("db/data.db")
db_sess = db_session.create_session()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'SuperSecretKey'


@app.route("/")
def home():
    # return render_template('html/carousel.html')
    return render_template('carousel.html')


@app.route("/signin", methods=['POST'])
def signin():
    global db_sess
    email = request.form['username']
    password = request.form['password']
    if email and password:
        db_sess = db_session.create_session()
        for user in db_sess.query(User).filter((User.email == email)):
            print(user.hashed_password, User.check_password(user, password))
            if User.check_password(user, password):
                validateUser(email, password)
                print(user.name)
                return render_template('secondvers.html')

        # return json.dumps({'validation' : validateUser(username, password)})
    # тут надо сделать чтобы при неправильном вводе данных или если вовсе учетной записи нет чтобы писало обэтом красным
            else:
                return json.dumps({'validation': False})  # временно


@app.route("/register", methods=['POST'])
def register():
    global db_sess
    email = request.form['username']
    password = request.form['password']
    name = request.form['name']
    surname = request.form['surname']
    if email and password and name and surname:
        user = User()
        user.name = name
        user.surname = surname
        user.email = email
        for users in db_sess.query(User).filter(User.email == email):
            if users:
                return json.dumps({'validation': False})
        user.password = User.set_password(user, password)
        # db_sess = db_session.create_session()
        db_sess.add(user)
        db_sess.commit()
        validateregisterUser(email, password, name, surname)
        return render_template('secondvers.html')
        # return json.dumps({'validation' : validateUser(username, password)})
    # тут надо сделать чтобы при неправильном вводе данных или если вовсе учетной записи нет чтобы писало обэтом красным
    else:
        return json.dumps({'validation': False})  # временно


def validateUser(username, password):
    print(username)
    print(password)
    return True


def validateregisterUser(username, password, name, surname):
    print(username)
    print(password)
    print(name)
    print(surname)
    return True


@app.route('/sign')
def sign():
    return render_template('signin.html')


@app.route('/reg')
def reg():
    return render_template('register.html')


@app.route('/search_main')
def search_main():
    return render_template('search_main.html')


@app.route('/like')
def like():
    return render_template('.html')


@app.route('/main')
def main():
    return render_template('secondvers.html')


@app.route('/log_out')
def log_out():
    return render_template('carousel.html')


@app.route('/studio')
def studio():
    return render_template('.html')


@app.route('/sssr')
def sssr_main():
    return render_template('carousel.html')
    # return render_template('player.html')  # пока что эта страница но потом должна быть та что выше строчкой


if __name__ == '__main__':
    app.run(port=8000)
