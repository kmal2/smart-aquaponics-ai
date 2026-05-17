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
# LOAD MODELS
# =========================
@st.cache_resource
def load_models():
    yield_model = joblib.load("yield_model.pkl")
    crop_model = joblib.load("crop_model.pkl")
    return yield_model, crop_model

yield_model, crop_model = load_models()

# =========================
# TITLE
# =========================
st.title("🌱 Smart Agriculture AI System")

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
# DATAFRAME (SAME FEATURES FOR YIELD MODEL)
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
# PREDICTION BUTTON
# =========================
if st.button("🚀 Predict AI Results"):

    try:
        # =========================
        # PREDICTIONS
        # =========================
        yield_prediction = yield_model.predict(input_data)[0]
        crop_prediction = crop_model.predict(input_data)[0]

        # =========================
        # METRICS
        # =========================
        c1, c2 = st.columns(2)

        c1.metric("🌾 Yield Prediction", f"{yield_prediction:.2f}")
        c2.metric("🌱 Recommended Crop", crop_prediction)

        st.markdown("---")

        # =========================
        # GAUGE
        # =========================
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=float(yield_prediction),
            title={'text': "Yield Prediction"},
            gauge={'axis': {'range': [0, 10]}}
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

        if yield_prediction >= 7:
            st.success("✅ Excellent conditions for high productivity")

        elif yield_prediction >= 4:
            st.warning("⚠ Moderate productivity")

        else:
            st.error("🚨 Low productivity - Improve conditions")

    except Exception as e:
        st.error(f"❌ Error: {e}")

# =========================
# MODEL INFO
# =========================
st.markdown("---")

st.subheader("🧠 Model Features")

try:
    st.write(list(yield_model.feature_names_in_))
except:
    st.write("Feature names not available")