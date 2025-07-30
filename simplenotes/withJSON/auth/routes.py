###############################
#                             #
#          FOR JSON           #
#                             #
###############################

# Import necessary Flask modules and database functions
from flask import Blueprint, flash, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from auth.user_manager import save_users, load_users
from functools import wraps

# Create Blueprint for authentication routes
auth = Blueprint("auth", __name__, template_folder="../templates")

# Load existing users from JSON file
users = load_users()  

# Decorator function to protect routes that require authentication
def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Check if user is logged in and redirect accordingly
        if "user" not in session:
            flash("Please login to continue.", "warning")
            return redirect(url_for("auth.login"))
        return func(*args, **kwargs)

    return wrapper

@auth.route("/login", methods=["GET", "POST"])
def login():
    # Handle user login
    if request.method == "POST":
        username = request.form.get("username")  # Get username from form
        password = request.form.get("password")  # Get password from form
        
        # Check if credentials match any user
        for user in users:
            # Verify username and password hash
            if user["username"] == username and check_password_hash(user["password"], password):
                session["user"] = username  # Store user in session
                flash("Welcome, " + username, "success")
                # Redirect to home page after successful login
                return redirect(url_for("notes_bp.home"))
        flash("Invalid username or password", "danger")
        return render_template("login.html")
    return render_template("login.html")

@auth.route("/logout")
@login_required
def logout():
    # Remove user from session and redirect to login
    session.pop("user", None)
    flash("You have been logged out", "info")
    return redirect(url_for("auth.login"))

@auth.route("/register", methods=["GET", "POST"])
def register():
    # Handle user registration
    if request.method == "POST":
        username = request.form.get("username")  # Get username from form
        password = request.form.get("password")  # Get password from form
        confirm = request.form.get("confirm")  # Get confirm from form
        
        # Check if username already exists
        for user in users:
            if user["username"] == username:
                flash("This username is already taken.", "danger")
                return redirect(url_for('auth.register'))
        
        # Check if passwords match
        if confirm != password:
            flash("Passwords do not match", "warning")
            return redirect(url_for("auth.register"))
            
        hash_password = generate_password_hash(password)  # Convert user password to secure hash format (for JSON)
        
        # Add new user to users list
        users.append({
            "username": username,
            "password": hash_password
        })
        save_users(users)  # Save users to file
        flash("Registration successful. You can now login.", "success")
        return redirect(url_for('auth.login')) 
    
    return render_template("register.html")