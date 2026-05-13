import sqlite3
from flask import Flask, request, jsonify
import pandas as pd
import joblib
import sqlite3
from datetime import datetime

app = Flask(__name__)

# =========================
# Load Models
# =========================
yield_model = joblib.load("yield_model.pkl")
risk_model = joblib.load("risk_model.pkl")

# =========================
# Create Database
# =========================
conn = sqlite3.connect("aquaponics.db", check_same_thread=False)

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS sensor_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    N REAL,
    P REAL,
    K REAL,
    temperature REAL,
    humidity REAL,
    ph REAL,
    rainfall REAL,
    yield_prediction REAL,
    risk_prediction TEXT,
    timestamp TEXT
)
""")

conn.commit()

# =========================
# Prediction API
# =========================
@app.route("/predict", methods=["POST"])
def predict():

    data = request.json

    df = pd.DataFrame({
        "N": [data["N"]],
        "P": [data["P"]],
        "K": [data["K"]],
        "temperature": [data["temperature"]],
        "humidity": [data["humidity"]],
        "ph": [data["ph"]],
        "rainfall": [data["rainfall"]]
    })

    # Predictions
    yield_prediction = float(yield_model.predict(df)[0])
    risk_prediction = str(risk_model.predict(df)[0])

    # Save to database
    cursor.execute("""
    INSERT INTO sensor_data (
        N, P, K, temperature, humidity, ph, rainfall,
        yield_prediction, risk_prediction, timestamp
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data["N"],
        data["P"],
        data["K"],
        data["temperature"],
        data["humidity"],
        data["ph"],
        data["rainfall"],
        yield_prediction,
        risk_prediction,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()

    return jsonify({
        "yield_prediction": yield_prediction,
        "risk_prediction": risk_prediction
    })

# =========================
# Run App
# =========================
if __name__ == "__main__":
    app.run(debug=True)
    # =========================
# Database Connection
# =========================
conn = sqlite3.connect("aquaponics.db")

# Load data
history_df = pd.read_sql_query(
    "SELECT * FROM sensor_data ORDER BY id DESC",
    conn
)

# =========================
# Show Database Table
# =========================
st.subheader("📊 Sensor History")

st.dataframe(history_df)

# =========================
# Temperature Chart
# =========================
st.subheader("🌡 Temperature History")

st.line_chart(history_df["temperature"])

# =========================
# Humidity Chart
# =========================
st.subheader("💧 Humidity History")

st.line_chart(history_df["humidity"])

# =========================
# Yield Chart
# =========================
st.subheader("🌾 Yield Prediction History")

st.line_chart(history_df["yield_prediction"])