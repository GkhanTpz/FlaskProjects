import json
import os

# File names for data storage
DATA_FILE = "notes.json"
USERS_FILE = "users.json"

def save_notes(notes):
    base_dir = os.path.dirname(__file__) # folder found file
    file_path = os.path.join(base_dir, DATA_FILE) # joint "user.json" with path
    # Save notes to JSON file
    with open(file_path, "w", encoding="utf-8") as f:
       json.dump(notes, f, ensure_ascii=False, indent=4)

def load_notes():
    base_dir = os.path.dirname(__file__) # folder found file
    file_path = os.path.join(base_dir, DATA_FILE) # joint "user.json" with path
    # Load notes from JSON file if exists
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
           return json.load(f)
    return []