from streamlit_autorefresh import st_autorefresh
import streamlit as st
import pandas as pd
import joblib
import plotly.graph_objects as go

# =========================
# Load Models
# =========================
yield_model = joblib.load("yield_model.pkl")
risk_model = joblib.load("risk_model.pkl")

# =========================
# Page Config
# =========================
st.set_page_config(
    page_title="Smart Aquaponics AI",
    page_icon="🌱",
    layout="wide"
)

st.title("🌱 Smart Aquaponics AI Dashboard")
st_autorefresh(interval=5000, key="datarefresh")
st.write("Real-Time Monitoring & Prediction System")

# =========================
# Sidebar Inputs
# =========================
st.sidebar.header("Sensor Inputs")

N = st.sidebar.slider("Nitrogen (N)", 0, 150, 90)
P = st.sidebar.slider("Phosphorus (P)", 0, 150, 42)
K = st.sidebar.slider("Potassium (K)", 0, 150, 43)

temperature = st.sidebar.slider("Temperature", 0.0, 50.0, 21.0)
humidity = st.sidebar.slider("Humidity", 0.0, 100.0, 80.0)
ph = st.sidebar.slider("pH", 0.0, 14.0, 6.5)
rainfall = st.sidebar.slider("Rainfall", 0.0, 300.0, 200.0)

# =========================
# Prediction
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

yield_prediction = yield_model.predict(data)[0]
risk_prediction = risk_model.predict(data)[0]

# =========================
# Metrics
# =========================
col1, col2 = st.columns(2)

with col1:
    st.metric("Predicted Yield", f"{yield_prediction:.2f} Ton")

with col2:
    st.metric("Risk Level", risk_prediction)

# =========================
# Gauge Chart
# =========================
fig = go.Figure(go.Indicator(
    mode="gauge+number",
    value=yield_prediction,
    title={'text': "Yield Prediction"},
    gauge={
        'axis': {'range': [0, 10]}
    }
))

st.plotly_chart(fig, use_container_width=True)

# =========================
# Recommendations
# =========================
st.subheader("AI Recommendation")

if risk_prediction == "High":

    st.error("⚠ High Risk Detected!")

    st.write("### Recommended Actions:")
    st.write("- Reduce water temperature")
    st.write("- Adjust pH levels immediately")
    st.write("- Increase oxygen supply")
    st.write("- Check nutrient balance")

elif risk_prediction == "Medium":

    st.warning("⚠ Medium Risk")

    st.write("### Recommended Actions:")
    st.write("- Monitor humidity regularly")
    st.write("- Keep water quality stable")
    st.write("- Observe plant health closely")

else:

    st.success("✅ System Status is Good")

    st.write("### System Analysis:")
    st.write("- Water conditions are stable")
    st.write("- Nutrient levels are balanced")
    st.write("- Environment is suitable for growth")
    st.subheader("Live Temperature Monitoring")

import plotly.graph_objects as go

fig = go.Figure(go.Indicator(
    mode="gauge+number",
    value=temperature,
    title={'text': "Temperature °C"},
    gauge={
        'axis': {'range': [0, 50]}
    }
))

st.plotly_chart(fig)