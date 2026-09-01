import numpy as np
import requests
from datetime import datetime


def get_nasa_data():
    url = "https://nasa-public-data.s3.amazonaws.com/iss-coords/current/ISS_OEM/ISS.OEM_J2K_EPH.txt"
    response = requests.get(url)

    lines = response.text.splitlines()

    flight_data = {}
    for line in lines:
        data = line.split()
        if len(data) != 7:
            continue
        try:
            epoch = datetime.fromisoformat(data[0])
            pos_vel = [float(value) for value in data[1:]]
            pos_vel = np.array(pos_vel) * 1000
            flight_data[epoch] = pos_vel
        except ValueError:
            continue

    states = np.array(list(flight_data.values()))

    return states
