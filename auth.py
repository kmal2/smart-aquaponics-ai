import sqlite3
import hashlib

# =========================
# DB CONNECTION
# =========================
def get_conn():
    return sqlite3.connect("aquaponics.db", check_same_thread=False)

# =========================
# INIT USERS TABLE
# =========================
def init_users():
    conn = get_conn()
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )
    """)

    conn.commit()
    conn.close()

# =========================
# HASH PASSWORD
# =========================
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# =========================
# REGISTER USER
# =========================
def register_user(username, password):
    conn = get_conn()
    c = conn.cursor()

    try:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)",
                  (username, hash_password(password)))
        conn.commit()
        return True
    except:
        return False
    finally:
        conn.close()

# =========================
# LOGIN USER
# =========================
def login_user(username, password):
    conn = get_conn()
    c = conn.cursor()

    c.execute("SELECT * FROM users WHERE username=? AND password=?",
              (username, hash_password(password)))

    user = c.fetchone()
    conn.close()

    return user