from flask_sqlalchemy import SQLAlchemy
from app.recipe_agent.recipe_agent import RecipeAgent

db = SQLAlchemy()

recipe_agent = RecipeAgent()


