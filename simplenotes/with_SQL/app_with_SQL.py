# Import necessary Flask modules and database functions
from flask import Flask, render_template, request, redirect, url_for
from db import init_db, get_notes, update_note_in_db, insert_note, delete_note_from_db

# Create Flask application instance
app = Flask(__name__)

# Initialize the database when the app starts
init_db()

# Home page route - displays all notes
@app.route("/")
def home():
    # Get all notes from the database
    notes = get_notes()
    # Render the main page with the notes
    return render_template("index_with_SQL.html", notes=notes)

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
    new_text = request.form.get("new_note")
    # Update the note in the database
    update_note_in_db(id, new_text)
    # Redirect back to home page
    return redirect(url_for("home"))

# Run the application in debug mode if this file is executed directly
if __name__ =="__main__":
    app.run(debug=True)