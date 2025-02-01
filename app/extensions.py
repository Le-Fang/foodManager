from flask_sqlalchemy import SQLAlchemy
from openai import OpenAI
from .config import Config

db = SQLAlchemy()

openai_client = OpenAI(
    api_key=Config.OPENAI_API_KEY
)