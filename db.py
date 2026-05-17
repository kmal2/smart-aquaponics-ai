import sqlite3
import pandas as pd

# =========================
# CONNECT DATABASE
# =========================
def get_connection():
    conn = sqlite3.connect("aquaponics.db", check_same_thread=False)
    return conn

# =========================
# CREATE TABLE
# =========================
def init_db():
    conn = get_connection()
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS predictions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        n REAL,
        p REAL,
        k REAL,
        temperature REAL,
        humidity REAL,
        ph REAL,
        rainfall REAL,
        yield REAL,
        crop TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()

# =========================
# INSERT DATA
# =========================
def save_prediction(data):
    conn = get_connection()
    c = conn.cursor()

    c.execute("""
    INSERT INTO predictions (
        n, p, k, temperature, humidity, ph, rainfall, yield, crop
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, data)

    conn.commit()
    conn.close()

# =========================
# LOAD HISTORY
# =========================
def load_history():
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM predictions ORDER BY id DESC", conn)
    conn.close()
    return df