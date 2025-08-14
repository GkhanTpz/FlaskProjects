# Import necessary Flask modules and database functions
from flask import Blueprint, flash, render_template, request, redirect, url_for, session
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
    form = NoteForm()
    current_user = session["user"]
    
    if form.validate_on_submit():
        note = form.note.data
        
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
    return render_template("index_with_JSON.html", notes=user_notes, user=current_user, form=form)


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
    form = NoteForm()
    current_user = session["user"]
    
    # Find note by ID
    note_index = next((index for index, note in enumerate(notes) if note["id"] == id), None)
    
    if form.validate_on_submit():
        new_note = form.note.data
        
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
    form.note.data = notes[note_index]["note"]
    
    return render_template("edit_with_JSON.html", form=form)


@notes_bp.route("/search")
@login_required
def search():
    """Search for notes containing specific text"""
    current_user = session["user"]
    query = request.args.get("q")

    # Filter to current user's notes only
    user_notes = [note for note in notes if note["user"] == current_user]
    
    # Search for exact match in user's notes
    for user_note in user_notes:
        if user_note["note"] == query:
            return f"Found note: {query} <a href='/'>Back</a>"

    # Return not found if no match
    return "Note not found <a href='/'>Back</a>", 404