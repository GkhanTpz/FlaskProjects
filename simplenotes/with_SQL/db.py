import sqlite3

def db_connect():
    conn = sqlite3.connect("notes.db")
    cursor = conn.cursor()
    return conn, cursor

def init_db():
    conn, cursor = db_connect()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def insert_note(text):
    conn, cursor = db_connect()
    cursor.execute("INSERT INTO notes (text) VALUES (?)", (text,))
    conn.commit()
    conn.close()

def get_notes():
    conn, cursor = db_connect()
    cursor.execute("SELECT * FROM notes")
    notes = cursor.fetchall()
    conn.close()
    return notes

def delete_note_from_db(id):
    conn, cursor = db_connect()
    cursor.execute("DELETE FROM notes WHERE id = ?",(id,))
    conn.commit()
    conn.close()

def update_note_in_db(id, new_text):
    conn, cursor = db_connect()
    cursor.execute("UPDATE notes SET text = ? WHERE id = ?",(new_text,id))
    conn.commit()
    conn.close()