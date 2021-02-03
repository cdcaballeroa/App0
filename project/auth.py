from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from .models import User
from . import usersDB

auth = Blueprint('auth', __name__)


@auth.route('/login')
def login():
    return render_template('login.html')


@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    # check authentication and hash de password to compare it
    if not user or not check_password_hash(user.password, password):
        flash('El e-mail o la contraseña no son válidos')
        return redirect(url_for('auth.login'))

    # login successful if it is ok
    login_user(user, remember=remember)
    return redirect(url_for('main.profile'))


@auth.route('/signup')
def signup():
    return render_template('signup.html')


@auth.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    user = User.query.filter_by(
        email=email).first()

    if user:  # if user's found
        flash('Ya existe un usuario con este email')
        return redirect(url_for('auth.signup'))

    # create new user with hashed password
    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))

    # add the new user to database
    usersDB.session.add(new_user)
    usersDB.session.commit()

    return redirect(url_for('auth.login'))


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
