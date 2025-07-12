# Import necessary Flask modules and file handling libraries
from flask import Flask, render_template, request, redirect, url_for, session
from auth.user_manager import save_users, load_users
from notes.note_manager import save_notes, load_notes
from functools import wraps

def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Check if user is logged in and redirect accordingly
        if "user" not in session:
            return redirect(url_for("login"))
        return func(*args, **kwargs)
    return wrapper
                 
notes = load_notes()        # we will store notes here
users = load_users()        # we will store users here
app = Flask(__name__)       # Flask application is starting                 
app.secret_key = "supersecretkey"  # Secret key for session management
 
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
@login_required
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

@app.route("/", methods=["GET", "POST"])        # Main page address (like localhost:5000)
@login_required
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
@login_required
def delete_note(index):
   # Delete note at specified index
   if 0 <= index < len(notes):  # Security check
       del notes[index]         # Delete from list
       save_notes(notes)        # Update JSON file
   return redirect(url_for('home'))         # Refresh page (homepage)

@app.route("/edit/<int:index>", methods=["GET", "POST"])
@login_required
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

@app.route("/search", methods=["GET", "POST"])
@login_required
def search():
    # Handle note searching
    query = request.args.get("q")  # Get search query from URL parameters
    
    # Search for exact match in notes
    for note in notes:
        if note == query:
            return f"Found note: {query} <a href='/'>Back</a>"
        
    return "Note not found <a href='/'>Back</a>",404

if __name__ == "__main__":
   app.run(debug=True)         # Application is started