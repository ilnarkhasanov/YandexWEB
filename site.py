from flask import Flask, render_template, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from forms import SignInField, SignUpField
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

app = Flask(__name__)
app.config['SECRET_KEY'] = 'qweasdasdasqwe'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'

engine = create_engine('sqlite:///data.db')
Base = declarative_base()

login_manager = LoginManager()
login_manager.init_app(app)


class User(UserMixin, Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    password = Column(String)
    name = Column(String)
    surname = Column(String)

    def __init__(self, email, password, name, surname):
        self.email = email
        self.password = password
        self.name = name
        self.surname = surname


class Goods(UserMixin, Base):
    __tablename__ = "goods"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    about = Column(String)
    cost = Column(Integer)
    url = Column(String)

    def __init__(self, name, about, cost, url):
        self.name = name
        self.about = about
        self.cost = cost
        self.url = url


@login_manager.user_loader
def load_user(user_id):
    session = sessionmaker(engine)()
    got_id = session.query(User).get(user_id)
    session.close()
    return got_id


@app.route('/')
def redirecting():
    return redirect(url_for('home'))


@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/signup', methods=['GET', 'POST'])
def register():
    form = SignUpField()

    session = sessionmaker(bind=engine)()

    if form.validate_on_submit():
        if session.query(User).filter(User.email == form.email.data).first():
            session.close()
            flash('Данный эл. ящик уже зарегестрирован в системе!')
            return render_template('register.html', title='Регистрация', form=form)

        user = User(form.email.data, form.password.data, form.name.data, form.surname.data)
        session.add(user)
        session.commit()
        session.close()
        
        return redirect('/')

    return render_template('register.html', form=form)


@app.route('/signin', methods=['GET', 'POST'])
def login():
    form = SignInField()
    
    if form.validate_on_submit():
        session = sessionmaker(engine)()
        user = session.query(User).filter(User.email == form.email.data, User.password == form.password.data).first()
        if user:
            login_user(user)
            session.close()
            return redirect('/')
        else:
            session.close()
            flash('Повторите попытку')
            return render_template('login.html', title='Войти', form=form)

    return render_template('login.html', form=form)


@app.route('/signout')
@login_required
def logout():
    logout_user()
    return redirect('/signin')


@app.route('/store')
@login_required
def store():
    session = sessionmaker(engine)()
    goods = session.query(Goods).all()
    
    for i in range(len(goods)):
        goods[i].url = """{{ url_for('static', filename='img/goods/""" + goods[i].url + """') }}"""

    for i in goods:
        print(i.url)

    session.close()

    return render_template('store.html', goods=goods)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
