from flask import Blueprint, session, jsonify, request
from auth.routes import login_required
from models.db import init_db,get_user_by_username, get_user_notes, insert_note, update_note_in_db, delete_note_from_db

# Create API blueprint with /api prefix
api_bp = Blueprint("api_bp", __name__, url_prefix="/api")
init_db()

@api_bp.route("/notes", methods=["GET"])
@login_required
def get_notes():
   """Get all notes for the current user."""
   current_user = session["user"]
   user = get_user_by_username(current_user)
   
   user_notes = get_user_notes(user[0])
   if user_notes:
       return jsonify(list(dict(user_notes).values())), 200
   return jsonify({"error": "Note not found"}), 404

@api_bp.route("/notes", methods=["POST"])
@login_required
def add_note():
   """Add a new note for the current user."""
   current_user = session["user"]
   user = get_user_by_username(current_user)
   data = request.get_json(silent=True)
   new_note = data["note"]
   
   # Check if data is provided
   if not data or "note" not in data:
       return jsonify({"error": "No data provided"}), 400
   
   if new_note:
       insert_note(new_note, user[0])
       user_notes = get_user_notes(user[0])
       return jsonify(list(dict(user_notes).values())), 201
   return jsonify({"error": "Note not updated"}), 400

@api_bp.route("/notes/<id>", methods=["PUT"])
@login_required
def update_note(id):
   """Update an existing note by ID."""
   current_user = session["user"]
   user = get_user_by_username(current_user)
   data = request.get_json(silent=True)
   
   # Validate request data
   if not data or "note" not in data:
       return jsonify({"error": "No data provided"}), 400
   
   updated_note = data["note"]
   if updated_note:
       update_note_in_db(id, updated_note, user[0])
       user_notes = get_user_notes(user[0])
       return jsonify(list(dict(user_notes).values())), 200
   
   return jsonify({"error": "Note not updated"}), 400

@api_bp.route("/notes/<id>", methods=["DELETE"])
@login_required
def delete_note(id):
   """Delete a note by ID."""
   current_user = session["user"]
   user = get_user_by_username(current_user)
   delete_note_from_db(id, user[0])
   
   return jsonify({"message": "Note deleted"}), 200