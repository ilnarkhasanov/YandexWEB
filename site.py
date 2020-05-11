from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from forms import SignInField, SignUpField

app = Flask(__name__)

app.config['SECRET_KEY'] = 'qweasdasdasqwe'
app.config['SQLALCHEMY_DATABASE_URI'] = 'db/data.db'

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True)


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


@app.route('/')
def redirecting():
    return redirect(url_for('home'))


@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/signup')
def register():
    form = SignUpField()
    
    return render_template('register.html', form=form)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
