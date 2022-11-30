from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length
import os

class LoginForm(FlaskForm):
  username = StringField("Логин", validators=[DataRequired(), Length(3)])
  password = StringField("Пароль", validators=[DataRequired(), Length(os.environ['MIN_PASSWORD_LENGTH'])])

  submit = SubmitField('Войти')