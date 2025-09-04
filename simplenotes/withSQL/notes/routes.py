# Import necessary Flask modules and database functions
from flask import Blueprint, flash, render_template, request, redirect, url_for, session, request
from auth.routes import login_required
from notes.forms import NoteForm, SearchForm
from models.db import init_db, get_user_by_username, get_user_notes, update_note_in_db, insert_note, delete_note_from_db, search_note_in_db

# Create Blueprint for notes-related routes
notes_bp = Blueprint("notes_bp", __name__, template_folder="../templates")

# Initialize the database when the app starts
init_db()


@notes_bp.route("/")
@login_required
def home():
    """Display home page with all user notes"""
    note_form = NoteForm()
    search_form = SearchForm()
    
    current_user = session["user"]
    user = get_user_by_username(current_user)
    
    # Handle case where user is not found in database
    if not user:
        flash("User not found! Please Sign Up!", "danger")
        return redirect(url_for("auth_bp.register"))
    
    notes = get_user_notes(user[0])
    return render_template("index_with_SQL.html", notes=notes, user=current_user, note_form=note_form, search_form=search_form)


@notes_bp.route("/add", methods=["POST"])
@login_required
def add_note():
    """Add a new note to the database"""
    note_form = NoteForm()
    current_user = session["user"]
    user = get_user_by_username(current_user)
    note = note_form.note.data
    
    # Validate note content before inserting
    if note:
        insert_note(note, user[0])
        flash("Note added successfully.", "success")
    else:
        flash("Note cannot be empty.", "danger")
        
    return redirect(url_for("notes_bp.home"))
    


@notes_bp.route("/delete/<int:id>", methods=["POST"])
@login_required
def delete_note(id):
    """Delete a specific note by ID"""
    delete_note_from_db(id)
    flash("Note deleted successfully.", "success")
    
    return redirect(url_for("notes_bp.home"))


@notes_bp.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_note(id):
    """Edit an existing note"""
    note_form = NoteForm()
    current_user = session["user"]
    user = get_user_by_username(current_user)
    notes = get_user_notes(user[0])
    
    # Find the specific note to edit
    current_note = next((note for note in notes if note[0] == id), None)
    if current_note is None:
        flash("Note not found", "warning")
    
    if request.method == "GET":
        # Pre-populate form with existing note content
        note_form.note.data = current_note[1]
        return render_template("edit_with_SQL.html", note=current_note, note_form=note_form)
    
    if note_form.validate_on_submit():
        new_note = note_form.note.data
        update_note_in_db(id, new_note)
        flash("Note updated successfully!", "success")
        return redirect(url_for("notes_bp.home"))
    else:
        # Handle validation errors
        flash("Note cannot be empty", "danger")
        return render_template("edit_with_SQL.html", note=current_note, note_form=note_form)


@notes_bp.route("/search", methods=["GET"])
@login_required
def search():
    """Handle note search functionality"""
    search_form = SearchForm(request.args)
    current_user = session["user"]
    user = get_user_by_username(current_user)
    result = []

    if search_form.validate():
        search = search_form.query.data

        # Perform database search if query exists
        if search:
            result = search_note_in_db(search, user[0]) 
        else:
            flash("Search cannot be empty.", "danger")
            return redirect(url_for("notes_bp.home"))

    return render_template("search.html", result=result, search_form=search_form)