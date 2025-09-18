from flask import Blueprint, session, jsonify, request
from auth.routes import login_required
from notes.note_manager import load_notes, save_notes
import uuid

# Create API blueprint with /api prefix
api_bp = Blueprint("api_bp", __name__, url_prefix="/api")
# Load existing notes from file
notes = load_notes()

@api_bp.route("/notes", methods=["GET"])
@login_required
def get_notes():
    """Get all notes for the current user"""
    current_user = session["user"]  
    # Filter notes by current user
    user_note = [note for note in notes if note["user"] == current_user]
    return jsonify(user_note)  

@api_bp.route("/notes", methods=["POST"])
@login_required
def add_note():
    """Create a new note"""
    current_user = session["user"]  
    data = request.get_json(silent=True)  
    
    # Check if data is valid
    if not data or "note" not in data:
        return jsonify({"error": "No data provided"}), 400
    
    # Create new note object
    notes.append({
        "id": str(uuid.uuid4()),  
        "note": data["note"],     
        "user": current_user      
    })
    save_notes(notes)  
    return jsonify(notes), 201  

@api_bp.route("/notes/<id>", methods=["PUT"])
@login_required
def update_note(id):
    """Update an existing note"""
    current_user = session["user"] 
    data = request.get_json(silent=True)  
    
    # Check if data is valid
    if not data or "note" not in data:
        return jsonify({"error": "No data provided"}), 400
    
    # Find and update note
    for note in notes:
        if note["id"] == id and note["user"] == current_user:
            note["note"] = data.get("note", note["note"])  
            save_notes(notes)  
            return jsonify(note), 200  
    
    return jsonify({"error": "Note not found"}), 404

@api_bp.route("/notes/<id>", methods=["DELETE"])
@login_required
def delete_note(id):
    """Delete a note"""
    current_user = session["user"] 
    # Get user's notes
    user_notes = [note for note in notes if note["user"] == current_user]
    
    # Find and delete note
    for note in user_notes:
        if note["id"] == id:
            notes.remove(note)  
            save_notes(notes)   
            return jsonify({"message": "Note deleted"}), 200
    
    return jsonify({"error": "Note not found"}), 404