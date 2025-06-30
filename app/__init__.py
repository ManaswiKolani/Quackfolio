from flask import Flask
from dotenv import load_dotenv
import os
from .routes import start_bp, search_bp, pond_bp


def create_app():
    load_dotenv()
    app = Flask(__name__)
    app.secret_key = os.getenv("SECRET_KEY") 
    app.register_blueprint(start_bp)
    app.register_blueprint(search_bp)
    app.register_blueprint(pond_bp)
    return app
