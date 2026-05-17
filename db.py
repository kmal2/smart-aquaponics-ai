import sqlite3
import pandas as pd

DB_NAME = "smart_agri.db"


def get_connection():
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    return conn


# =========================
# INIT DB
# =========================
def init_db():
    conn = get_connection()
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS predictions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        n REAL,
        p REAL,
        k REAL,
        temperature REAL,
        humidity REAL,
        ph REAL,
        rainfall REAL,
        yield REAL,
        crop TEXT
    )
    """)

    conn.commit()
    conn.close()


# =========================
# SAVE
# =========================
def save_prediction(data):
    conn = get_connection()
    c = conn.cursor()

    c.execute("""
        INSERT INTO predictions (
            username, n, p, k,
            temperature, humidity, ph, rainfall,
            yield, crop
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, data)

    conn.commit()
    conn.close()


# =========================
# LOAD HISTORY
# =========================
def load_history():
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM predictions", conn)
    conn.close()
    return df