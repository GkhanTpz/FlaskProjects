# Import necessary Flask modules and database functions
from flask import Blueprint, flash, render_template, redirect, url_for, session, request
from auth.routes import login_required
from notes.forms import NoteForm, SearchForm
from notes.note_manager import save_notes, load_notes
import uuid

# Create Blueprint for notes-related routes
notes_bp = Blueprint("notes_bp", __name__, template_folder="../templates")

# Load existing notes from JSON file
notes = load_notes()


@notes_bp.route("/", methods=["GET", "POST"]) 
@login_required
def home():
    """Display home page with user notes and handle note creation"""
    note_form = NoteForm()
    search_form = SearchForm()
    
    current_user = session["user"]
    
    if note_form.validate_on_submit():
        note = note_form.note.data
        
        # Add note if content exists
        if note:
            notes.append({
                "id": str(uuid.uuid4()),
                "note": note,
                "user": current_user
            })
            save_notes(notes)
            flash("Note added successfully.", "success")
        else:
            flash("Note cannot be empty", "danger")
            
    # Filter notes for current user only
    user_notes = [note for note in notes if note["user"] == current_user]
    return render_template("index_with_JSON.html", notes=user_notes, user=current_user, note_form=note_form, search_form=search_form)


@notes_bp.route("/delete/<id>", methods=["POST"])
@login_required
def delete_note(id):
    """Delete a specific note by ID"""
    current_user = session["user"]
    
    # Find note by ID and verify ownership
    note_index = next((index for index, note in enumerate(notes) if note["id"] == id), None)
    
    if note_index is not None and notes[note_index]["user"] == current_user:
        del notes[note_index]
        save_notes(notes)
        flash("Note deleted successfully.", "success")
    else:
        flash("Note not found", "warning")
        
    return redirect(url_for('notes_bp.home'))


@notes_bp.route("/edit/<id>", methods=["GET", "POST"])
@login_required
def edit_note(id):
    """Edit an existing note"""
    note_form = NoteForm()
    current_user = session["user"]
    
    # Find note by ID
    note_index = next((index for index, note in enumerate(notes) if note["id"] == id), None)
    
    if note_form.validate_on_submit():
        new_note = note_form.note.data
        
        # Update note if valid and user owns it
        if note_index is not None and notes[note_index]["user"] == current_user:
            if new_note:
                notes[note_index]["note"] = new_note
                save_notes(notes)
                flash("Note updated successfully.","success")
                return redirect(url_for('notes_bp.home'))
            else:
                flash("Note cannot be empty.", "danger")
    
    # Pre-populate form with existing note content
    note_form.note.data = notes[note_index]["note"]
    
    return render_template("edit_with_JSON.html", note_form=note_form)


@notes_bp.route("/search", methods=["GET"])
@login_required
def search():
    """Handle note search functionality"""
    search_form = SearchForm(request.args)
    current_user = session["user"]
    user_notes = [note for note in notes if note["user"] == current_user]
    result = []

    if search_form.validate():
        search = search_form.query.data

        # Find exact matches in user's notes
        if search:
            result = [note for note in user_notes if search == note["note"]]
        else:
            flash("Search cannot be empty.", "warning")
            return redirect(url_for("notes_bp.home"))

    return render_template("search.html",  result=result, search_form=search_form)