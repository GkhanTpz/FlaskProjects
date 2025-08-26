from flask import Blueprint, session, jsonify
from notes.note_manager import load_notes
from auth.routes import login_required

notes = load_notes()

api_bp = Blueprint("api_bp", __name__, url_prefix="/api")

@api_bp.route("/notes", methods=["GET"])
@login_required
def get_notes():
    current_user = session["user"]
    user_note = [note for note in notes if note["user"] == current_user]
    
    return jsonify(user_note)