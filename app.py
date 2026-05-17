import streamlit as st
import pandas as pd
import joblib
import plotly.graph_objects as go

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Smart Agriculture AI",
    page_icon="🌱",
    layout="wide"
)

# =========================
# LOAD MODEL
# =========================
@st.cache_resource
def load_model():
    return joblib.load("yield_model.pkl")

yield_model = load_model()

# =========================
# TITLE
# =========================
st.title("🌱 Smart Agriculture Yield Prediction")

st.markdown("""
AI-powered system for predicting crop yield based on:

- Soil Nutrients (NPK)
- Temperature
- Humidity
- pH
- Rainfall
""")

st.markdown("---")

# =========================
# SIDEBAR INPUTS
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
# DATAFRAME
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
# PREDICTION
# =========================
if st.button("🚀 Predict Yield"):

    try:
        prediction = yield_model.predict(input_data)[0]

        # =========================
        # METRICS
        # =========================
        c1, c2, c3 = st.columns(3)

        c1.metric("🌾 Yield Prediction", f"{prediction:.2f}")

        c2.metric("🌡 Temperature", f"{temperature} °C")

        c3.metric("💧 Humidity", f"{humidity}%")

        st.markdown("---")

        # =========================
        # GAUGE CHART
        # =========================
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=float(prediction),
            title={'text': "Predicted Yield"},
            gauge={
                'axis': {'range': [0, 10]}
            }
        ))

        st.plotly_chart(fig, use_container_width=True)

        st.markdown("---")

        # =========================
        # INPUT TABLE
        # =========================
        st.subheader("📊 Input Data")

        st.dataframe(input_data, use_container_width=True)

        st.markdown("---")

        # =========================
        # AI ANALYSIS
        # =========================
        st.subheader("🤖 AI Analysis")

        if prediction >= 7:
            st.success("✅ Excellent conditions for high crop productivity.")

        elif prediction >= 4:
            st.warning("⚠ Moderate productivity expected.")

        else:
            st.error("🚨 Low productivity predicted. Improve soil or climate conditions.")

    except Exception as e:
        st.error(f"❌ Prediction Error: {e}")

# =========================
# MODEL FEATURES
# =========================
st.markdown("---")

st.subheader("🧠 Model Features")

try:
    features = list(yield_model.feature_names_in_)
    st.write(features)

except:
    st.warning("Feature names are not available in this model.")