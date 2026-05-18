import pandas as pd
import random

data = []

for i in range(5000):

    # =========================
    # RANDOM INPUTS
    # =========================
    N = random.randint(0, 140)

    P = random.randint(0, 145)

    K = random.randint(0, 205)

    temperature = round(random.uniform(10, 45), 1)

    humidity = round(random.uniform(20, 100), 1)

    ph = round(random.uniform(4, 9), 1)

    rainfall = round(random.uniform(20, 300), 1)

    # =========================
    # HEALTH LOGIC
    # =========================
    if (
        6 <= ph <= 7.5 and
        20 <= temperature <= 30 and
        humidity >= 50 and
        N >= 40 and
        P >= 40 and
        K >= 40
    ):

        health = "Healthy"

    elif (
        ph < 5.5 or
        ph > 8 or
        temperature > 38 or
        temperature < 15
    ):

        health = "Dangerous"

    else:

        health = "Warning"

    # =========================
    # SAVE ROW
    # =========================
    data.append([

        N,
        P,
        K,

        temperature,
        humidity,
        ph,
        rainfall,

        health

    ])

# =========================
# DATAFRAME
# =========================
df = pd.DataFrame(data, columns=[

    "N",
    "P",
    "K",

    "temperature",
    "humidity",
    "ph",
    "rainfall",

    "health"

])

# =========================
# SAVE CSV
# =========================
df.to_csv("health_dataset.csv", index=False)

print("✅ health_dataset.csv generated successfully")