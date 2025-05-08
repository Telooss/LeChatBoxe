import sqlite3
import bcrypt
from config.config import DATABASE
from security.crypt import encrypt_message, decrypt_message  

def init_db():
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash BLOB NOT NULL
    )
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        message TEXT NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)
    conn.commit()
    conn.close()

def register_user(username, password):
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    try:
        cur.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (username, password_hash))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def login_user(username, password):
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute("SELECT password_hash FROM users WHERE username = ?", (username,))
    row = cur.fetchone()
    conn.close()
    return row is not None and bcrypt.checkpw(password.encode(), row[0])

def save_message(username, message):
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    encrypted_message = encrypt_message(message)
    cur.execute("INSERT INTO messages (username, message) VALUES (?, ?)", (username, encrypted_message))
    conn.commit()
    conn.close()

def get_all_messages():
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute("SELECT username, message, timestamp FROM messages")
    rows = cur.fetchall()
    conn.close()
    return [(user, decrypt_message(msg), ts) for user, msg, ts in rows]

if __name__ == "__main__":
    from pprint import pprint
    pprint(get_all_messages())
