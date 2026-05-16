import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

# =========================
# Load Dataset
# =========================
df = pd.read_csv("aquaponics_crop_dataset.csv")

# =========================
# Features & Labels
# =========================
X = df.drop("label", axis=1)

y = df["label"]

# =========================
# Split Data
# =========================
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# =========================
# Train Model
# =========================
model = RandomForestClassifier(
    n_estimators=200,
    random_state=42
)

model.fit(X_train, y_train)

# =========================
# Accuracy
# =========================
predictions = model.predict(X_test)

accuracy = accuracy_score(y_test, predictions)

print(f"Crop Recommendation Accuracy: {accuracy:.2f}")

# =========================
# Save Model
# =========================
joblib.dump(model, "crop_recommendation_model.pkl")

print("Crop Recommendation Model Trained Successfully ✔")