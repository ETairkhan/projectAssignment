# filepath: /d:/oldversion/routes/auth_routes.py
from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from models.user_profile import UserProfile
from models.database import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        remember_me = request.form.get('remember')  # Check if the "remember me" field is checked
        user = UserProfile.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user, remember=remember_me)  # Log in user with remember option
            return redirect(url_for('expense_bp.index'))  # Redirect to expense page after login
        else:
            flash('Login failed. Check your username and/or password.')
    return render_template('login.html')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        full_name = request.form.get('full_name')
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = UserProfile(username=username, password=hashed_password, email=email, full_name=full_name)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('auth.login'))
    return render_template('register.html')

@auth_bp.route('/logout')
@login_required
def logout():
    # Print the current user's username before logout to confirm they are logged in
    print(f"Logging out user: {current_user.username}")
    
    # Perform the logout
    logout_user()
    
    # Print the current_user after logout to verify that the session is cleared
    print(f"After logout, current_user: {current_user.username if current_user.is_authenticated else 'None'}")
    
    return redirect(url_for('auth.login'))

