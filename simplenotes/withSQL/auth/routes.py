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
        user = get_user_by_username(username)

        # Verify user exists and password is correct
        if user and check_password_hash(user[2], password):
            session["user"] = username
            flash("Welcome, " + user[1], "success")
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
    
        user = get_user_by_username(username)
        
        # Check if username is already taken
        if user:
            flash("This username is already taken.", "danger")
            return redirect(url_for("auth_bp.register"))
        
        # Create new user with hashed password
        hash_password = generate_password_hash(password)
        create_user(username, hash_password)
        flash("Registration successful. You can now login.", "success")
        return redirect(url_for("auth_bp.login"))
        
    else:
        # Display form validation errors
        if form.errors:
            for field, errors in form.errors.items():
                for error in errors:
                    flash(f"{getattr(form, field).label.text} - {error}", "danger")
                    
    return render_template("register.html", form=form)