from streamlit_autorefresh import st_autorefresh
import streamlit as st
import pandas as pd
import joblib
import plotly.graph_objects as go
import sqlite3
from datetime import datetime

# =========================
# APP CONFIG
# =========================
st.set_page_config(
    page_title="Aquaponics Startup Cloud V3",
    page_icon="🌱",
    layout="wide"
)

st.title("🌱 Aquaponics AI Startup Cloud System V3")
st_autorefresh(interval=5000, key="refresh")

st.markdown("---")

# =========================
# LOAD MODELS
# =========================
@st.cache_resource
def load_models():
    yield_model = joblib.load("yield_model.pkl")
    risk_model = joblib.load("risk_model.pkl")
    crop_model = joblib.load("crop_recommendation_model.pkl")
    return yield_model, risk_model, crop_model

yield_model, risk_model, crop_model = load_models()

# =========================
# CLOUD DATABASE (SQLite -> Cloud Ready)
# =========================
conn = sqlite3.connect("aquaponics_cloud.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS sensor_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT,
    N REAL,
    P REAL,
    K REAL,
    temperature REAL,
    humidity REAL,
    ph REAL,
    rainfall REAL,
    yield REAL,
    risk TEXT,
    crop TEXT
)
""")
conn.commit()

# =========================
# SIDEBAR INPUTS (IoT SIMULATION)
# =========================
st.sidebar.header("🌊 IoT Sensors")

N = st.sidebar.slider("Nitrogen (N)", 0, 150, 90)
P = st.sidebar.slider("Phosphorus (P)", 0, 150, 42)
K = st.sidebar.slider("Potassium (K)", 0, 150, 43)

temperature = st.sidebar.slider("Temperature", 0.0, 50.0, 21.0)
humidity = st.sidebar.slider("Humidity", 0.0, 100.0, 80.0)
ph = st.sidebar.slider("pH", 0.0, 14.0, 6.5)
rainfall = st.sidebar.slider("Rainfall", 0.0, 300.0, 200.0)

# =========================
# FEATURE ENGINEERING
# =========================
data = pd.DataFrame({
    "N": [N],
    "P": [P],
    "K": [K],
    "temperature": [temperature],
    "humidity": [humidity],
    "ph": [ph],
    "rainfall": [rainfall]
})

# =========================
# AI PREDICTIONS
# =========================
yield_prediction = yield_model.predict(data)[0]
risk_prediction = str(risk_model.predict(data)[0])
crop_prediction = str(crop_model.predict(data)[0])

# =========================
# SAVE TO CLOUD DB
# =========================
cursor.execute("""
INSERT INTO sensor_logs (
timestamp, N, P, K, temperature, humidity, ph, rainfall, yield, risk, crop
)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
""", (
datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
N, P, K, temperature, humidity, ph, rainfall,
float(yield_prediction),
risk_prediction,
crop_prediction
))

conn.commit()

# =========================
# LOAD HISTORY FROM CLOUD
# =========================
df = pd.read_sql("SELECT * FROM sensor_logs ORDER BY id DESC LIMIT 50", conn)

# =========================
# METRICS
# =========================
c1, c2, c3 = st.columns(3)

c1.metric("🌾 Yield", f"{yield_prediction:.2f}")
c2.metric("⚠ Risk", risk_prediction)
c3.metric("🌱 Crop", crop_prediction)

st.markdown("---")

# =========================
# GAUGE
# =========================
fig = go.Figure(go.Indicator(
    mode="gauge+number",
    value=yield_prediction,
    title={'text': "Yield Prediction"},
    gauge={'axis': {'range': [0, 10]}}
))

st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# =========================
# LIVE CLOUD DATA
# =========================
st.subheader("☁️ Cloud Sensor Database (Live)")

st.dataframe(df, use_container_width=True)

# =========================
# TREND ANALYSIS
# =========================
st.subheader("📈 Yield Trend (Cloud History)")

if len(df) > 1:
    st.line_chart(df["yield"])

st.markdown("---")

# =========================
# SMART ALERTS
# =========================
st.subheader("🚨 Smart Alerts")

if risk_prediction == "High":
    st.error("🚨 CRITICAL SYSTEM ALERT")
elif risk_prediction == "Medium":
    st.warning("⚠ SYSTEM WARNING")
else:
    st.success("✅ SYSTEM STABLE")

# =========================
# INSIGHT ENGINE
# =========================
st.subheader("🌱 AI Crop Insight")

st.success(f"""
Recommended Crop: {crop_prediction}

System stored in Cloud DB ✔
Total Records: {len(df)}
""")