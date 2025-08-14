# Import necessary Flask modules and database functions
from flask import Blueprint, flash, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from auth.user_manager import save_users, load_users
from auth.forms import LoginForm, RegisterForm
from functools import wraps

# Create Blueprint for authentication routes
auth_bp = Blueprint("auth_bp", __name__, template_folder="../templates")

# Load existing users from JSON file
users = load_users()  

def login_required(func):
    """Decorator function to protect routes that require authentication"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        if "user" not in session:
            flash("Please login to continue.", "warning")
            return redirect(url_for("auth_bp.login"))
        return func(*args, **kwargs)
    return wrapper

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    """Handle user login process"""
    form = LoginForm()
    
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        
        # Check credentials against stored users
        for user in users:
            if user["username"] == username and check_password_hash(user["password"], password):
                session["user"] = username
                flash("Welcome, " + username, "success")
                return redirect(url_for("notes_bp.home"))
        
        # Invalid credentials
        flash("Invalid username or password", "danger")
    
    else:
        # Display form validation errors
        if form.errors:
            for field, errors in form.errors.items():
                for error in errors:
                    flash(f"{getattr(form, field).label.text} - {error}", "danger")
                    
    return render_template("login.html", form=form)

@auth_bp.route("/logout")
@login_required
def logout():
    """Handle user logout process"""
    session.pop("user", None)
    flash("You have been logged out", "info")
    return redirect(url_for("auth_bp.login"))

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    """Handle user registration process"""
    form = RegisterForm()
    
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        
        # Check if username already exists
        for user in users:
            if user["username"] == username:
                flash("This username is already taken.", "danger")
                return redirect(url_for('auth_bp.register'))
        
        # Create new user with hashed password
        hash_password = generate_password_hash(password)
        
        users.append({
            "username": username,
            "password": hash_password
        })
        
        # Save updated user list to file
        save_users(users)
        flash("Registration successful. You can now login.", "success")
        return redirect(url_for('auth_bp.login'))
    
    else:
        # Display form validation errors
        if form.errors:
            for field, errors in form.errors.items():
                for error in errors:
                    flash(f"{getattr(form, field).label.text} - {error}", "danger")
                    
    return render_template("register.html", form=form)