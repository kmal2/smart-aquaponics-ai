import pandas as pd
import random

data = []

for i in range(1000):

    N = random.randint(50, 120)
    P = random.randint(20, 80)
    K = random.randint(20, 80)

    temperature = round(random.uniform(18, 35), 2)
    humidity = round(random.uniform(50, 90), 2)
    ph = round(random.uniform(5.5, 7.5), 2)
    rainfall = random.randint(80, 300)

    # Yield logic
    yield_value = round(
        (N + P + K) / 60 +
        (humidity / 100) +
        (rainfall / 200),
        2
    )

    # Risk logic
    if ph < 5.8 or ph > 7.2 or temperature > 32:
        risk = "High"
    elif temperature > 28:
        risk = "Medium"
    else:
        risk = "Low"

    data.append([
        N, P, K,
        temperature,
        humidity,
        ph,
        rainfall,
        yield_value,
        risk
    ])

df = pd.DataFrame(data, columns=[
    "N","P","K",
    "temperature",
    "humidity",
    "ph",
    "rainfall",
    "yield",
    "risk"
])

df.to_csv("big_dataset.csv", index=False)

print("Dataset Generated Successfully ✔")