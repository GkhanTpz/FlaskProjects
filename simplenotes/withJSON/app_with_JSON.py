# Import necessary Flask modules and file handling libraries
from flask import Flask, flash, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf.csrf import CSRFProtect
from auth.user_manager import save_users, load_users
from notes.note_manager import save_notes, load_notes
from functools import wraps
import uuid

def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Check if user is logged in and redirect accordingly
        if "user" not in session:
            flash("Please login to continue.", "warning")
            return redirect(url_for("login"))
        return func(*args, **kwargs)
    return wrapper
                 
notes = load_notes()        # we will store notes here
users = load_users()        # we will store users here
app = Flask(__name__)       # Flask application is starting                 
app.secret_key = "supersecretkey"  # Secret key for session management

# Activate CSRF Protect
csrf = CSRFProtect(app)

@app.route("/login", methods=["GET", "POST"])
def login():
    # Handle user login
    if request.method == "POST":
        username = request.form.get("username")  # Get username from form
        password = request.form.get("password")  # Get password from form
        users = load_users()  # Load users from file
        
        # Check if credentials match any user
        for user in users:
            if user["username"] == username and check_password_hash(user["password"], password):
                session["user"] = username  # Store user in session
                flash("Welcome, " + username, "success")
                return redirect(url_for("home"))
        flash("Invalid username or password", "danger")
        return render_template("login.html")
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
        # Check if username already exists
        for user in users:
            if user["username"] == username:
                flash("This username is already taken.", "danger")
                return redirect(url_for('register'))
            # Check if passwords match
            if confirm != password:
                flash("Passwords do not match", "warning")
                return redirect(url_for("register"))
        hash_password = generate_password_hash(password)  # Convert user password to secure hash format (for JSON)   
        # Add new user to users list
        users.append({
            "username": username,
            "password": hash_password
        })
        save_users(users)  # Save users to file
        flash("Registration successful. You can now login.", "success")
        return redirect(url_for('login'))  # Redirect to login page
    return render_template("register.html")

@app.route("/", methods=["GET", "POST"])        # Main page address (like localhost:5000)
@login_required
def home():
    current_user = session["user"]  # Get current logged in user
    # Handle form submission
    if request.method == "POST":
        note = request.form.get("note")         # Get the note from the form
        if note:        # If not empty, add to list
             # adds the text from form to notes list
            notes.append({
                          "id": str(uuid.uuid4()),  # Generate unique ID for note
                          "note": note,
                          "user": current_user
                          })     
            save_notes(notes)       # Write to JSON after each addition
    # Filter notes to show only current user's notes
    user_note = [note for note in notes if note["user"] == current_user]
    # HTML file to be displayed in browser
    return render_template("index_with_JSON.html", notes=user_note, user=current_user)       

@app.route("/delete/<id>", methods=["POST"])
@login_required
def delete_note(id):    # Delete note at specified id 
    current_user = session["user"]  # Get current logged in user
    # Find note index by ID
    note_index = next((index for index, note in enumerate(notes) if note["id"] == id), None)
    # Check if note exists and belongs to current user
    if note_index is not None and notes[note_index]["user"] == current_user:
       del notes[note_index]         # Delete from list
       save_notes(notes)        # Update JSON file
    else:
        flash("Note not found", "warning")
    return redirect(url_for('home'))         # Refresh page (homepage)

@app.route("/edit/<id>", methods=["GET", "POST"])
@login_required
def edit_note(id):     # Handle note editing
    current_user = session["user"]  # Get current logged in user
    # Find note index by ID
    note_index = next((index for index, note in enumerate(notes) if note["id"] == id), None)
    if request.method == "POST":
        new_note = request.form.get("note")  # Get updated note from form
        # Check if note exists, belongs to user and new content is provided
        if note_index is not None and notes[note_index]["user"] == current_user:
            if new_note:
                notes[note_index]["note"] = new_note  # Update note
                save_notes(notes)        # Save changes
            return redirect(url_for('home'))
    current_note = notes[note_index]["note"]      # Get current note for editing
    return render_template("edit_with_JSON.html", note=current_note, id=id)

@app.route("/search", methods=["GET", "POST"])
@login_required
def search():
    current_user = session["user"]  # Get current logged in user
    # Handle note searching
    query = request.args.get("q")  # Get search query from URL parameters
    
    # Filter notes to current user's notes only
    search = [note for note in notes if note["user"] == current_user]
    # Search for exact match in notes
    for note in search:
        if note["note"] == query:
            return f"Found note: {query} <a href='/'>Back</a>"
    
    # Return not found message if no match
    return "Note not found <a href='/'>Back</a>",404

if __name__ == "__main__":
   app.run(debug=True)         # Application is started