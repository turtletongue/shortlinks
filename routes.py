from flask import url_for, redirect, render_template, flash
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy.orm import Session
from sqlalchemy import select

from models import User
from db import engine
from forms import LoginForm, RegistrationForm, CreateLinkForm

def initialize_routes(app, login_manager):
  with Session(engine) as session:
    @login_manager.user_loader
    def load_user(user_id):
      return session.scalars(select(User).where(User.id == user_id)).first()

    @app.route('/', methods=['GET', 'POST'])
    @login_required
    def index():
      form = CreateLinkForm()

      return render_template('index.html', form=form)

    @app.route('/login', methods=['GET', 'POST'])
    def login():
      form = LoginForm()

      if current_user.is_authenticated:
        return redirect(url_for('index'))

      if form.validate_on_submit():
        user = session.scalars(select(User).where(User.username == form.username.data)).first()

        if user is None or not user.verify_password(form.password.data):
          flash("Неправильный логин или пароль")

          return render_template('login.html', form=form)

        login_user(user)

        return redirect(url_for('index'))

      return render_template('login.html', form=form)

    @app.route('/signup', methods=['GET', 'POST'])
    def signup():
      form = RegistrationForm()

      if current_user.is_authenticated:
        return redirect(url_for('index'))

      if form.validate_on_submit():
        if form.password.data != form.password_again.data:
          flash('Пароли должны совпадать')

          return render_template('signup.html', form=form)

        user = User(username=form.username.data, password=form.password.data)
        user.hash_password()

        session.add(user)
        session.commit()

        flash('Вы успешно зарегистрировались')

        return redirect(url_for('login'))

      return render_template('signup.html', form=form)

    @app.route('/logout', methods=['GET'])
    @login_required
    def logout():
      logout_user()

      return redirect(url_for('login'))