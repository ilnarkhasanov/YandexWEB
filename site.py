from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin

app = Flask(__name__)

# app.config['SECRET_KEY'] = 'qweasdasdasqwe'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'db/data.db'

# db = SQLAlchemy(app)
# login_manager = LoginManager()
# login_manager.init_app(app)


# class User(UserMixin, db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(30), unique=True)


@app.route('/')
def hello():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
