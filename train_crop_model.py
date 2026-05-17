import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

# =========================
# LOAD DATASET
# =========================
df = pd.read_csv("crop_dataset.csv")

# =========================
# FEATURES & TARGET
# =========================
X = df.drop("label", axis=1)

y = df["label"]

# =========================
# SPLIT DATA
# =========================
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# =========================
# TRAIN MODEL
# =========================
model = RandomForestClassifier(
    n_estimators=200,
    random_state=42
)

model.fit(X_train, y_train)

# =========================
# EVALUATION
# =========================
predictions = model.predict(X_test)

accuracy = accuracy_score(y_test, predictions)

print(f"✅ Crop Recommendation Accuracy: {accuracy:.2f}")

# =========================
# SAVE MODEL
# =========================
joblib.dump(model, "crop_model.pkl")

print("✅ Crop Recommendation Model Saved")