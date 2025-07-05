# Import necessary Flask modules and file handling libraries
from flask import Flask, render_template, request, redirect, url_for, session
import json
import os

# File names for data storage
DATA_FILE = "notes.json"
USERS_FILE = "users.json"

def save_notes(notes):
    base_dir = os.path.dirname(__file__) # folder found file
    file_path = os.path.join(base_dir, DATA_FILE) # joint "user.json" with path
    # Save notes to JSON file
    with open(file_path, "w", encoding="utf-8") as f:
       json.dump(notes, f, ensure_ascii=False, indent=4)

def load_notes():
    base_dir = os.path.dirname(__file__) # folder found file
    file_path = os.path.join(base_dir, DATA_FILE) # joint "user.json" with path
    # Load notes from JSON file if exists
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
           return json.load(f)
    return []

def save_users(users):
    base_dir = os.path.dirname(__file__) # folder found file
    file_path = os.path.join(base_dir, USERS_FILE) # joint "user.json" with path
    # Save users to JSON file
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=4)
        
def load_users():
    base_dir = os.path.dirname(__file__) # folder found file
    file_path = os.path.join(base_dir, USERS_FILE) # joint "user.json" with path
     # Load users from JSON file if exists
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return[]
    
notes = load_notes()        # we will store notes here
users = load_users()        # we will store users here
app = Flask(__name__)       # Flask application is starting                 
app.secret_key = "supersecretkey"  # Secret key for session management

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
        users = load_users()  # Load users from file
        
        # Check if credentials match any user
        for user in users:
            if user["username"] == username and user["password"] == password:
                session["user"] = username  # Store user in session
                return redirect(url_for("home"))
        return render_template("login.html", error="Invalid username or password!")
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
        # Add new user to users list
        users.append({
            "username": username,
            "password": password
        })
        save_users(users)  # Save users to file
        return redirect(url_for('login'))  # Redirect to login page
    return render_template("register.html")

@app.route("/index", methods=["GET", "POST"])        # Main page address (like localhost:5000)
def home():
    # Handle form submission
    if request.method == "POST":
        note = request.form.get("note")         # Get the note from the form
        if note:        # If not empty, add to list
            notes.append(note)      # adds the text from form to notes list
            save_notes(notes)       # Write to JSON after each addition
     
    # HTML file to be displayed in browser
    return render_template("index_with_JSON.html", notes=notes, user=session["user"])       

@app.route("/delete/<int:index>", methods=["POST"])
def delete_note(index):
   # Delete note at specified index
   if 0 <= index < len(notes):  # Security check
       del notes[index]         # Delete from list
       save_notes(notes)        # Update JSON file
   return redirect(url_for('home'))         # Refresh page (homepage)

@app.route("/edit/<int:index>", methods=["GET", "POST"])
def edit_note(index):
   # Handle note editing
   if request.method == "POST":
       new_note = request.form.get("note")  # Get updated note from form
       if new_note:
           notes[index] = new_note  # Update note
           save_notes(notes)        # Save changes
       return redirect(url_for('home'))
   current_note = notes[index]      # Get current note for editing
   return render_template("edit_with_JSON.html", note=current_note, index=index)

@app.route("/search", methods=["GET"])
def search():
    # Handle note searching
    query = request.args.get("q")  # Get search query from URL parameters
    
    # Search for exact match in notes
    for note in notes:
        if note == query:
            return f"Found note: {query} <a href='/index'>Back</a>"
        
    return "Note not found <a href='/index'>Back</a>"

if __name__ == "__main__":
   app.run(debug=True)         # Application is started