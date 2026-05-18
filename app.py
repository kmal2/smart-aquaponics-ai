from auth import init_users, register_user, login_user
from db import init_db, save_prediction, load_history

import streamlit as st
import pandas as pd
import joblib
import plotly.graph_objects as go
import plotly.express as px

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

    yield_model = joblib.load("yield_model.pkl")
    crop_model = joblib.load("crop_model.pkl")
    health_model = joblib.load("health_model.pkl")

    return yield_model, crop_model, health_model


yield_model, crop_model, health_model = load_models()


# =========================
# LOGIN SYSTEM
# =========================
if "user" not in st.session_state:

    st.title("🔐 Smart Aquaponics Login")

    mode = st.radio("Choose", ["Login", "Register"])

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    # REGISTER
    if mode == "Register":

        if st.button("Create Account"):

            if register_user(username, password):
                st.success("✅ Account Created Successfully")

            else:
                st.error("❌ Username already exists")

    # LOGIN
    if mode == "Login":

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

if st.sidebar.button("🔴 Toggle Live Mode"):
    st.session_state["live"] = not st.session_state["live"]

if st.session_state["live"]:
    st.sidebar.success("🔴 LIVE MODE ACTIVE")

    st_autorefresh(
        interval=3000,
        key="live_refresh"
    )


# =========================
# SAVE LAST RESULT
# =========================
if "result" not in st.session_state:
    st.session_state["result"] = None


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

    st.info("🔴 LIVE IoT SENSOR MODE ACTIVE")

else:

    st.sidebar.header("🌿 Inputs")

    N = st.sidebar.slider("Nitrogen (N)", 0, 140, 50)
    P = st.sidebar.slider("Phosphorus (P)", 0, 145, 50)
    K = st.sidebar.slider("Potassium (K)", 0, 205, 50)

    temperature = st.sidebar.slider(
        "Temperature",
        0.0,
        50.0,
        25.0
    )

    humidity = st.sidebar.slider(
        "Humidity",
        0.0,
        100.0,
        60.0
    )

    ph = st.sidebar.slider(
        "Water pH",
        0.0,
        14.0,
        6.5
    )

    rainfall = st.sidebar.slider(
        "Water Flow",
        0.0,
        500.0,
        100.0
    )


# =========================
# INPUT DATA
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


# =========================
# FIX FEATURE ORDER
# =========================
try:
    input_data = input_data[yield_model.feature_names_in_]

except:
    pass


# =========================
# RUN AI
# =========================
if st.button("🚀 Run Smart AI Analysis"):

    try:

        # =========================
        # PREDICTIONS
        # =========================
        yield_prediction = float(
            yield_model.predict(input_data)[0]
        )

        crop_prediction = crop_model.predict(input_data)[0]

        health_prediction = health_model.predict(input_data)[0]

        # =========================
        # SMART ANALYSIS
        # =========================
        if health_prediction == "Healthy":

            health_score = 90

            fish_status = "Safe 🐟"
            water_status = "Good 💧"

        elif health_prediction == "Warning":

            health_score = 60

            fish_status = "Risk ⚠"
            water_status = "Medium 💧"

        else:

            health_score = 25

            fish_status = "Danger 🚨"
            water_status = "Bad 💧"

        # =========================
        # PLANT STATUS
        # =========================
        if health_score >= 80:
            plant_status = "Healthy 🌱"

        elif health_score >= 50:
            plant_status = "Moderate ⚠"

        else:
            plant_status = "Poor 🚨"

        # =========================
        # RISK LEVEL
        # =========================
        if health_score >= 80:
            risk_level = "Low 🟢"

        elif health_score >= 50:
            risk_level = "Medium 🟡"

        else:
            risk_level = "High 🔴"

        # =========================
        # SAVE TO DATABASE
        # =========================
        save_prediction((
            st.session_state["user"],

            N,
            P,
            K,

            temperature,
            humidity,
            ph,
            rainfall,

            yield_prediction,
            str(crop_prediction),

            health_score,
            risk_level
        ))

        # =========================
        # SAVE RESULT
        # =========================
        st.session_state["result"] = {

            "yield": yield_prediction,
            "crop": crop_prediction,

            "health": health_prediction,
            "score": health_score,

            "risk": risk_level,

            "fish": fish_status,
            "water": water_status,
            "plant": plant_status
        }

    except Exception as e:

        st.error(f"Error: {e}")


# =========================
# DISPLAY RESULT
# =========================
if st.session_state["result"] is not None:

    r = st.session_state["result"]

    st.markdown("## 🌱 Full System Analysis")

    # =========================
    # MAIN METRICS
    # =========================
    col1, col2 = st.columns(2)

    col1.metric(
        "🌾 Yield Prediction",
        f"{r['yield']:.2f}"
    )

    col2.metric(
        "🌱 Recommended Crop",
        r["crop"]
    )

    st.metric(
        "🧠 AI Health Status",
        r["health"]
    )

    st.metric(
        "💚 Health Score",
        f"{r['score']}/100"
    )

    st.metric(
        "⚠ Risk Level",
        r["risk"]
    )

    st.markdown("---")

    # =========================
    # SMART SYSTEM ANALYSIS
    # =========================
    st.subheader("🧠 Smart System Analysis")

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "💧 Water Status",
        r["water"]
    )

    c2.metric(
        "🐟 Fish Status",
        r["fish"]
    )

    c3.metric(
        "🌱 Plant Status",
        r["plant"]
    )

    st.markdown("---")

    # =========================
    # ALERTS
    # =========================
    st.subheader("🚨 Alerts")

    alerts = []

    if r["score"] < 50:
        alerts.append("⚠ Low plant health detected")

    if r["risk"] == "High 🔴":
        alerts.append("🚨 High system risk detected")

    if "Danger" in r["fish"]:
        alerts.append("🐟 Fish environment is dangerous")

    if len(alerts) == 0:
        st.success("✅ System Stable - No Alerts")

    else:
        for alert in alerts:
            st.error(alert)

    st.markdown("---")

    # =========================
    # RECOMMENDATIONS
    # =========================
    st.subheader("💡 Recommendations")

    if r["risk"] == "Low 🟢":

        st.success("System conditions are optimal")

    elif r["risk"] == "Medium 🟡":

        st.warning("Monitor water quality regularly")

    else:

        st.error("Immediate maintenance required")

        st.info("Check nutrients and oxygen levels")
        st.info("Check water temperature")
        st.info("Check fish environment")

    st.markdown("---")

    # =========================
    # GAUGE CHART
    # =========================
    fig = go.Figure(go.Indicator(

        mode="gauge+number",

        value=r["yield"],

        title={
            "text": "🌾 Yield Prediction"
        },

        gauge={

            "axis": {
                "range": [0, max(10, r["yield"] + 2)]
            },

            "bar": {
                "color": "green"
            },

            "steps": [

                {
                    "range": [0, 3],
                    "color": "red"
                },

                {
                    "range": [3, 7],
                    "color": "yellow"
                },

                {
                    "range": [7, 10],
                    "color": "lightgreen"
                },
            ],
        }
    ))

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# =========================
# HISTORY + ANALYTICS
# =========================
history = load_history()

if history is not None and not history.empty:

    user_history = history[
        history["username"] == st.session_state["user"]
    ]

    if not user_history.empty:

        st.markdown("---")
        st.markdown("## 📊 Analytics Dashboard")

        # =========================
        # YIELD TREND
        # =========================
        st.subheader("🌾 Yield Trend")

        fig1 = px.line(
            user_history,
            y="yield",
            title="Yield Over Time"
        )

        st.plotly_chart(
            fig1,
            use_container_width=True
        )

        # =========================
        # RISK DISTRIBUTION
        # =========================
        st.subheader("⚠ Risk Distribution")

        risk_data = (
            user_history["risk_level"]
            .value_counts()
            .reset_index()
        )

        risk_data.columns = [
            "risk_level",
            "count"
        ]

        fig2 = px.pie(
            risk_data,
            names="risk_level",
            values="count",
            title="Risk Levels"
        )

        st.plotly_chart(
            fig2,
            use_container_width=True
        )

        # =========================
        # CROP ANALYSIS
        # =========================
        st.subheader("🌱 Crop Analysis")

        fig3 = px.histogram(
            user_history,
            x="crop",
            title="Crop Distribution"
        )

        st.plotly_chart(
            fig3,
            use_container_width=True
        )

        # =========================
        # HEALTH SCORE TREND
        # =========================
        st.subheader("💚 Health Score Trend")

        fig4 = px.line(
            user_history,
            y="health_score",
            title="Health Score Over Time"
        )

        st.plotly_chart(
            fig4,
            use_container_width=True
        )

        # =========================
        # FULL HISTORY TABLE
        # =========================
        st.subheader("📋 Full History")

        st.dataframe(
            user_history,
            use_container_width=True
        )

    else:
        st.info("No user history found")

else:
    st.info("No history available yet")