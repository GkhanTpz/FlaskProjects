import json
import os

USERS_FILE = "users.json"

def save_users(users):
    base_dir = os.path.dirname(__file__) # folder found file
    file_path = os.path.join(base_dir, USERS_FILE) # joint "user.json" with path
    # Save users to JSON file
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=4)
        
def load_users():
    base_dir = os.path.dirname(__file__) # folder found file
    file_path = os.path.join(base_dir, USERS_FILE) # joint "user.json" with path
     # Load users from JSON file if exists
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return[]