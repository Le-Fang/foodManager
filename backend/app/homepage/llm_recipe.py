from flask import Flask, request, redirect, jsonify, url_for, session
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import utils
from http import HTTPStatus
from app.login.login import login_required
from app.rate_limit import rate_limit
from .homepage import homepage_bp
from app.models import Food
from app.config import Config
from app.extensions import recipe_agent
from datetime import datetime

@homepage_bp.route('/recipe', methods=['GET'])
@jwt_required()
@rate_limit(limit=60, interval=60)
def get_recipe():
    # Get the userid from the token
    userid = int(get_jwt_identity())

    # Get the list of food objects from db
    food_list = Food.query.filter_by(owner=userid).all()

    # Create a list of foods that are not expired yet
    today_date = datetime.today().date()
    foods = []
    for food in food_list:
        if food.expiration_date.date() >= today_date:
            foods.append({
                "name": food.name,
                "quantity": food.quantity,
                "expiration_date": food.expiration_date
            })
    
    res = recipe_agent.generate_recipe(foods)
    
    return jsonify({"recipe": res.get("recipe")}), HTTPStatus.OK