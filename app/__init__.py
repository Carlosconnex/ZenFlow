from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

# Initialize the database extension
db = SQLAlchemy()

# Constants
APP_NAME = "ZenFlow"
VERSION = "1.2" # Incremented for the Trello refactor
DESCRIPTION = "A Trello-style productivity suite."

def create_app():
    app = Flask(__name__)
    
    # 1. Security: Add a Secret Key
    # This is required for user sessions, logins, and flashing alert messages.
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key-placeholder')
    
    # 2. Database Configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///zenflow.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize the app with the database
    db.init_app(app)

    # 3. Register Blueprints
    # Importing here inside the function prevents circular imports 
    # since routes.py will need to import 'db' from this file.
    from .routes import main
    app.register_blueprint(main)

    return app