import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.metrics import accuracy_score, r2_score

# =====================
# Load dataset
# =====================
df = pd.read_csv("dataset.csv")

features = ["N","P","K","temperature","humidity","ph","rainfall"]

X = df[features]

# =====================
# Yield Model
# =====================
y_yield = df["yield"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y_yield, test_size=0.2, random_state=42
)

yield_model = RandomForestRegressor(
    n_estimators=200,
    random_state=42
)

yield_model.fit(X_train, y_train)

pred_yield = yield_model.predict(X_test)

print("Yield R2 Score:", r2_score(y_test, pred_yield))

joblib.dump(yield_model, "yield_model.pkl")

# =====================
# Risk Model
# =====================
y_risk = df["risk"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y_risk, test_size=0.2, random_state=42
)

risk_model = RandomForestClassifier(
    n_estimators=200,
    random_state=42
)

risk_model.fit(X_train, y_train)

pred_risk = risk_model.predict(X_test)

print("Risk Accuracy:", accuracy_score(y_test, pred_risk))

joblib.dump(risk_model, "risk_model.pkl")

print("Models trained successfully ✔")