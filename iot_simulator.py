import random
import time

def generate_sensor_data():

    return {

        "N": random.randint(20, 120),
        "P": random.randint(20, 120),
        "K": random.randint(20, 180),

        "temperature": round(random.uniform(18, 40), 1),
        "humidity": round(random.uniform(30, 95), 1),
        "ph": round(random.uniform(5.0, 8.5), 1),
        "rainfall": round(random.uniform(50, 300), 1)

    }


# test loop
if __name__ == "__main__":

    while True:

        data = generate_sensor_data()

        print(data)

        time.sleep(2)