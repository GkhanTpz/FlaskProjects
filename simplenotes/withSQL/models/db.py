import os
import sqlite3

# Database file paths
NOTE_PATH = "notes/notes.db"
USER_PATH = "auth/users.db"

def get_file_path(db_path):
    """Get absolute file path for database"""
    base_dir = os.path.dirname(os.path.dirname(__file__))  # Get parent directory of parent directory
    file_path = os.path.join(base_dir, db_path)            # Join base directory with database path
    return file_path

def db_connect(db_path):
    """Connect to database and return connection and cursor"""
    file_path = get_file_path(db_path)      # Get absolute path for database file
    conn = sqlite3.connect(file_path)       # Establish database connection
    cursor = conn.cursor()                  # Create cursor object for executing queries
    return conn, cursor

def create_user(username, password):
    """Insert new user into database"""
    conn, cursor = db_connect(USER_PATH)    # Connect to users database
    # Execute INSERT query to add new user
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ? )", (username, password))
    conn.commit()                           # Save changes to database
    conn.close()                            # Close database connection

def users():
    """Create users table if not exists"""
    conn, cursor = db_connect(USER_PATH)    # Connect to users database
    try:
        # Execute CREATE TABLE query if table doesn't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                password TEXT NOT NULL
            )
        """)
        conn.commit()                       # Save changes to database
        conn.close()                        # Close database connection
        return True                         # Return success status
    except sqlite3.IntegrityError:          # Handle database integrity errors
        conn.close()                        # Close connection on error
        return False                        # Return failure status

def get_user_by_username(username):
    """Fetch user data by username"""
    conn, cursor = db_connect(USER_PATH)    # Connect to users database
    # Execute SELECT query to find user by username
    cursor.execute("SELECT id, username, password FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()                # Get first matching record
    conn.close()                            # Close database connection
    return user                             # Return user data or None

def init_db():
    """Initialize notes table"""
    conn, cursor = db_connect(NOTE_PATH)    # Connect to notes database
    # Execute CREATE TABLE query for notes table
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                note TEXT NOT NULL,
                user_id INTEGER NOT NULL
            )
        """)
        conn.commit()                       # Save changes to database
        conn.close()                        # Close database connection
        return True                         # Return success status
    except sqlite3.IntegrityError:          # Handle database integrity errors
        conn.close()                        # Close connection on error
        return False                        # Return failure status
        
def insert_note(note, user_id):
    """Add new note to database"""
    conn, cursor = db_connect(NOTE_PATH)    # Connect to notes database
    # Execute INSERT query to add new note
    cursor.execute("INSERT INTO notes (note, user_id) VALUES (?, ?)", (note, user_id))
    conn.commit()                           # Save changes to database
    conn.close()                            # Close database connection

def get_notes(user_id):
    """Fetch all notes from database"""
    conn, cursor = db_connect(NOTE_PATH)    # Connect to notes database
    # Execute SELECT query to get user's notes
    cursor.execute("SELECT id, note FROM notes WHERE user_id = ?", (user_id, ))
    notes = cursor.fetchall()               # Get all matching records
    conn.close()                            # Close database connection
    return notes                            # Return list of notes

def delete_note_from_db(id):
    """Delete note by ID"""
    conn, cursor = db_connect(NOTE_PATH)    # Connect to notes database
    # Execute DELETE query to remove note
    cursor.execute("DELETE FROM notes WHERE id = ?", (id,))
    conn.commit()                           # Save changes to database
    conn.close()                            # Close database connection

def update_note_in_db(id, new_note):
    """Update note content by ID"""
    conn, cursor = db_connect(NOTE_PATH)    # Connect to notes database
    # Execute UPDATE query to modify note content
    cursor.execute("UPDATE notes SET note = ? WHERE id = ?", (new_note, id))
    conn.commit()                           # Save changes to database
    conn.close()                            # Close database connection

def search_note_in_db(query, user_id):
    """Search for note containing query text"""
    conn, cursor = db_connect(NOTE_PATH)    # Connect to notes database
    # Execute SELECT query with LIKE operator for text search
    cursor.execute("SELECT note FROM notes WHERE note LIKE ? and user_id = ?", (query, user_id))
    result = cursor.fetchone()              # Get first matching record
    conn.close()                            # Close database connection
    return result                           # Return search result or None