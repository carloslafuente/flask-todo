from flask import redirect, render_template, session
from flask.helpers import flash, url_for
from flask_login.utils import login_required, login_user, logout_user
from app.firestore_service import get_user, put_user
from app.forms import LoginForm
from app.models import UserData, UserModel
from . import auth

from werkzeug.security import generate_password_hash, check_password_hash


@auth.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    context = {
        'login_form': login_form
    }

    if login_form.validate_on_submit():
        username = login_form.username.data
        password = login_form.password.data

        user_doc = get_user(username)

        if user_doc.to_dict() is not None:
            password_from_db = user_doc.to_dict()['password']
            if check_password_hash(password_from_db, password):
                user_data = UserData(username, password)
                user = UserModel(user_data)

                login_user(user)

                flash('Bienvenido de nuevo')

                redirect(url_for('hello'))

            else:
                flash('La informacion no coincide')

        else:
            flash('EL usuario no existe')

        session['username'] = username
        flash('Nombre de usuario registrado correctamente.')
        return redirect(url_for('index'))

    return render_template('login.html', **context)


@auth.route('logout')
@login_required
def logout():
    logout_user()
    flash('Regresa pronto')

    return redirect(url_for('auth.login'))


@auth.route('signup', methods=['GET', 'POST'])
def signup():
    signup_form = LoginForm()

    context = {
        'signup_form': signup_form
    }

    if signup_form.validate_on_submit():
        username = signup_form.username.data
        password = signup_form.password.data

        user_doc = get_user(username)

        if user_doc.to_dict() is None:
            password_hash = generate_password_hash(password)
            user_data = UserData(username, password_hash)
            put_user(user_data)

            user = UserModel(user_data)

            login_user(user)

            flash('Bienvenido')

            return redirect(url_for('hello'))

        else:
            flash('El usuario ya existe')

    return render_template('signup.html', **context)
