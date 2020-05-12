import datetime
from flask import Flask, render_template, redirect, request
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

from data import db_session
from data.users import User
from data.news import News
from data.registerform import RegisterForm
from data.loginform import LoginForm
from data.newsform import NewsForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


def main():
    db_session.global_init("db/blogs.db")
    app.run()
    '''
    #добавление
    user = User()
    user.name = "Пользователь 1"
    user.about = "О пользователе"
    user.email = "email@email.ru"
    session = db_session.create_session()
    session.add(user)
    session.commit()
    '''
    '''
    #получение, изменение, удаление информации
    session = db_session.create_session()
    user = session.query(User).first()
    print(user.name)

    for user in session.query(User).all():
        print(user)

    for user in session.query(User).filter(User.id > 1, User.email.notilike("%1%")):
        print(user)

    for user in session.query(User).filter((User.id > 1) | (User.email.notilike("%1%"))):
        print(user)

    user = session.query(User).filter(User.id == 1).first()
    print(user)
    user.name = "Измененное имя пользователя"
    user.created_date = datetime.datetime.now()
    session.commit()

    session.query(User).filter(User.id >= 3).delete()
    session.commit()

    user = session.query(User).filter(User.id == 2).first()
    session.delete(user)
    session.commit()
    '''

@app.route("/")
def index():
    session = db_session.create_session()

    if current_user.is_authenticated:
        user = [user for user in session.query(User).all() if user.id == current_user.id][0].name
        wilkommen = user
    else:
        wilkommen = ''
    return render_template("index.html", wilkommen=wilkommen)

@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        session = db_session.create_session()
        if session.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data
        )
        user.set_password(form.password.data)
        session.add(user)
        session.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)

@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")

@app.route('/news')
def news():
    return render_template('news.html')

if __name__ == '__main__':
    main()
