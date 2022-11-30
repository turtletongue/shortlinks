from flask import request, url_for, redirect, render_template, abort, flash
from flask_login import login_user
from sqlalchemy.orm import Session
from sqlalchemy import select

from models import User
from dto import UserDto
from errors import format_error
from db import engine
from forms import LoginForm

def initialize_routes(app, login_manager):
  with Session(engine) as session:
    @login_manager.user_loader
    def load_user(user_id):
      return User.get(user_id)

    @app.route('/login', methods=['GET', 'POST'])
    def login():
      form = LoginForm()

      if form.validate_on_submit():
        user = User.query.filter(username=form.username.data).fetchone()

        if not user.verify_password(form.password.data):
          return abort(400)
          
        login_user(user)
        flash("Logged in successfully")

        return redirect(url_for('index'))

      return render_template('login.html', form=form)

    @app.route('/signup', methods=['POST'])
    def signup():
      return "SignUp"

    @app.route('/logout', methods=['POST'])
    def logout():
      return "Logout"

    @app.route('/users', methods=['POST'])
    def create_user():
      try:
        user_dto = UserDto(request.json)
      except ValueError as error:
        return format_error(400, str(error))

      user = User(username=user_dto.username, password=user_dto.password)
      user.hash_password()

      session.add(user)
      session.commit()

      return user.to_dict(), 201

    @app.route('/users/<id>', methods=['GET'])
    def get_user_by_id(id):
      user = session.scalars(select(User).where(User.id == id)).first()

      if user == None:
        return format_error(404, "User not found")

      return user.to_dict()
      