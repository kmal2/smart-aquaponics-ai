from auth import init_users, register_user, login_user
from db import init_db, save_prediction, load_history

import streamlit as st
import pandas as pd
import joblib
import plotly.graph_objects as go
import os

from iot_simulator import generate_sensor_data
from streamlit_autorefresh import st_autorefresh


# =========================
# INIT
# =========================
init_db()
init_users()

# =========================
# PAGE CONFIG
# =========================
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

    required_files = [
        "yield_model.pkl",
        "crop_model.pkl",
        "health_model.pkl"
    ]

    for f in required_files:
        if not os.path.exists(f):
            st.error(f"❌ Missing model file: {f}")
            st.stop()

    yield_model = joblib.load("yield_model.pkl")
    crop_model = joblib.load("crop_model.pkl")
    health_model = joblib.load("health_model.pkl")

    return yield_model, crop_model, health_model


yield_model, crop_model, health_model = load_models()


# =========================
# LOGIN SYSTEM
# =========================
if "user" not in st.session_state:

    st.title("🔐 Smart Aquaponics Login System")

    choice = st.radio("Choose Option", ["Login", "Register"])

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if choice == "Register":
        if st.button("Create Account"):
            if register_user(username, password):
                st.success("✅ Account Created Successfully")
            else:
                st.error("❌ Username already exists")

    if choice == "Login":
        if st.button("Login"):
            user = login_user(username, password)

            if user:
                st.session_state["user"] = username
                st.success("✅ Login Successful")
                st.rerun()
            else:
                st.error("❌ Invalid Credentials")

    st.stop()


# =========================
# SIDEBAR
# =========================
st.sidebar.success(f"👤 Logged in as: {st.session_state['user']}")
st.sidebar.title("🌱 Smart Aquaponics AI")


# =========================
# LIVE MODE
# =========================
if "live" not in st.session_state:
    st.session_state["live"] = False

if st.sidebar.button("🔴 Toggle Live IoT Mode"):
    st.session_state["live"] = not st.session_state["live"]

if st.session_state["live"]:
    st.sidebar.success("🔴 LIVE MODE ACTIVE")
    st_autorefresh(interval=3000, key="live_refresh")


# =========================
# STORE LAST RESULT
# =========================
if "last_result" not in st.session_state:
    st.session_state["last_result"] = None


# =========================
# TITLE
# =========================
st.title("🌱💧 Smart Aquaponics Monitoring System")
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

    st.info("🔴 LIVE IoT SENSOR MODE ACTIVE")

else:

    st.sidebar.header("🌿 Manual Inputs")

    N = st.sidebar.slider("Nitrogen (N)", 0, 140, 50)
    P = st.sidebar.slider("Phosphorus (P)", 0, 145, 50)
    K = st.sidebar.slider("Potassium (K)", 0, 205, 50)

    temperature = st.sidebar.slider("Temperature (°C)", 0.0, 50.0, 25.0)
    humidity = st.sidebar.slider("Humidity (%)", 0.0, 100.0, 60.0)
    ph = st.sidebar.slider("Water pH", 0.0, 14.0, 6.5)
    rainfall = st.sidebar.slider("Water Flow", 0.0, 500.0, 100.0)


# =========================
# INPUT DATA
# =========================
input_data = pd.DataFrame({
    "N": [N],
    "P": [P],
    "K": [K],
    "temperature": [temperature],
    "humidity": [humidity],
    "ph": [ph],
    "rainfall": [rainfall]
})

try:
    input_data = input_data[yield_model.feature_names_in_]
except:
    pass


# =========================
# PREDICTION
# =========================
if st.button("🚀 Run Smart AI Analysis"):

    try:
        yield_prediction = yield_model.predict(input_data)[0]
        crop_prediction = crop_model.predict(input_data)[0]
        health_prediction = health_model.predict(input_data)[0]

        # =========================
        # ML HEALTH MAPPING
        # =========================
        if health_prediction == "Healthy":
            health_score = 90
        elif health_prediction == "Warning":
            health_score = 60
        else:
            health_score = 20

        # =========================
        # SAVE TO DB
        # =========================
        save_prediction((
            st.session_state["user"],
            N, P, K,
            temperature,
            humidity,
            ph,
            rainfall,
            float(yield_prediction),
            str(crop_prediction),
            int(health_score),
            health_prediction
        ))

        # =========================
        # STORE RESULT
        # =========================
        st.session_state["last_result"] = {
            "yield": float(yield_prediction),
            "crop": str(crop_prediction),
            "health": health_prediction,
            "score": int(health_score)
        }

    except Exception as e:
        st.error(f"Error: {e}")


# =========================
# DISPLAY RESULTS + ANALYSIS
# =========================
if st.session_state["last_result"] is not None:

    r = st.session_state["last_result"]

    st.subheader("🌱 AI Results")

    c1, c2 = st.columns(2)
    c1.metric("🌾 Yield", f"{r['yield']:.2f}")
    c2.metric("🌱 Crop", r["crop"])

    st.metric("🧠 Health Status", r["health"])
    st.metric("💚 Health Score", f"{r['score']}/100")

    st.markdown("---")

    # =========================
    # 💧 WATER ANALYSIS
    # =========================
    water_status = (
        "Good 🟢" if 6 <= ph <= 7.5
        else "Moderate 🟡" if 5 <= ph < 6 or 7.5 < ph <= 8
        else "Danger 🔴"
    )

    # =========================
    # 🐟 FISH ANALYSIS
    # =========================
    fish_status = (
        "Safe 🟢" if 20 <= temperature <= 30
        else "Warning 🟡" if 15 <= temperature < 20 or 30 < temperature <= 35
        else "Critical 🔴"
    )

    # =========================
    # 🌱 PLANT ANALYSIS
    # =========================
    plant_status = (
        "Healthy 🟢" if r["score"] >= 80
        else "Moderate 🟡" if r["score"] >= 50
        else "Poor 🔴"
    )

    # =========================
    # 🚨 SYSTEM RISK
    # =========================
    def risk(x):
        return {"Low 🟢": 1, "Medium 🟡": 2, "High 🔴": 3}.get(x.split()[0] + " " + x.split()[1], 2)

    total_risk = (
        risk(water_status) +
        risk(fish_status) +
        risk(plant_status)
    )

    system_status = (
        "Excellent 🟢" if total_risk <= 3
        else "Stable 🟡" if total_risk <= 5
        else "Critical 🔴"
    )

    # =========================
    # DISPLAY ANALYSIS
    # =========================
    st.subheader("🧠 Smart Analysis")

    s1, s2, s3 = st.columns(3)

    s1.metric("💧 Water", water_status)
    s2.metric("🐟 Fish", fish_status)
    s3.metric("🌱 Plant", plant_status)

    st.metric("🚨 System Status", system_status)


# =========================
# HISTORY
# =========================
st.markdown("---")
st.subheader("📊 History")

try:
    history = load_history()

    if history is not None and not history.empty:
        user_history = history[history["username"] == st.session_state["user"]]
        st.dataframe(user_history, use_container_width=True)
    else:
        st.info("No history yet")

except Exception as e:
    st.warning(f"History error: {e}")