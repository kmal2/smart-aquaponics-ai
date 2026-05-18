from auth import init_users, register_user, login_user
from db import init_db, save_prediction, load_history

import streamlit as st
import pandas as pd
import joblib
import plotly.graph_objects as go
import plotly.express as px
import os

from iot_simulator import generate_sensor_data
from streamlit_autorefresh import st_autorefresh


# =========================
# INIT
# =========================
init_db()
init_users()

st.set_page_config(
    page_title="Smart Aquaponics AI",
    page_icon="🌱",
    layout="wide"
)


# =========================
# LOAD MODELS
# =========================
@st.cache_resource
def load_models():
    return (
        joblib.load("yield_model.pkl"),
        joblib.load("crop_model.pkl"),
        joblib.load("health_model.pkl"),
    )

yield_model, crop_model, health_model = load_models()


# =========================
# LOGIN
# =========================
if "user" not in st.session_state:

    st.title("🔐 Smart Aquaponics Login")

    mode = st.radio("Choose", ["Login", "Register"])
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if mode == "Register" and st.button("Create Account"):
        if register_user(username, password):
            st.success("Account Created")
        else:
            st.error("User exists")

    if mode == "Login" and st.button("Login"):
        user = login_user(username, password)
        if user:
            st.session_state["user"] = username
            st.rerun()
        else:
            st.error("Invalid login")

    st.stop()


# =========================
# SIDEBAR
# =========================
st.sidebar.success(f"👤 Logged in as: {st.session_state['user']}")
st.sidebar.title("🌱 Smart Aquaponics AI")

if "live" not in st.session_state:
    st.session_state["live"] = False

if st.sidebar.button("🔴 Toggle Live Mode"):
    st.session_state["live"] = not st.session_state["live"]

if st.session_state["live"]:
    st_autorefresh(interval=3000, key="refresh")
    st.sidebar.success("LIVE MODE 🔴")


# =========================
# TITLE
# =========================
st.title("🌱💧 Smart Aquaponics FULL Dashboard")
st.markdown("---")


# =========================
# INPUTS
# =========================
if st.session_state["live"]:
    sensor = generate_sensor_data()

    N = sensor["N"]
    P = sensor["P"]
    K = sensor["K"]
    temperature = sensor["temperature"]
    humidity = sensor["humidity"]
    ph = sensor["ph"]
    rainfall = sensor["rainfall"]

    st.info("🔴 LIVE IoT ACTIVE")

else:
    st.sidebar.header("Inputs")

    N = st.sidebar.slider("N", 0, 140, 50)
    P = st.sidebar.slider("P", 0, 145, 50)
    K = st.sidebar.slider("K", 0, 205, 50)

    temperature = st.sidebar.slider("Temp", 0.0, 50.0, 25.0)
    humidity = st.sidebar.slider("Humidity", 0.0, 100.0, 60.0)
    ph = st.sidebar.slider("pH", 0.0, 14.0, 6.5)
    rainfall = st.sidebar.slider("Rain", 0.0, 500.0, 100.0)


# =========================
# DATA
# =========================
input_data = pd.DataFrame([{
    "N": N,
    "P": P,
    "K": K,
    "temperature": temperature,
    "humidity": humidity,
    "ph": ph,
    "rainfall": rainfall
}])

try:
    input_data = input_data[yield_model.feature_names_in_]
except:
    pass


# =========================
# PREDICT
# =========================
if st.button("🚀 Run AI Analysis"):

    yield_pred = float(yield_model.predict(input_data)[0])
    crop_pred = crop_model.predict(input_data)[0]
    health_pred = health_model.predict(input_data)[0]

    # =========================
    # SMART LOGIC
    # =========================
    if health_pred == "Healthy":
        score = 90
        fish = "Safe 🐟"
        water = "Good 💧"
    elif health_pred == "Warning":
        score = 60
        fish = "Risk ⚠"
        water = "Medium 💧"
    else:
        score = 25
        fish = "Danger 🚨"
        water = "Bad 💧"

    plant = "Healthy 🌱" if score > 80 else "Moderate ⚠" if score > 50 else "Poor 🚨"
    risk = "Low 🟢" if score == 90 else "Medium 🟡" if score == 60 else "High 🔴"

    # SAVE DB
    save_prediction((
        st.session_state["user"],
        N, P, K,
        temperature, humidity, ph, rainfall,
        yield_pred,
        str(crop_pred),
        score,
        risk
    ))

    # STORE RESULT
    st.session_state["result"] = {
        "yield": yield_pred,
        "crop": crop_pred,
        "health": health_pred,
        "score": score,
        "risk": risk,
        "fish": fish,
        "water": water,
        "plant": plant
    }


# =========================
# RESULT DISPLAY (IMPORTANT FIX)
# =========================
if "result" in st.session_state and st.session_state["result"]:

    r = st.session_state["result"]

    st.markdown("## 🌱 Full System Analysis")

    # =========================
    # MAIN METRICS
    # =========================
    col1, col2 = st.columns(2)
    col1.metric("🌾 Yield", f"{r['yield']:.2f}")
    col2.metric("🌱 Crop", r["crop"])

    st.metric("🧠 Health Status", r["health"])
    st.metric("💚 Score", f"{r['score']}/100")
    st.metric("⚠ Risk", r["risk"])

    st.markdown("---")

    # =========================
    # ENVIRONMENT STATUS
    # =========================
    c1, c2, c3 = st.columns(3)
    c1.metric("💧 Water Status", r["water"])
    c2.metric("🐟 Fish Status", r["fish"])
    c3.metric("🌱 Plant Status", r["plant"])

    st.markdown("---")

    # =========================
    # GAUGE CHART
    # =========================
    fig = go.Figure()

    fig.add_trace(go.Indicator(
        mode="gauge+number",
        value=r["yield"],
        title={"text": "🌾 Yield Prediction"},
        gauge={
            "axis": {"range": [0, max(10, r["yield"] + 2)]},
            "bar": {"color": "green"},
            "steps": [
                {"range": [0, 3], "color": "red"},
                {"range": [3, 7], "color": "yellow"},
                {"range": [7, 10], "color": "lightgreen"},
            ],
        }
    ))

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")


# =========================
# HISTORY + ANALYTICS
# =========================
history = load_history()

if history is not None and not history.empty:

    user_history = history[history["username"] == st.session_state["user"]]

    st.markdown("## 📊 Analytics Dashboard")

    # Yield Trend
    st.subheader("🌾 Yield Trend")
    st.plotly_chart(px.line(user_history, y="yield", title="Yield Over Time"), use_container_width=True)

    # Risk Pie (FIXED COLUMN NAME)
    st.subheader("⚠ Risk Distribution")
    st.plotly_chart(px.pie(user_history, names="risk_level", title="Risk Levels"), use_container_width=True)

    # Crop Distribution
    st.subheader("🌱 Crop Analysis")
    st.plotly_chart(px.histogram(user_history, x="crop", title="Crop Distribution"), use_container_width=True)

    # FULL TABLE
    st.subheader("📋 Full History")
    st.dataframe(user_history, use_container_width=True)

else:
    st.info("No history yet")