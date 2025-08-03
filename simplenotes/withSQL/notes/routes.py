###############################
#                             #
#         FOR SQLITE          #
#                             #
###############################

# Import necessary Flask modules and database functions
from flask import Blueprint, flash, render_template, request, redirect, url_for, session
from auth.routes import login_required
from models.db import init_db, get_user_by_username, get_notes, update_note_in_db, insert_note, delete_note_from_db, search_note_in_db

# Create Blueprint for notes-related routes
notes_bp = Blueprint("notes_bp", __name__, template_folder="../templates")

# Initialize the database when the app starts
init_db()

@notes_bp.route("/")
@login_required
def home():
    current_user = session["user"]  # Get current logged in user
    user = get_user_by_username(current_user)  # Get user from database
    # Check if user exists in database
    if not user:
        flash("User not found! Please Sign Up!", "danger")
        return redirect(url_for("auth_bp.register"))
    # Get all notes from the database
    notes = get_notes(user[0])
    return render_template("index_with_SQL.html", notes=notes, user=current_user)

@notes_bp.route("/add", methods=["POST"])
@login_required
def add_note():
    current_user = session["user"]  # Get current logged in user
    user = get_user_by_username(current_user)  # Get user from database
    # Get the note content from the form
    note = request.form.get("note")
    # If note exists, add it to the database
    if note:
        insert_note(note, user[0])  # Insert note with user ID
    return redirect(url_for("notes_bp.home"))


@notes_bp.route("/delete/<int:id>", methods=["POST"])
@login_required
def delete_note(id):
    # Delete the note from database using the ID
    delete_note_from_db(id)
    return redirect(url_for("notes_bp.home"))

@notes_bp.route("/edit/<int:id>")
@login_required
def edit_note(id):
    current_user = session["user"]  # Get current logged in user
    user = get_user_by_username(current_user)  # Get user from database
    # Get all notes from database
    notes = get_notes(user[0])
    # Find the specific note by ID
    current_note = next((note for note in notes if note[0] == id), None)

    # If note doesn't exist, return 404 error
    if current_note is None:
        return "Note not found", 404
    return render_template("edit_with_SQL.html", note=current_note)

@notes_bp.route("/update/<int:id>", methods=["POST"])
@login_required
def update_note(id):
    # Get the new note content from the form
    new_note = request.form.get("new_note")
    # Update the note in the database
    update_note_in_db(id, new_note)
    # Redirect back to home page
    return redirect(url_for("notes_bp.home"))

@notes_bp.route("/search", methods=["GET", "POST"])
@login_required
def search():
    current_user = session["user"]  # Get current logged in user
    user = get_user_by_username(current_user)  # Get user from database
    # Handle note searching
    query = request.args.get("q")  # Get search query from URL parameters

    # Search for note in database
    found_note = search_note_in_db(query, user[0])
    # Check if note was found
    if found_note:
        return f"Found note: {found_note[0]} <a href='/'>Back</a>"
    else:
        return "Note not found <a href='/'>Back</a>", 404