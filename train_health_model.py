import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib

# =========================
# LOAD DATASET
# =========================
df = pd.read_csv("health_dataset.csv")

# =========================
# FEATURES / LABEL
# =========================
X = df.drop("health", axis=1)
y = df["health"]

# =========================
# TRAIN / TEST SPLIT
# =========================
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42
)

# =========================
# MODEL
# =========================
model = RandomForestClassifier(
    n_estimators=200,
    random_state=42
)

model.fit(X_train, y_train)

# =========================
# ACCURACY
# =========================
accuracy = model.score(X_test, y_test)
print(f"✅ Model Accuracy: {accuracy:.2f}")

# =========================
# SAVE MODEL
# =========================
joblib.dump(model, "health_model.pkl")

print("✅ health_model.pkl saved successfully")