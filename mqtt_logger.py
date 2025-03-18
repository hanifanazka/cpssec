import paho.mqtt.client as mqtt
import json
import sqlite3

# Database setup
conn = sqlite3.connect("medical_logs.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        device_id TEXT,
        device_type TEXT,
        patient_id INTEGER,
        timestamp TEXT,
        value REAL
    )
""")
conn.commit()

# MQTT Settings
MQTT_BROKER = "localhost"
MQTT_PORT = 1883
TOPIC = "medical/devices"

# Define MQTT callbacks
def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker")
    client.subscribe(TOPIC)

def on_message(client, userdata, msg):
    data = json.loads(msg.payload)
    print(f"Received: {data}")
    
    cursor.execute("""
        INSERT INTO logs (device_id, device_type, patient_id, timestamp, value)
        VALUES (?, ?, ?, ?, ?)
    """, (data["device_id"], data["device_type"], data["patient_id"], data["timestamp"], data["value"]))
    conn.commit()

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.loop_forever()

