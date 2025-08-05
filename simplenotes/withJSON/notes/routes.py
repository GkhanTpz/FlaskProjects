###############################
#                             #
#          FOR JSON           #
#                             #
###############################

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
    form = NoteForm()
    current_user = session["user"]  # Get current logged in user
    if form.validate_on_submit():
        note = form.note.data  # Get the note from the form
        if note:  # If not empty, add to list
            # Add the text from form to notes list
            notes.append({
                "id": str(uuid.uuid4()),  # Generate unique ID for note
                "note": note,
                "user": current_user
            })
            save_notes(notes)  # Write to JSON after each addition
    # Filter notes to show only current user's notes
    user_notes = [note for note in notes if note["user"] == current_user]
    return render_template("index_with_JSON.html", notes=user_notes, user=current_user, form=form)


@notes_bp.route("/delete/<id>", methods=["POST"])
@login_required
def delete_note(id):  # Delete note with specified id
    current_user = session["user"]  # Get current logged in user
    # Find note index by ID using generator expression
    note_index = next((index for index, note in enumerate(notes) if note["id"] == id), None)
    # Check if note exists and belongs to current user
    if note_index is not None and notes[note_index]["user"] == current_user:
        del notes[note_index]  # Delete from list
        save_notes(notes)  # Update JSON file
    else:
        flash("Note not found", "warning")
    return redirect(url_for('notes_bp.home'))  


@notes_bp.route("/edit/<id>", methods=["GET", "POST"])
@login_required
def edit_note(id):  
    form = NoteForm()
    current_user = session["user"]  # Get current logged in user
    
    # Find note index by ID using generator expression
    note_index = next((index for index, note in enumerate(notes) if note["id"] == id), None)
    
    if form.validate_on_submit():
        new_note = form.note.data  # Get updated note from form
        # Check if note exists, belongs to user and new content is provided
        if note_index is not None and notes[note_index]["user"] == current_user:
            if new_note:
                notes[note_index]["note"] = new_note  # Update note
                flash("Note updated successfully!","success")
                return redirect(url_for('notes_bp.home'))
            
    form.note.data = notes[note_index]["note"]  # Get current note for editing
    
    # Render edit template with current note content and ID
    return render_template("edit_with_JSON.html", form=form)


# Route for searching notes
@notes_bp.route("/search", methods=["GET"])
@login_required
def search():
    #form = SearchForm()
    current_user = session["user"]  # Get current logged in user
    query = request.args.get("q")  # Get search query from URL parameters

    # Filter notes to current user's notes only
    user_notes = [note for note in notes if note["user"] == current_user]
    
    # Search for exact match in notes
    for user_note in user_notes:
        if user_note["note"] == query:
            # Return success message with back link if found
            return f"Found note: {query} <a href='/'>Back</a>"

    # Return not found message if no match
    return "Note not found <a href='/'>Back</a>", 404
