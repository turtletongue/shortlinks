from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length
import os


class LoginForm(FlaskForm):
    username = StringField("Логин", validators=[DataRequired()])
    password = PasswordField("Пароль", validators=[DataRequired()])

    submit = SubmitField('Войти')


class RegistrationForm(FlaskForm):
    username = StringField("Логин", validators=[DataRequired(), Length(3)])
    password = PasswordField("Пароль", validators=[DataRequired(), Length(int(os.environ['MIN_PASSWORD_LENGTH']))])
    password_again = PasswordField("Подтвердите пароль",
                                   validators=[DataRequired(), Length(int(os.environ['MIN_PASSWORD_LENGTH']))])

    submit = SubmitField('Зарегистрироваться')


class CreateLinkForm(FlaskForm):
    link = StringField("Ссылка", validators=[DataRequired(), Length(3)])
    type = SelectField("Тип",
                       choices=[('public', 'Публичная'), ('protected', 'Общего доступа'), ('private', 'Приватная')],
                       validators=[DataRequired()])
    alias = StringField("Псевдоним")

    submit = SubmitField('Создать')

class EditLinkForm(FlaskForm):
    type = SelectField("Тип",
                       choices=[('public', 'Публичная'), ('protected', 'Общего доступа'), ('private', 'Приватная')],
                       validators=[DataRequired()])
    alias = StringField("Псевдоним")

    submit = SubmitField('Сохранить')

class DeleteLinkForm(FlaskForm):
    submit = SubmitField('Удалить')