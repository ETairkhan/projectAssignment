# filepath: /d:/git clone/py/project/app.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from models import db  # Import the db instance from models/__init__.py

app = Flask(__name__)
app.config.from_object('config.Config')

db.init_app(app)  # Initialize the db instance with the app

login_manager = LoginManager(app)
login_manager.login_view = 'login'

from models.user import User
from models.expense import Expense

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Register blueprints and other app configurations