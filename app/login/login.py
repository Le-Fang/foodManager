from flask import Flask, request, redirect, Blueprint, jsonify, url_for, session
from app.models import User
from app.extensions import db
from app import utils
from http import HTTPStatus
from functools import wraps
from app.forms.loginForm import LoginForm
from app.forms.registerForm import RegisterForm
from app.rate_limit import rate_limit

login_bp = Blueprint('login_bp', __name__)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'userid' not in session:
            return jsonify({"message": "Unauthorized"}), HTTPStatus.UNAUTHORIZED
        return f(*args, **kwargs)
    return decorated_function

@login_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    session.clear()
    return jsonify({"message": "Logged out successfully"}), HTTPStatus.OK

@login_bp.route('/login', methods=['POST'])
def login():
    form = LoginForm()

    if not form.validate_on_submit():
        return jsonify({"message": "Invalid form", "errors": form.errors}), HTTPStatus.BAD_REQUEST

    # Get the username and password from the request
    username = form.username.data
    password = form.password.data

    # Check if the user exists
    user = User.query.filter_by(username=username).first()
    if user is None:
        return jsonify({"message": "User does not exist"}), HTTPStatus.NOT_FOUND

    # Check if the password is correct
    if not utils.check_password(password, user.password_hash):
        return jsonify({"message": "Incorrect password"}), HTTPStatus.UNAUTHORIZED
    
    # Set the user in the session
    session['userid'] = user.id
    session['username'] = user.username


    return jsonify({"message": "Logged in successfully"}), HTTPStatus.OK


@login_bp.route('/register', methods=['POST'])
def register():
    form = RegisterForm()

    if not form.validate_on_submit():
        return jsonify({"message": "Invalid form", "errors": form.errors}), HTTPStatus.BAD_REQUEST
    
    # Get the username, password, and email from the request
    username = form.username.data
    password = form.password.data
    email = form.email.data
    
    # Check if the username or email already exists
    if User.query.filter_by(username=username).first() is not None:
        return jsonify({"message": "username already exists"}), HTTPStatus.BAD_REQUEST
    
    if User.query.filter_by(email=email).first() is not None:
        return jsonify({"message": "email already exists"}), HTTPStatus.BAD_REQUEST

    # Create a new user
    new_user = User(username=username, password_hash=utils.hash_password(password), email=email)
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({"message": "User created successfully"}), HTTPStatus.CREATED