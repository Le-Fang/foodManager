from flask import Blueprint

homepage_bp = Blueprint('homepage_bp', __name__)

# Import the routes
from . import manage_food
from . import llm_recipe