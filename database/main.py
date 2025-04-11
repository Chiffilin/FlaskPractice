import sqlite3

DB_STORAGE = "database/"
DB_NAME = f"{DB_STORAGE}notes.db"

def connect():
    return sqlite3.connect(DB_NAME)

def init_db()-> str:
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()
    return f"Database: {DB_NAME} was created! "

def create_note(text: str):
    conn = connect()
    cur = conn.cursor()
    cur.execute("INSERT INTO notes (text) VALUES (?)", (text,))
    conn.commit()
    note_id = cur.lastrowid
    conn.close()
    return {"id": note_id, "text": text}

def note_exists(note_id: int) -> bool:
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM notes WHERE id = ?", (note_id,))
    result = cur.fetchone()
    conn.close()
    return result is not None

def get_all_notes():
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT id, text FROM notes")
    rows = cur.fetchall()
    conn.close()
    return [{"id": r[0], "text": r[1]} for r in rows]

def add_new_note(text:str):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO notes (text) VALUES (?)", (text,))
    conn.commit()
    note_id = cursor.lastrowid
    conn.close()
    print(text)
    return {"id": note_id, "text": text}

def update_note(note_id: int, new_text: str):
    if note_exists(note_id):
        conn = connect()
        cursor = conn.cursor()
        cursor.execute("UPDATE notes SET text = ? WHERE id = ?", (new_text, note_id))
        conn.commit()
        conn.close()
        return f"The note{note_id} has been updated"
    else:
        return "Note doesn't found"

def delete_notes(note_id:int):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM notes WHERE id = ?", (note_id,))
    conn.commit()
    conn.close()
    return f"The note {note_id} has been removed."


