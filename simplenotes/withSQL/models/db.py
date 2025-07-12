import os
import sqlite3

NOTE_PATH = "notes/notes.db"
USER_PATH = "auth/users.db"

def get_file_path(db_path):
    """Get absolute file path for database"""
    base_dir = os.path.dirname(os.path.dirname(__file__))
    file_path = os.path.join(base_dir, db_path)
    return file_path

def db_connect(db_path):
    """Connect to database and return connection and cursor"""
    file_path = get_file_path(db_path)
    conn = sqlite3.connect(file_path)
    cursor = conn.cursor()
    return conn, cursor

def create_user(username, password):
    """Insert new user into database"""
    conn, cursor = db_connect(USER_PATH)
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ? )", (username, password))
    conn.commit()
    conn.close()

def users():
    """Create users table if not exists"""
    conn, cursor = db_connect(USER_PATH)
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                password TEXT NOT NULL
            )
        """)
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        conn.close()
        return False

def get_user_by_username(username):
    """Fetch user data by username"""
    conn, cursor = db_connect(USER_PATH)
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    return user

def init_db():
    """Initialize notes table"""
    conn, cursor = db_connect(NOTE_PATH)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def insert_note(text):
    """Add new note to database"""
    conn, cursor = db_connect(NOTE_PATH)
    cursor.execute("INSERT INTO notes (text) VALUES (?)", (text,))
    conn.commit()
    conn.close()

def get_notes():
    """Fetch all notes from database"""
    conn, cursor = db_connect(NOTE_PATH)
    cursor.execute("SELECT * FROM notes")
    notes = cursor.fetchall()
    conn.close()
    return notes

def delete_note_from_db(id):
    """Delete note by ID"""
    conn, cursor = db_connect(NOTE_PATH)
    cursor.execute("DELETE FROM notes WHERE id = ?", (id,))
    conn.commit()
    conn.close()

def update_note_in_db(id, new_text):
    """Update note text by ID"""
    conn, cursor = db_connect(NOTE_PATH)
    cursor.execute("UPDATE notes SET text = ? WHERE id = ?", (new_text, id))
    conn.commit()
    conn.close()

def search_note_in_db(query):
    """Search for note containing query text"""
    conn, cursor = db_connect(NOTE_PATH)
    cursor.execute("SELECT text FROM notes WHERE text LIKE ?", (query,))
    result = cursor.fetchone()
    conn.close()
    return result