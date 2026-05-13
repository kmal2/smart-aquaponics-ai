import requests
import random
import time

url = "http://127.0.0.1:5000/predict"

while True:

    data = {
        "N": random.randint(60, 100),
        "P": random.randint(30, 60),
        "K": random.randint(30, 60),
        "temperature": round(random.uniform(18, 35), 2),
        "humidity": round(random.uniform(60, 90), 2),
        "ph": round(random.uniform(5.5, 7.5), 2),
        "rainfall": random.randint(100, 300)
    }

    response = requests.post(url, json=data)

    print("Sent Data:", data)
    print("Response:", response.json())
    print("-" * 40)

    time.sleep(3600)  # Simulate hourly data generation