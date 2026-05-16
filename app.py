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
st.markdown("""
<style>
    .main {
        background-color: #0e1117;
    }
    h1 {
        color: #00ffcc;
    }
    .stMetric {
        background-color: #1c1f26;
        padding: 10px;
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)
st.markdown("<h1 style='text-align:center;'>🌱 Smart Aquaponics AI Platform</h1>", unsafe_allow_html=True)
st.caption("Smart Farming • AI Prediction • Real-Time IoT Monitoring")
st_autorefresh(interval=5000, key="datarefresh")

st.markdown("---")

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

# تأكيد أن risk string
risk_prediction = str(risk_prediction)

# =========================
# Metrics
# =========================
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 🌾 Yield")
    st.markdown(f"<h2 style='color:#00ffcc'>{yield_prediction:.2f} Ton</h2>", unsafe_allow_html=True)

with col2:
    st.markdown("### ⚠ Risk")
    color = "red" if risk_prediction == "High" else "orange" if risk_prediction == "Medium" else "lightgreen"
    st.markdown(f"<h2 style='color:{color}'>{risk_prediction}</h2>", unsafe_allow_html=True)

with col3:
    st.markdown("### 📡 System")
    st.markdown("<h2 style='color:#00ffcc'>ACTIVE</h2>", unsafe_allow_html=True)

# =========================
# Gauge Chart (Yield)
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
# AI Recommendation
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

st.markdown("---")

# =========================
# Real-Time Monitoring
# =========================
st.subheader("📊 Real-Time Sensor Monitoring")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("🌡 Temperature", f"{temperature} °C")

with col2:
    st.metric("💧 Humidity", f"{humidity} %")

with col3:
    st.metric("⚗ pH Level", ph)

# Gauges
temp_fig = go.Figure(go.Indicator(
    mode="gauge+number",
    value=temperature,
    title={'text': "Temperature"},
    gauge={'axis': {'range': [0, 50]}}
))

hum_fig = go.Figure(go.Indicator(
    mode="gauge+number",
    value=humidity,
    title={'text': "Humidity"},
    gauge={'axis': {'range': [0, 100]}}
))

ph_fig = go.Figure(go.Indicator(
    mode="gauge+number",
    value=ph,
    title={'text': "pH Level"},
    gauge={'axis': {'range': [0, 14]}}
))

col1, col2, col3 = st.columns(3)

with col1:
    st.plotly_chart(temp_fig, use_container_width=True)

with col2:
    st.plotly_chart(hum_fig, use_container_width=True)

with col3:
    st.plotly_chart(ph_fig, use_container_width=True)

st.markdown("---")

# =========================
# Live Table
# =========================
st.subheader("📋 Real-Time Sensor Data")

sensor_df = pd.DataFrame({
    "Temperature": [temperature],
    "Humidity": [humidity],
    "pH": [ph],
    "Rainfall": [rainfall],
    "Yield Prediction": [yield_prediction],
    "Risk Level": [risk_prediction]
})

st.dataframe(sensor_df, use_container_width=True)

st.markdown("---")

# =========================
# Smart Alerts System
# =========================
st.subheader("🚨 Smart Alerts System")

if risk_prediction == "High":

    st.markdown("""
    <div style="background-color:#ff4d4d;padding:15px;border-radius:10px;color:white;">
        <h3>🚨 CRITICAL ALERT!</h3>
        <p>Immediate Actions Required:</p>
        <ul>
            <li>🔴 Adjust water pH immediately</li>
            <li>🔴 Increase oxygen supply</li>
            <li>🔴 Reduce temperature</li>
            <li>🔴 Check system urgently</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

elif risk_prediction == "Medium":

    st.markdown("""
    <div style="background-color:#ff9800;padding:15px;border-radius:10px;color:white;">
        <h3>⚠ WARNING ALERT</h3>
        <p>Recommended Monitoring:</p>
        <ul>
            <li>🟠 Monitor humidity closely</li>
            <li>🟠 Check nutrient balance</li>
            <li>🟠 Observe system stability</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

else:

    st.markdown("""
    <div style="background-color:#2ecc71;padding:15px;border-radius:10px;color:white;">
        <h3>✅ SYSTEM STABLE</h3>
        <p>All parameters are normal</p>
        <ul>
            <li>🟢 No immediate action required</li>
            <li>🟢 System running optimally</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)