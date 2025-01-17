from flask import Flask, request, redirect, jsonify, url_for, session
from app.models import User
from app.extensions import db
from app import utils
from http import HTTPStatus
from app.login.login import login_required
from .homepage import homepage_bp
from app.rate_limit import rate_limit

@homepage_bp.route('/food', methods=['GET'])
@login_required
@rate_limit(limit=5, interval=60)
def get_food():
    return jsonify({"message": "Food management page"}), HTTPStatus.OK