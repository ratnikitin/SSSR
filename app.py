from flask import Flask, request, json, render_template
import db_session
from db_session import User, Music
import os
import pathlib
import difflib
import random
import json

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
                return render_template('secondvers.html', songs=update_list(), rand=random_music())

            # return json.dumps({'validation' : validateUser(username, password)}) тут надо сделать чтобы при
            # неправильном вводе данных или если вовсе учетной записи нет чтобы писало обэтом красным
            else:
                return render_template('signin_bad.html')
                # return json.dumps({'validation': False})  # временно
    else:
        return render_template('signin_bad_2.html')


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
                # return json.dumps({'validation': False})
                return render_template('register_bad.html')
        user.password = User.set_password(user, password)
        # db_sess = db_session.create_session()
        db_sess.add(user)
        db_sess.commit()
        validateregisterUser(email, password, name, surname)
        return render_template('secondvers.html', songs=update_list(), rand=random_music())
        # return json.dumps({'validation' : validateUser(username, password)})
    # тут надо сделать чтобы при неправильном вводе данных или если вовсе учетной записи нет чтобы писало обэтом красным
    else:
        return render_template('register_bad_2.html')
        # return json.dumps({'validation': False})  # временно


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
    return render_template('like_song.html')


@app.route('/main')
def main():
    return render_template('secondvers.html', songs=update_list(), rand=random_music())


@app.route('/log_out')
def log_out():
    return render_template('carousel.html')


@app.route('/studio')
def studio():
    return render_template('studio.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    file_audio = request.files['audio_file']
    track_name = request.form['track_name']
    artist = request.form['artist']
    file_cover = request.files['cover_file']
    if file_cover and artist and track_name and file_audio:
        # filename = file_audio.filename
        # file_audio.save(os.path.join(os.path.dirname(__file__), str(artist + "_" + track_name + ".mp3")))
        # file_cover.save(os.path.join(os.path.dirname(__file__), str(artist + "_" + track_name + ".jpeg")))
        file_audio.save(os.path.join(str(os.path.dirname(__file__) + "/static/other/Audio"),
                                     str(artist + "_" + track_name + ".mp3")))
        file_cover.save(os.path.join(str(os.path.dirname(__file__) + "/static/other/Cover"),
                                     str(artist + "_" + track_name + ".jpeg")))
        music = Music()
        music.sound_path = os.path.join(str(os.path.dirname(__file__) + "/static/other/Audio"),
                                        str(artist + "_" + track_name + ".mp3"))
        music.picture_path = os.path.join(str(os.path.dirname(__file__) + "/static/other/Cover"),
                                          str(artist + "_" + track_name + ".jpeg"))
        music.author_name = artist
        music.track_name = track_name
        print(music.sound_path)
        print(music.picture_path)
        print(music.author_name)
        print(music.track_name)
        db_sess.add(music)
        db_sess.commit()
        return render_template('studio_nice.html')
    else:
        return render_template('studio_bad.html')


@app.route('/sssr')
def sssr_main():
    return render_template('carousel.html')


def update_list():
    s = []
    for music in db_sess.query(Music).all():
        s.append(str(music.author_name + "_" + music.track_name))
    print(s)
    return json.dumps(s)


def update_list_for_rand():
    s = []
    for music in db_sess.query(Music).all():
        s.append(str(music.author_name + "_" + music.track_name))
    print(s)
    return s


def random_music():
    r = random.choice(update_list_for_rand())
    print(r)
    return r


@app.route('/search_list', methods=['POST'])
def search_list():
    what = request.form['what']
    s = []
    print(s)
    for music in db_sess.query(Music).all():
        s.append(str(music.author_name + "_" + music.track_name))
    # for music in db_sess.query(Music).all():
    #     s.append(str(music.author_name))
    # for music in db_sess.query(Music).all():
    #     s.append(str(music.track_name))
    print(s)
    matches = difflib.get_close_matches(what, s, n=10)
    print(matches)
    return render_template('search.html', what=what, matches=matches)


def update_list_search(song):
    s = list()
    s.append(song)
    print(s)
    return json.dumps(s)


@app.route('/search_song', methods=['POST'])
def search_song():
    song = request.form['search_song']
    print(song)
    return render_template('secondvers_search.html', songs=update_list_search(song), search=song)


if __name__ == '__main__':
    app.run(port=8000)
