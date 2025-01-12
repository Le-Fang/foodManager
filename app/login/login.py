from flask import Flask, request, redirect, Blueprint, jsonify, url_for, session
from app.models import User
from app.extensions import db
from app import utils
from http import HTTPStatus
import re
from functools import wraps

login_bp = Blueprint('login_bp', __name__)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        print(session)
        if 'userid' not in session:
            return jsonify({"message": "Unauthorized"}), HTTPStatus.UNAUTHORIZED
        return f(*args, **kwargs)
    return decorated_function

@login_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    session.clear()
    print("session cleared")
    print(session)
    return jsonify({"message": "Logged out successfully"}), HTTPStatus.OK

@login_bp.route('/login', methods=['POST'])
def login():
    # Check if the request is JSON
    if not request.is_json:
        return jsonify({"message": "Request must be JSON"}), HTTPStatus.BAD_REQUEST

    # Get the username and password from the request
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # Check if the username and password are provided
    if not username or not password:
        return jsonify({"message": "Username and password are required"}), HTTPStatus.BAD_REQUEST

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
    # Check if the request is JSON
    if not request.is_json:
        return jsonify({"message": "Request must be JSON"}), HTTPStatus.BAD_REQUEST
    
    # Get the username, password, and email from the request
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')

    # Check if the username, password, and email are provided
    if not username or not password or not email:
        return jsonify({"message": "Username, password, and email are required"}), HTTPStatus.BAD_REQUEST

    # Validate the inputs
    if not validate_user(username, password, email):
        return jsonify({"message": "Invalid username, password, or email"}), HTTPStatus.BAD_REQUEST
    
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

def username_isvalid(username):
    if len(username) < 3 or len(username) > 20:
        return False
    return True

def password_isvalid(password):
    if len(password) < 6 or len(password) > 20:
        return False
    return True

def email_isvalid(email):
    if len(email) > 120:
        return False
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if not re.match(email_regex, email):
        return False
    return True

def validate_user(username, password, email):
    if not username_isvalid(username):
        return False
    if not password_isvalid(password):
        return False
    if not email_isvalid(email):
        return False
    return True