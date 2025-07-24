# Import necessary Flask modules and database functions
from flask import Flask, flash, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf.csrf import CSRFProtect
from functools import wraps
from models.db import init_db, users, create_user, get_user_by_username, get_notes, update_note_in_db, insert_note, delete_note_from_db, search_note_in_db

# Create Flask application instance
app = Flask(__name__)
app.secret_key = "supersecretkey"  # Secret key for session management

# Activate CSRF Protect
csrf = CSRFProtect(app)

# Initialize the databases when the app starts
init_db()
users()

def login_required(func):
    """Decorator function to require login for protected routes"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Check if user is logged in and redirect accordingly
        if "user" not in session:
            flash("Please login to continue.", "warning")
            return redirect(url_for("login"))
        return func(*args, **kwargs)
    return wrapper
    
@app.route("/login", methods=["GET", "POST"])
def login():
    # Handle user login
    if request.method == "POST":
        username = request.form.get("username")  # Get username from form
        password = request.form.get("password")  # Get password from form
        user = get_user_by_username(username)    # Get user from database
        
        # Check if user exists and password matches
        if user and check_password_hash(user[2], password):
            session["user"] = username  # Store user in session
            flash("Welcome, " + user[1], "success")
            return redirect(url_for("home"))
        else:
            flash("Invalid username or password", "danger")
            return render_template("login.html", error="Invalid username or password")
    # Render login page for GET requests
    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    # Remove user from session and redirect to login
    session.pop("user", None)
    flash("You have been logged out", "info")
    return redirect(url_for("login"))

@app.route("/register", methods=["GET", "POST"])
def register():
    # Handle user registration
    if request.method == "POST":
        username = request.form.get("username")  # Get username from form
        password = request.form.get("password")  # Get password from form
        confirm = request.form.get("confirm")    # Get confirm from form
        user = get_user_by_username(username)    # Check if username already exists
        # Check if username is already taken
        if user:
            flash("This username is already taken.", "danger")
            return redirect(url_for("register"))   
        # Check if passwords match
        if confirm != password:
            flash("Passwords do not match", "warning")
            return redirect(url_for("register"))
        hash_password = generate_password_hash(password) # Convert user password to secure hash format (for database storage)
        create_user(username, hash_password)          # Create new user in database
        flash("Registration successful. You can now login.", "success")
        return redirect(url_for("login"))       # Redirect to login page
    # Render registration page for GET requests
    return render_template("register.html")

# Home page route - displays all notes
@app.route("/")
@login_required
def home():
    current_user = session["user"]               # Get current logged in user
    user = get_user_by_username(current_user)    # Get user from database
    # Check if user exists in database
    if not user:
        flash("User not found! Please Sign Up!", "danger")
        return redirect(url_for("register"))
    # Get all notes from the database
    notes = get_notes(user[0])
    # Render the main page with the notes
    return render_template("index_with_SQL.html", notes=notes, user=current_user)

# Add new note route - handles POST requests only
@app.route("/add", methods=["POST"])
@login_required
def add_note():
    current_user= session["user"]                # Get current logged in user
    user = get_user_by_username(current_user)    # Get user from database
    # Get the note content from the form
    note = request.form.get("note")
    # If note exists, add it to the database
    if note:
        insert_note(note, user[0])               # Insert note with user ID
    # Redirect back to home page
    return redirect(url_for("home"))

# Delete note route - handles POST requests with note ID
@app.route("/delete/<int:id>", methods=["POST"])
@login_required
def delete_note(id):
    # Delete the note from database using the ID
    delete_note_from_db(id)
    # Redirect back to home page
    return redirect(url_for("home"))

# Edit note page route - displays the edit form
@app.route("/edit/<int:id>")
@login_required
def edit_note(id):
    current_user= session["user"]                # Get current logged in user
    user = get_user_by_username(current_user)    # Get user from database
    # Get all notes from database
    notes = get_notes(user[0])
    # Find the specific note by ID
    current_note = next((note for note in notes if note[0] == id), None)

    # If note doesn't exist, return 404 error
    if current_note is None:
        return "Note not found", 404
    # Render edit page with the current note
    return render_template("edit_with_SQL.html", note=current_note)

# Update note route - handles POST requests to save changes
@app.route("/update/<int:id>", methods=["POST"])
@login_required
def update_note(id):
    # Get the new note content from the form
    new_note = request.form.get("new_note")
    # Update the note in the database
    update_note_in_db(id, new_note)
    # Redirect back to home page
    return redirect(url_for("home"))

@app.route("/search", methods=["GET", "POST"])
@login_required
def search():
    current_user= session["user"]                # Get current logged in user
    user = get_user_by_username(current_user)    # Get user from database
    # Handle note searching
    query = request.args.get("q")  # Get search query from URL parameters
    
    # Search for note in database
    found_note = search_note_in_db(query, user[0])
    # Check if note was found
    if found_note:
        return f"Found note: {found_note[0]} <a href='/'>Back</a>"
    else:
        # Return not found message with 404 status
        return "Note not found <a href='/'>Back</a>",404

# Run the application in debug mode if this file is executed directly
if __name__ =="__main__":
    app.run(debug=True)