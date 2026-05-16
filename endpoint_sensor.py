import paho.mqtt.client as mqtt
import time
import random
import json

# Configuration
BROKER = "broker.hivemq.com"
PORT = 1883
STUDENT_ID = "104390459" 
TOPIC = f"{STUDENT_ID}/audit/logs/server-A"
STATUS_TOPIC = f"{STUDENT_ID}/audit/status/server-A" # NEW: Second topic for Gap 2
PUBLIC_TOPIC = "public" # NEW: Public topic for Gap 1

# Callback for when the client connects to the broker
def on_connect(client, userdata, flags, reason_code, properties=None):
    print(f"Connected to {BROKER} with code: {reason_code}")
    # NEW: Subscribe to public upon connection
    client.subscribe(PUBLIC_TOPIC) 

# NEW: Callback to print public messages
def on_message(client, userdata, msg):
    if msg.topic == PUBLIC_TOPIC:
        print(f"\n[PUBLIC BROADCAST] {msg.payload.decode('utf-8')}")

# Setup the MQTT Client
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message # NEW: Link the message callback

client.connect(BROKER, PORT, 60)
client.loop_start()

events = ["Successful Login", "Failed Login", "Privilege Escalation Attempt", "File Modified"]

print(f"Starting Endpoint Sensor.")
print(f"Publishing logs to: {TOPIC}")
print(f"Publishing status to: {STATUS_TOPIC}")

try:
    while True:
        # 1. Publish the regular audit log
        event_type = random.choice(events)
        ip_address = f"192.168.1.{random.randint(10, 50)}"
        
        payload_dict = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "event": event_type,
            "source_ip": ip_address
        }
        
        payload_string = json.dumps(payload_dict)
        print(f"Publishing Log: {payload_string}")
        client.publish(TOPIC, payload_string)
        
        # 2. Publish a simple status ping to a second topic (Satisfies Gap 2)
        client.publish(STATUS_TOPIC, "Status: Online")
        
        time.sleep(5) 

except KeyboardInterrupt:
    print("\nStopping sensor...")
    client.loop_stop()
    client.disconnect()