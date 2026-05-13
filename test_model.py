import joblib
import pandas as pd

# Load models
yield_model = joblib.load("yield_model.pkl")
risk_model = joblib.load("risk_model.pkl")

# Example input
data = {
    "N": [90],
    "P": [42],
    "K": [43],
    "temperature": [21],
    "humidity": [80],
    "ph": [6.5],
    "rainfall": [200]
}

df = pd.DataFrame(data)

# Predictions
yield_prediction = yield_model.predict(df)
risk_prediction = risk_model.predict(df)

print("Predicted Yield:", yield_prediction[0])
print("Predicted Risk:", risk_prediction[0])