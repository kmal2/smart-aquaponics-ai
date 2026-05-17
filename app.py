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

    st.title("🔐 Smart Agriculture Login System")

    choice = st.radio("Choose Option", ["Login", "Register"])

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if choice == "Register":
        if st.button("Create Account"):
            if register_user(username, password):
                st.success("Account Created 🚀")
            else:
                st.error("Username already exists")

    if choice == "Login":
        if st.button("Login"):
            user = login_user(username, password)
            if user:
                st.session_state["user"] = username
                st.success("Login Successful 🚀")
                st.rerun()
            else:
                st.error("Invalid Credentials")

    st.stop()


# =========================
# UI
# =========================
st.sidebar.success(f"Logged in as: {st.session_state['user']}")

st.title("🌱 Smart Agriculture AI System")
st.markdown("---")


# =========================
# INPUTS
# =========================
st.sidebar.header("🌿 Input Parameters")

N = st.sidebar.slider("Nitrogen (N)", 0, 140, 50)
P = st.sidebar.slider("Phosphorus (P)", 0, 145, 50)
K = st.sidebar.slider("Potassium (K)", 0, 205, 50)

temperature = st.sidebar.slider("Temperature (°C)", 0.0, 50.0, 25.0)
humidity = st.sidebar.slider("Humidity (%)", 0.0, 100.0, 60.0)
ph = st.sidebar.slider("Soil pH", 0.0, 14.0, 6.5)
rainfall = st.sidebar.slider("Rainfall (mm)", 0.0, 500.0, 100.0)


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


# =========================
# FIX FEATURE ORDER (VERY IMPORTANT)
# =========================
try:
    input_data = input_data[yield_model.feature_names_in_]
except:
    pass


# =========================
# PREDICTION
# =========================
if st.button("🚀 Predict AI Results"):

    try:
        yield_prediction = yield_model.predict(input_data)[0]
        crop_prediction = crop_model.predict(input_data)[0]

        # SAVE
        save_prediction((
            st.session_state["user"],
            N, P, K,
            temperature,
            humidity,
            ph,
            rainfall,
            float(yield_prediction),
            str(crop_prediction)
        ))

        # RESULTS
        c1, c2 = st.columns(2)
        c1.metric("🌾 Yield", f"{yield_prediction:.2f}")
        c2.metric("🌱 Crop", crop_prediction)

        # GAUGE
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=float(yield_prediction),
            title={'text': "Yield Prediction"},
            gauge={'axis': {'range': [0, 10]}}
        ))

        st.plotly_chart(fig, use_container_width=True)

        # ANALYSIS
        if yield_prediction >= 7:
            st.success("Excellent conditions 🌟")
        elif yield_prediction >= 4:
            st.warning("Moderate conditions ⚠")
        else:
            st.error("Poor conditions 🚨")

    except Exception as e:
        st.error(f"Error: {e}")


# =========================
# HISTORY
# =========================
st.markdown("---")
st.subheader("📊 Your History")

try:
    history = load_history()

    if history is not None and not history.empty:
        user_history = history[history["username"] == st.session_state["user"]]
        st.dataframe(user_history, use_container_width=True)
    else:
        st.info("No history yet")

except Exception as e:
    st.warning(f"History error: {e}")