from flask_wtf import FlaskForm
from wtforms.fields import PasswordField, StringField, SubmitField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Length, Email


class SignUpField(FlaskForm):
    email = EmailField('Эл. почта', [Email(), DataRequired()])
    password = PasswordField('Пароль', [DataRequired()])
    name = StringField('Имя', [DataRequired()])
    surname = StringField('Фамилия', [DataRequired()])
    submit = SubmitField('Регистрация')


class SignInField(FlaskForm):
    email = EmailField('Эл. почта', [Email(), DataRequired()])
    password = PasswordField('Пароль', [DataRequired()])
    submit = SubmitField('Войти')
