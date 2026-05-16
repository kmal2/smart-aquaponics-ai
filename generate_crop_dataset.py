import pandas as pd
import random

data = []

crops = {

    "Lettuce": {
        "N": (80, 120),
        "P": (30, 60),
        "K": (30, 60),
        "temp": (18, 24),
        "humidity": (60, 80),
        "ph": (5.5, 6.5)
    },

    "Basil": {
        "N": (70, 110),
        "P": (25, 50),
        "K": (40, 70),
        "temp": (20, 30),
        "humidity": (50, 70),
        "ph": (5.5, 6.5)
    },

    "Mint": {
        "N": (60, 100),
        "P": (20, 50),
        "K": (30, 60),
        "temp": (18, 26),
        "humidity": (60, 85),
        "ph": (6.0, 7.0)
    },

    "Spinach": {
        "N": (90, 130),
        "P": (30, 60),
        "K": (40, 80),
        "temp": (15, 22),
        "humidity": (50, 70),
        "ph": (6.0, 7.5)
    },

    "Tomato": {
        "N": (50, 90),
        "P": (40, 80),
        "K": (60, 100),
        "temp": (22, 30),
        "humidity": (50, 70),
        "ph": (5.5, 6.8)
    },

    "Strawberry": {
        "N": (40, 80),
        "P": (30, 70),
        "K": (50, 90),
        "temp": (18, 26),
        "humidity": (60, 80),
        "ph": (5.5, 6.5)
    }
}

for crop, ranges in crops.items():

    for i in range(500):

        N = random.randint(*ranges["N"])
        P = random.randint(*ranges["P"])
        K = random.randint(*ranges["K"])

        temperature = round(random.uniform(*ranges["temp"]), 1)

        humidity = round(random.uniform(*ranges["humidity"]), 1)

        ph = round(random.uniform(*ranges["ph"]), 1)

        water_oxygen = round(random.uniform(5, 10), 1)

        water_temp = round(random.uniform(18, 28), 1)

        fish_density = round(random.uniform(0.5, 2.0), 1)

        data.append([
            N,
            P,
            K,
            temperature,
            humidity,
            ph,
            water_oxygen,
            water_temp,
            fish_density,
            crop
        ])

df = pd.DataFrame(data, columns=[
    "N",
    "P",
    "K",
    "temperature",
    "humidity",
    "ph",
    "water_oxygen",
    "water_temp",
    "fish_density",
    "label"
])

df.to_csv("aquaponics_crop_dataset.csv", index=False)

print("Advanced Aquaponics Dataset Generated Successfully ✔")