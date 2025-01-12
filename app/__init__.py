from flask import Flask
from app.config import Config
from app.login.login import login_bp  # Import the Blueprint
from app.extensions import db
from flask_session import Session


app = Flask(__name__)
app.config.from_object(Config)

# Register Blueprints
app.register_blueprint(login_bp)

db.init_app(app)

Session(app)