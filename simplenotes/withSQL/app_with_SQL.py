# Import necessary Flask modules and database functions
from flask import Flask, render_template, request, redirect, url_for, session
from db import init_db, users, create_user, get_user_by_username, get_notes, update_note_in_db, insert_note, delete_note_from_db, search_note_in_db

# Create Flask application instance
app = Flask(__name__)
app.secret_key = "supersecretkey"  # Secret key for session management

# Initialize the databases when the app starts
init_db()
users()

@app.route("/")
def check_login():
    # Check if user is logged in and redirect accordingly
    if "user" in session:
        return redirect(url_for("home"))
    else:
        return redirect(url_for("login"))
    
@app.route("/login", methods=["GET", "POST"])
def login():
    # Handle user login
    if request.method == "POST":
        username = request.form.get("username")  # Get username from form
        password = request.form.get("password")  # Get password from form
        user = get_user_by_username(username)    # Get user from database
        
        # Check if user exists and password matches
        if user and user[2] == password:
            session["user"] = username  # Store user in session
            return redirect(url_for("home"))
        else:
            return render_template("login.html", error="Invalid username or password")
    return render_template("login.html")

@app.route("/logout")
def logout():
    # Remove user from session and redirect to login
    session.pop("user", None)
    return redirect(url_for("login"))

@app.route("/register", methods=["GET", "POST"])
def register():
    # Handle user registration
    if request.method == "POST":
        username = request.form.get("username")  # Get username from form
        password = request.form.get("password")  # Get password from form
        create_user(username, password)          # Create new user in database
        return redirect(url_for("login"))       # Redirect to login page
    return render_template("register.html")

# Home page route - displays all notes
@app.route("/index")
def home():
    # Get all notes from the database
    notes = get_notes()
    # Render the main page with the notes
    return render_template("index_with_SQL.html", notes=notes, user=session["user"])

# Add new note route - handles POST requests only
@app.route("/add", methods=["POST"])
def add_note():
    # Get the note text from the form
    text = request.form.get("note")
    # If text exists, add it to the database
    if text:
        insert_note(text)
    # Redirect back to home page
    return redirect(url_for("home"))

# Delete note route - handles POST requests with note ID
@app.route("/delete/<int:id>", methods=["POST"])
def delete_note(id):
    # Delete the note from database using the ID
    delete_note_from_db(id)
    # Redirect back to home page
    return redirect(url_for("home"))

# Edit note page route - displays the edit form
@app.route("/edit/<int:id>")
def edit_note(id):
    # Get all notes from database
    notes = get_notes()
    # Find the specific note by ID
    current_note = next((note for note in notes if note[0] == id), None)

    # If note doesn't exist, return 404 error
    if current_note is None:
        return "Note not found", 404
    # Render edit page with the current note
    return render_template("edit_with_SQL.html", note=current_note)

# Update note route - handles POST requests to save changes
@app.route("/update/<int:id>", methods=["POST"])
def update_note(id):
    # Get the new note text from the form
    new_note = request.form.get("new_note")
    # Update the note in the database
    update_note_in_db(id, new_note)
    # Redirect back to home page
    return redirect(url_for("home"))

@app.route("/search", methods=["GET"])
def search():
    # Handle note searching
    query = request.args.get("q")  # Get search query from URL parameters
    
    # Search for note in database
    found_note = search_note_in_db(query)
    if found_note:
        return f"Found note: {found_note[0]} <a href='/index'>Back</a>"
    else:
        return "Note not found <a href='/index'>Back</a>"

# Run the application in debug mode if this file is executed directly
if __name__ =="__main__":
    app.run(debug=True)