from flask import Flask
from config import Config
from models.database import db
from models.user_profile import UserProfile
from routes.expense_routes import expense_bp
from routes.auth_routes import auth_bp
from flask_login import LoginManager

# Define the Flask app first
app = Flask(__name__)

# Set the configuration values
app.config.from_object(Config)
app.config['SESSION_PERMANENT'] = True  # Add this line here to make sure session is permanent

# Initialize the database
db.init_app(app)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(expense_bp)

# User loader function for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return UserProfile.query.get(int(user_id))

# Run the app
if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Create all tables if they don't exist
    app.run(debug=True)
