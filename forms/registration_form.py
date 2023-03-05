from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms import BooleanField, SubmitField, IntegerField, DateField, EmailField
from wtforms.validators import DataRequired


class RegistrationForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    surname = StringField('Фамилия')
    name = StringField('Имя')
    age = IntegerField('Возраст')
    position = StringField('Позиция')
    speciality = StringField('Специавльность')
    address = StringField("Адрес")
    password = PasswordField('Пароль')
    submit = SubmitField('Применить')
