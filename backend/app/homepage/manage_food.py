from flask import Flask, request, redirect, jsonify, url_for, session
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import User, Food
from app.extensions import db
from app import utils
from http import HTTPStatus
from app.login.login import login_required
from .homepage import homepage_bp
from app.rate_limit import rate_limit
from app.forms.foodForm import AddFoodForm

@homepage_bp.route('/food', methods=['GET'])
@jwt_required()
@rate_limit(limit=60, interval=60)
def get_food():
    # Get the userid from jwt token
    userid = int(get_jwt_identity())

    # Get the list of food objects from db
    food_list = Food.query.filter_by(owner=userid).all()

    # Create a list of foods
    foods = []
    for food in food_list:
        foods.append({
            "id": food.id,
            "name": food.name,
            "quantity": food.quantity,
            "expiration_date": food.expiration_date
        })

    # Return the list of foods to the frontend
    return jsonify({"foods": foods}), HTTPStatus.OK

@homepage_bp.route('/food', methods=['DELETE'])
@jwt_required()
@rate_limit(limit=60, interval=60)
def delete_food():
    # Get the userid from jwt token
    userid = int(get_jwt_identity())

    # Get the food id from the request
    food_id = request.json.get('food_id')

    # Get the food object from the db
    food = Food.query.filter_by(id=food_id, owner=userid).first()

    # Check if the food object exists
    if food is None:
        return jsonify({"message": "Food does not exist"}), HTTPStatus.NOT_FOUND

    # Delete the food object from the db
    db.session.delete(food)
    db.session.commit()

    return jsonify({"message": "Food deleted successfully"}), HTTPStatus.OK

@homepage_bp.route('/food', methods=['PUT'])
@jwt_required()
@rate_limit(limit=60, interval=60)
def update_food():
    # Get the userid from jwt token
    userid = int(get_jwt_identity())

    food_id = request.json.get('food_id')

    # Get the food object from the db
    food = Food.query.filter_by(id=food_id, owner=userid).first()

    if food is None:
        return jsonify({"message": "Food does not exist"}), HTTPStatus.NOT_FOUND

    # Get the form data
    form = AddFoodForm()


    if not form.validate_on_submit():
        print(form.errors)
        return jsonify({"message": "Invalid form", "errors": form.errors}), HTTPStatus.BAD_REQUEST

    # Get the data
    name = form.name.data
    quantity = form.quantity.data
    expiration_date = form.expiration_date.data

    # Update
    food.name = name
    food.quantity = quantity
    food.expiration_date = expiration_date

    # Commit the changes to the db
    db.session.commit()

    return jsonify({"message": "Food updated successfully"}), HTTPStatus.OK

@homepage_bp.route('/food', methods=['POST'])
@jwt_required()
@rate_limit(limit=60, interval=60)
def add_food():
    # Get the userid from the token
    userid = int(get_jwt_identity())

    form = AddFoodForm()

    if not form.validate_on_submit():
        return jsonify({"message": "Invalid form", "errors": form.errors}), HTTPStatus.BAD_REQUEST

    # Get the data from the form
    name = form.name.data
    quantity = form.quantity.data
    expiration_date = form.expiration_date.data

    new_food = Food(name=name, quantity=quantity, expiration_date=expiration_date, owner=userid)

    # Add the food object to the db
    db.session.add(new_food)
    db.session.commit()

    return jsonify({"new_item": {
        "id": new_food.id,
        "name": new_food.name,
        "quantity": new_food.quantity,
        "expiration_date": new_food.expiration_date
    }}), HTTPStatus.CREATED