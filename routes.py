import os

from flask import url_for, redirect, render_template, flash
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy.orm import Session
from sqlalchemy import select, delete, or_, and_
from shortuuid import ShortUUID

from models import User, ShortLink
from db import engine
from forms import LoginForm, RegistrationForm, CreateLinkForm, EditLinkForm, DeleteLinkForm
from utils import map_kind_to_type


def initialize_routes(app, login_manager):
    with Session(engine) as session:
        @login_manager.user_loader
        def load_user(user_id):
            return session.scalars(select(User).where(User.id == user_id)).first()

        @app.route('/', methods=['GET', 'POST'])
        @login_required
        def index():
            form = CreateLinkForm()

            if form.validate_on_submit():
                conflicted_link = session.scalars(
                    select(ShortLink).where(ShortLink.alias == form.alias.data)
                ).first()

                if conflicted_link:
                    flash("Данный псевдоним уже занят, попробуйте указать что-нибудь другое")

                    return redirect(url_for('index'))

                shortlink = ShortLink(
                    kind=form.type.data,
                    original=form.link.data,
                    short=ShortUUID().random(length=int(os.environ['LINK_LENGTH'])),
                    alias=form.alias.data if form.alias.data else None,
                    user_id=current_user.id
                )

                session.add(shortlink)
                session.commit()

                return redirect(url_for('index'))

            links = session.scalars(select(ShortLink).where(ShortLink.user_id == current_user.id)).fetchall()

            return render_template(
                'index.html',
                form=form,
                links=map(
                    lambda link: {
                        'id': link.id,
                        'type': map_kind_to_type[link.kind],
                        'original': link.original,
                        'short': os.environ['SITE_URL'] + link.short,
                        'alias': os.environ['SITE_URL'] + link.alias if link.alias else "",
                        'redirects_count': link.redirects_count
                    },
                    links
                )
            )

        @app.route('/edit/<int:id>', methods=['GET', 'POST'])
        @login_required
        def edit_link(id):
            form = EditLinkForm()

            link = session.scalars(
                select(ShortLink).where(and_(ShortLink.id == id, ShortLink.user_id == current_user.id))
            ).first()

            if link is None:
                return "Ссылка не найдена", 404

            if form.validate_on_submit():
                conflicted_link = session.scalars(
                    select(ShortLink).where(and_(ShortLink.alias == form.alias.data, ShortLink.alias is not None, ShortLink.id != id))
                ).first()

                if conflicted_link:
                    flash("Данный псевдоним уже занят, попробуйте указать что-нибудь другое")

                    return redirect(url_for('index'))

                link.kind = form.type.data
                link.alias = form.alias.data

                session.commit()

                return redirect(url_for('index'))

            form.type.data = link.kind
            form.alias.data = link.alias

            delete_form = DeleteLinkForm()

            if delete_form.validate_on_submit():
                session.execute(delete(ShortLink).where(ShortLink.id == link.id))

                return redirect(url_for('index'))

            return render_template('edit.html', form=form, id=id, delete_form=delete_form)

        @app.route('/<link>')
        def process_short_link(link):
            shortlink = session.scalars(
                select(ShortLink).where(or_(ShortLink.short == link, ShortLink.alias == link))
            ).first()

            if shortlink is None:
                return "Ссылка не найдена", 404

            is_invalid_protected = shortlink.kind == "protected" and not current_user.is_authenticated
            is_invalid_private = shortlink.kind == "private" and \
                (not current_user.is_authenticated or current_user.id != shortlink.user_id)

            if is_invalid_private or is_invalid_protected:
                flash('Недостаточно прав для доступа к этой ссылке')

                return redirect(url_for('index'))

            shortlink.redirects_count = ShortLink.redirects_count + 1

            return redirect(shortlink.original)

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
