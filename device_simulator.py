import paho.mqtt.client as mqtt
import json
import time
from faker import Faker
import random

faker = Faker()

# MQTT Settings
MQTT_BROKER = "localhost"
MQTT_PORT = 1883
TOPIC = "medical/devices"

# Create MQTT client
client = mqtt.Client()
client.connect(MQTT_BROKER, MQTT_PORT, 60)

# Predefined device pool with stable IDs
DEVICE_POOL = {
    "Heart Monitor": 4,
    "Infusion Pump": 2,
    "ECG": 3,
    "Oxygen Sensor": 3,
    "Blood Pressure Monitor": 2
}

# Generate fixed devices and assign stable patient IDs
devices = []
for device_type, count in DEVICE_POOL.items():
    for _ in range(count):
        device_id = faker.uuid4()[:8]  # Shorter, stable ID
        patient_id = faker.random_int(min=1000, max=9999)  # Stable patient ID
        devices.append({
            "device_id": device_id,
            "device_type": device_type,
            "patient_id": patient_id
        })

# Device-specific value ranges
DEVICE_TYPES = {
    "Heart Monitor": {"min": 60, "max": 100, "unit": "bpm"},
    "Infusion Pump": {"min": 5, "max": 50, "unit": "ml/hr"},
    "ECG": {"min": 0.8, "max": 1.2, "unit": "mV"},
    "Oxygen Sensor": {"min": 90, "max": 100, "unit": "%SpO2"},
    "Blood Pressure Monitor": {"min": 90, "max": 140, "unit": "mmHg"}
}

def generate_fake_data(device):
    """Generate data for a specific predefined device."""
    value_range = DEVICE_TYPES[device["device_type"]]
    value = round(random.uniform(value_range["min"], value_range["max"]), 2)
    
    battery_status = random.randint(10, 100)  # Battery percentage
    alert_flag = "High" if value > value_range["max"] * 0.9 else "Normal"  

    return {
        "device_id": device["device_id"],
        "device_type": device["device_type"],
        "patient_id": device["patient_id"],
        "timestamp": faker.date_time_this_year().isoformat(),
        "value": value,
        "unit": value_range["unit"],
        "battery": f"{battery_status}%",
        "alert": alert_flag
    }

# Continuous data publishing loop
while True:
    for device in devices:
        fake_data = generate_fake_data(device)
        client.publish(TOPIC, json.dumps(fake_data))
        print(f"Sent: {fake_data}")
        time.sleep(random.uniform(1, 3))  # Simulate different transmission rates

