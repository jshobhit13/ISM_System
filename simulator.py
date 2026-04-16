import random
import time
import requests
from datetime import datetime

API_URL = "http://127.0.0.1:5000/api/data"

SENSORS = [
    {"sensor_id": "TEMP-01",  "sensor_type": "temperature", "unit": "°C",    "base": 50,  "noise": 20},
    {"sensor_id": "TEMP-02",  "sensor_type": "temperature", "unit": "°C",    "base": 55,  "noise": 15},
    {"sensor_id": "PRES-01",  "sensor_type": "pressure",    "unit": "bar",   "base": 5.5, "noise": 3},
    {"sensor_id": "FLOW-01",  "sensor_type": "flow_rate",   "unit": "L/min", "base": 28,  "noise": 18},
]

def simulate_reading(sensor):
    """Add realistic noise + occasional spike to trigger alerts."""
    spike = random.random() < 0.05  # 5% chance of anomaly
    noise = random.uniform(-sensor["noise"], sensor["noise"])
    if spike:
        noise *= 2.5
    return round(sensor["base"] + noise, 2)

def main():
    print("Sensor simulator started. Press Ctrl+C to stop.\n")
    while True:
        for sensor in SENSORS:
            value = simulate_reading(sensor)
            payload = {
                "sensor_id":   sensor["sensor_id"],
                "sensor_type": sensor["sensor_type"],
                "value":       value,
                "unit":        sensor["unit"],
            }
            try:
                resp = requests.post(API_URL, json=payload, timeout=3)
                data = resp.json()
                alert_tag = " ⚠ ALERT" if data.get("alert") else ""
                print(f"[{datetime.now().strftime('%H:%M:%S')}] "
                      f"{sensor['sensor_id']:10s} {value:7.2f} {sensor['unit']}{alert_tag}")
            except requests.exceptions.ConnectionError:
                print("Flask server not running. Start app.py first.")
        time.sleep(3)  # Send readings every 3 seconds

if __name__ == "__main__":
    main()