from auth import init_users, register_user, login_user
from db import init_db, save_prediction, load_history
import streamlit as st
import pandas as pd
import joblib
import plotly.graph_objects as go
import os

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
# LOAD MODELS SAFELY
# =========================
@st.cache_resource
def load_models():

    if not os.path.exists("yield_model.pkl") or not os.path.exists("crop_model.pkl"):
        st.error("❌ Model files missing (.pkl)")
        st.stop()

    yield_model = joblib.load("yield_model.pkl")
    crop_model = joblib.load("crop_model.pkl")

    return yield_model, crop_model


yield_model, crop_model = load_models()

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

st.sidebar.markdown("---")

# =========================
# MAIN TITLE
# =========================
st.title("🌱💧 Smart Aquaponics Monitoring System")

st.markdown("""
AI-powered aquaponics monitoring and decision support system.
""")

st.markdown("---")

# =========================
# INPUTS
# =========================
st.sidebar.header("🌿 Water & Environment Inputs")

N = st.sidebar.slider("Nitrogen (N)", 0, 140, 50)

P = st.sidebar.slider("Phosphorus (P)", 0, 145, 50)

K = st.sidebar.slider("Potassium (K)", 0, 205, 50)

temperature = st.sidebar.slider(
    "Water Temperature (°C)",
    0.0,
    50.0,
    25.0
)

humidity = st.sidebar.slider(
    "Humidity (%)",
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
    "Water Flow / Rainfall",
    0.0,
    500.0,
    100.0
)

# =========================
# INPUT DATAFRAME
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

# =========================
# FIX FEATURE ORDER
# =========================
try:
    input_data = input_data[yield_model.feature_names_in_]

except:
    pass

# =========================
# PREDICTION BUTTON
# =========================
if st.button("🚀 Run Smart AI Analysis"):

    try:

        # =========================
        # MODEL PREDICTIONS
        # =========================
        yield_prediction = yield_model.predict(input_data)[0]

        crop_prediction = crop_model.predict(input_data)[0]

        # =========================
        # HEALTH + RISK SYSTEM
        # =========================
        if yield_prediction >= 7:

            health_score = 90
            risk_level = "Low 🟢"

        elif yield_prediction >= 4:

            health_score = 60
            risk_level = "Medium 🟡"

        else:

            health_score = 30
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

            float(yield_prediction),

            str(crop_prediction),

            int(health_score),

            risk_level

        ))

        # =========================
        # RESULTS
        # =========================
        st.subheader("🌱 Prediction Results")

        c1, c2 = st.columns(2)

        c1.metric(
            "🌾 Predicted Yield",
            f"{yield_prediction:.2f}"
        )

        c2.metric(
            "🌱 Recommended Crop",
            crop_prediction
        )

        st.markdown("---")

        c3, c4 = st.columns(2)

        c3.metric(
            "💚 Health Score",
            f"{health_score}/100"
        )

        c4.metric(
            "⚠ Risk Level",
            risk_level
        )

        # =========================
        # YIELD GAUGE
        # =========================
        fig = go.Figure(go.Indicator(

            mode="gauge+number",

            value=float(yield_prediction),

            title={'text': "Yield Prediction"},

            gauge={
                'axis': {'range': [0, 10]}
            }

        ))

        st.plotly_chart(fig, use_container_width=True)

        # =========================
        # HEALTH GAUGE
        # =========================
        fig2 = go.Figure(go.Indicator(

            mode="gauge+number",

            value=health_score,

            title={'text': "System Health"},

            gauge={
                'axis': {'range': [0, 100]}
            }

        ))

        st.plotly_chart(fig2, use_container_width=True)

        # =========================
        # SMART ANALYSIS SYSTEM
        # =========================
        st.markdown("---")

        st.subheader("🧠 Smart System Analysis")

        # =========================
        # WATER QUALITY
        # =========================
        if 6 <= ph <= 7.5:
            water_status = "Good 🟢"

        else:
            water_status = "Danger ⚠"

        # =========================
        # FISH SAFETY
        # =========================
        if 20 <= temperature <= 30:
            fish_status = "Safe 🐟"

        else:
            fish_status = "Risk 🚨"

        # =========================
        # PLANT HEALTH
        # =========================
        if health_score >= 80:
            plant_status = "Healthy 🌱"

        elif health_score >= 50:
            plant_status = "Moderate ⚠"

        else:
            plant_status = "Poor 🚨"

        # =========================
        # STATUS CARDS
        # =========================
        s1, s2, s3 = st.columns(3)

        s1.metric(
            "💧 Water Quality",
            water_status
        )

        s2.metric(
            "🐟 Fish Safety",
            fish_status
        )

        s3.metric(
            "🌱 Plant Health",
            plant_status
        )

        # =========================
        # ALERTS
        # =========================
        st.markdown("---")

        st.subheader("🚨 Smart Alerts")

        if ph < 6:

            st.error("🚨 Water is too acidic")

        elif ph > 7.5:

            st.error("🚨 Water pH is too high")

        if temperature > 35:

            st.warning("⚠ High water temperature detected")

        if health_score < 50:

            st.error("🚨 Plant health is critical")

        # =========================
        # RECOMMENDATIONS
        # =========================
        st.markdown("---")

        st.subheader("💡 AI Recommendations")

        if ph < 6:

            st.info("💡 Add alkaline buffer to increase pH")

        if ph > 7.5:

            st.info("💡 Reduce pH gradually using safe treatment")

        if temperature > 35:

            st.info("💡 Cool the water or reduce sunlight exposure")

        if health_score < 50:

            st.info("💡 Check nutrients and oxygen levels")

        # =========================
        # OVERALL ANALYSIS
        # =========================
        st.markdown("---")

        if yield_prediction >= 7:

            st.success("🌟 Excellent aquaponics conditions detected")

        elif yield_prediction >= 4:

            st.warning("⚠ Moderate system conditions")

        else:

            st.error("🚨 Poor system conditions detected")

    except Exception as e:

        st.error(f"❌ Error: {e}")

# =========================
# HISTORY
# =========================
st.markdown("---")

st.subheader("📊 Prediction History")

try:

    history = load_history()

    if history is not None and not history.empty:

        user_history = history[
            history["username"] == st.session_state["user"]
        ]

        st.dataframe(
            user_history,
            use_container_width=True
        )

    else:

        st.info("No history yet")

except Exception as e:

    st.warning(f"History error: {e}")