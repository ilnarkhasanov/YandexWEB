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


class User(Base):
    __tablename__ = "user"

    email = Column(String, primary_key=True)
    password = Column(String)
    name = Column(String)
    surname = Column(String)

    def __init__(self, email, password, name, surname):
        self.email = email
        self.password = password
        self.name = name
        self.surname = surname


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


@app.route('/')
def redirecting():
    return redirect(url_for('home'))


@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/signup', methods=['GET', 'POST'])
def register():
    # user = User('kjreng', 'fwefewfew', 'fewfewf', 'fewfewf')

    # try:
    #     session.add(user)
    #     session.commit()
    # except:
    #     session.rollback()
    #     raise
    # finally:
    #     session.close()


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


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
