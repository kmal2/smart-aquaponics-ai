import streamlit as st
import pandas as pd
import joblib
import plotly.graph_objects as go
from streamlit_autorefresh import st_autorefresh

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Smart Aquaponics PRO",
    page_icon="🌱",
    layout="wide"
)

# =========================
# AUTO REFRESH (REAL TIME)
# =========================
st_autorefresh(interval=5000, key="refresh")

# =========================
# STYLE
# =========================
st.markdown("""
<style>
.main {
    background-color: #0e1117;
    color: white;
}

.block-container {
    padding: 2rem;
}

h1, h2, h3 {
    color: #00ffcc;
}
</style>
""", unsafe_allow_html=True)

# =========================
# HEADER
# =========================
st.markdown("<h1 style='text-align:center;'>🌱 Smart Aquaponics AI PRO</h1>", unsafe_allow_html=True)
st.caption("AI Prediction • IoT Simulation • Smart Monitoring System")

st.markdown("---")

# =========================
# LOAD MODELS (SAFE)
# =========================
@st.cache_resource
def load_models():
    yield_model = joblib.load("yield_model.pkl")
    risk_model = joblib.load("risk_model.pkl")
    return yield_model, risk_model

try:
    yield_model, risk_model = load_models()
except Exception as e:
    st.error("❌ Error loading models. Check .pkl files")
    st.stop()

# =========================
# SIDEBAR INPUTS
# =========================
st.sidebar.header("Sensor Inputs")

N = st.sidebar.slider("Nitrogen (N)", 0, 150, 90)
P = st.sidebar.slider("Phosphorus (P)", 0, 150, 42)
K = st.sidebar.slider("Potassium (K)", 0, 150, 43)

temperature = st.sidebar.slider("Temperature (°C)", 0.0, 50.0, 21.0)
humidity = st.sidebar.slider("Humidity (%)", 0.0, 100.0, 80.0)
ph = st.sidebar.slider("pH Level", 0.0, 14.0, 6.5)
rainfall = st.sidebar.slider("Rainfall (mm)", 0.0, 300.0, 200.0)

# =========================
# INPUT DATA
# =========================
data = pd.DataFrame([{
    "N": N,
    "P": P,
    "K": K,
    "temperature": temperature,
    "humidity": humidity,
    "ph": ph,
    "rainfall": rainfall
}])

# =========================
# PREDICTIONS
# =========================
yield_prediction = yield_model.predict(data)[0]
risk_prediction_raw = risk_model.predict(data)[0]

# FIX: Normalize risk output
if isinstance(risk_prediction_raw, (int, float)):
    if risk_prediction_raw == 2:
        risk_prediction = "High"
    elif risk_prediction_raw == 1:
        risk_prediction = "Medium"
    else:
        risk_prediction = "Low"
else:
    risk_prediction = str(risk_prediction_raw)

# =========================
# DASHBOARD METRICS
# =========================
col1, col2, col3 = st.columns(3)

col1.metric("🌱 Plant Health Score", f"{yield_prediction:.2f}/10")
col2.metric("⚠ Risk Level", risk_prediction)
col3.metric("📡 System Status", "ONLINE")

st.markdown("---")

# =========================
# GAUGE CHART
# =========================
fig = go.Figure(go.Indicator(
    mode="gauge+number",
    value=yield_prediction,
   title={'text': "Plant Health Score"},
    gauge={'axis': {'range': [0, max(10, float(yield_prediction) * 1.2)]}}
))

st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# =========================
# AI RECOMMENDATION
# =========================
st.subheader("🤖 AI Recommendation")

if risk_prediction == "High":
    st.error("🚨 HIGH RISK DETECTED")
    st.write("""
    - Reduce temperature immediately  
    - Adjust pH levels  
    - Increase oxygen supply  
    - Check system health urgently  
    """)

elif risk_prediction == "Medium":
    st.warning("⚠ MEDIUM RISK")
    st.write("""
    - Monitor humidity  
    - Stabilize environment  
    - Check nutrients  
    """)

else:
    st.success("✅ SYSTEM STABLE")
    st.write("""
    - All parameters normal  
    - System running efficiently  
    """)

st.markdown("---")

# =========================
# REAL-TIME MONITORING
# =========================
st.subheader("📊 Live Monitoring")

c1, c2, c3 = st.columns(3)

c1.metric("🌡 Temperature", f"{temperature} °C")
c2.metric("💧 Humidity", f"{humidity} %")
c3.metric("⚗ pH", ph)

# GAUGES
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
# LIVE DATA TABLE
# =========================
st.subheader("📋 System Data")

st.dataframe(pd.DataFrame({
    "N": [N],
    "P": [P],
    "K": [K],
    "Temperature": [temperature],
    "Humidity": [humidity],
    "pH": [ph],
    "Rainfall": [rainfall],
   "Plant Health Score": [yield_prediction],
    "Risk": [risk_prediction]
}), use_container_width=True)

st.markdown("---")

# =========================
# SMART ALERTS
# =========================
st.subheader("🚨 Smart Alerts System")

if risk_prediction == "High":
    st.markdown("""
    <div style="background:#ff4d4d;padding:15px;border-radius:10px;color:white;">
    🚨 CRITICAL ALERT - Immediate Action Required
    </div>
    """, unsafe_allow_html=True)

elif risk_prediction == "Medium":
    st.markdown("""
    <div style="background:#ff9800;padding:15px;border-radius:10px;color:white;">
    ⚠ WARNING - Monitor System Closely
    </div>
    """, unsafe_allow_html=True)

else:
    st.markdown("""
    <div style="background:#2ecc71;padding:15px;border-radius:10px;color:white;">
    ✅ SYSTEM HEALTHY
    </div>
    """, unsafe_allow_html=True)