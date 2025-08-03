###############################
#                             #
#          FOR SQLITE         #
#                             #
###############################

# Import necessary Flask modules and database functions
from flask import Blueprint, flash, render_template, request, redirect, url_for, session
from models.db import users, create_user, get_user_by_username
from auth.forms import LoginForm, RegisterForm
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

# Create authentication blueprint for modular routing
auth_bp = Blueprint("auth_bp", __name__, template_folder="../templates")

# Initialize the database when the app starts
users()

def login_required(func):
    """Decorator function to require login for protected routes"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Check if user is logged in and redirect accordingly
        if "user" not in session:
            flash("Please login to continue.", "warning")
            return redirect(url_for("auth_bp.login"))
        return func(*args, **kwargs)
    return wrapper

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    # Handle user login
    form = LoginForm()                           # Create login form instance
    # Validate form submission
    if form.validate_on_submit():
        username = form.username.data            # Get username from form
        password = form.password.data            # Get password from form
        user = get_user_by_username(username)    # Get user from database

        # Check if user exists and password matches
        if user and check_password_hash(user[2], password):
            session["user"] = username           # Store user in session
            flash("Welcome, " + user[1], "success")
            return redirect(url_for("notes_bp.home"))
        else:
            flash("Invalid username or password", "danger")
            return render_template("login.html", form=form)
    # Render login page for GET requests
    return render_template("login.html", form=form)

@auth_bp.route("/logout")
@login_required
def logout():
    # Remove user from session and redirect to login
    session.pop("user", None)
    flash("You have been logged out", "info")
    return redirect(url_for("auth_bp.login"))

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    # Handle user registration
    form = RegisterForm()                        # Create registration form instance
    # Validate form submission
    if form.validate_on_submit():
        username = form.username.data            # Get username from form
        password = form.password.data            # Get password from form
    
        user = get_user_by_username(username)    # Check if username already exists
        # Check if username is already taken
        if user:
            flash("This username is already taken.", "danger")
            return redirect(url_for("auth_bp.register"))
        else:
            # Convert user password to secure hash format (for database storage)
            hash_password = generate_password_hash(password)
            create_user(username, hash_password)  # Create new user in database
            flash("Registration successful. You can now login.", "success")
            return redirect(url_for("auth_bp.login"))  # Redirect to login page
    # Render registration page for GET requests
    return render_template("register.html", form=form)