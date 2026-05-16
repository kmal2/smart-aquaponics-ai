import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import r2_score
from sklearn.metrics import accuracy_score

# =========================
# Load Dataset
# =========================
df = pd.read_csv("big_dataset.csv")

features = [
    "N",
    "P",
    "K",
    "temperature",
    "humidity",
    "ph",
    "rainfall"
]

X = df[features]

# =========================
# Yield Model
# =========================
y_yield = df["yield"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y_yield,
    test_size=0.2,
    random_state=42
)

yield_model = RandomForestRegressor(
    n_estimators=500,
    max_depth=20,
    random_state=42
)

yield_model.fit(X_train, y_train)

yield_predictions = yield_model.predict(X_test)

yield_score = r2_score(y_test, yield_predictions)

print("Yield R2 Score:", yield_score)

joblib.dump(yield_model, "yield_model.pkl")

# =========================
# Risk Model
# =========================
y_risk = df["risk"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y_risk,
    test_size=0.2,
    random_state=42
)

risk_model = RandomForestClassifier(
    n_estimators=500,
    max_depth=20,
    random_state=42
)

risk_model.fit(X_train, y_train)

risk_predictions = risk_model.predict(X_test)

risk_score = accuracy_score(y_test, risk_predictions)

print("Risk Accuracy:", risk_score)

joblib.dump(risk_model, "risk_model.pkl")

print("Advanced Models Trained Successfully ✔")