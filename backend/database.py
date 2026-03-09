import sqlite3
import os

DB_NAME = "smart_organizer.db"

def get_db_connection():
    """Create a connection to the SQLite database."""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row  # access columns by name
    return conn

def init_db():
    """Create the users table if it doesn't exist."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            otp_code TEXT,
            otp_expiry REAL,  -- Unix timestamp
            session_token TEXT
        )
    """)
    conn.commit()
    conn.close()

# Initialize the database when this module is imported
init_db()