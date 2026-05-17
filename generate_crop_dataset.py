import pandas as pd
import random

data = []

# =========================
# RICE
# =========================
for _ in range(500):
    data.append([
        random.randint(80, 120),
        random.randint(35, 60),
        random.randint(35, 60),
        random.uniform(20, 35),
        random.uniform(80, 100),
        random.uniform(5.0, 7.0),
        random.uniform(200, 300),
        "Rice"
    ])

# =========================
# WHEAT
# =========================
for _ in range(500):
    data.append([
        random.randint(60, 100),
        random.randint(30, 50),
        random.randint(30, 50),
        random.uniform(15, 25),
        random.uniform(40, 60),
        random.uniform(6.0, 7.5),
        random.uniform(50, 100),
        "Wheat"
    ])

# =========================
# MAIZE
# =========================
for _ in range(500):
    data.append([
        random.randint(70, 110),
        random.randint(40, 60),
        random.randint(35, 60),
        random.uniform(18, 30),
        random.uniform(50, 70),
        random.uniform(5.5, 7.0),
        random.uniform(60, 120),
        "Maize"
    ])

# =========================
# COTTON
# =========================
for _ in range(500):
    data.append([
        random.randint(50, 90),
        random.randint(25, 45),
        random.randint(25, 45),
        random.uniform(25, 40),
        random.uniform(40, 60),
        random.uniform(5.5, 8.0),
        random.uniform(30, 80),
        "Cotton"
    ])

# =========================
# POTATO
# =========================
for _ in range(500):
    data.append([
        random.randint(40, 80),
        random.randint(40, 60),
        random.randint(40, 70),
        random.uniform(10, 25),
        random.uniform(60, 80),
        random.uniform(5.0, 6.5),
        random.uniform(70, 150),
        "Potato"
    ])

# =========================
# CREATE DATAFRAME
# =========================
df = pd.DataFrame(data, columns=[
    "N",
    "P",
    "K",
    "temperature",
    "humidity",
    "ph",
    "rainfall",
    "label"
])

# =========================
# SAVE CSV
# =========================
df.to_csv("crop_dataset.csv", index=False)

print("✅ Advanced Crop Dataset Generated")