import paho.mqtt.client as mqtt

# Configuration
BROKER = "192.168.12.100"
PORT = 1883
STUDENT_ID = "104390459" 
COMMAND_TOPIC = f"{STUDENT_ID}/admin/access_control"
PUBLIC_TOPIC = "public"

# Callback for when the client connects to the broker
def on_connect(client, userdata, flags, reason_code, properties=None):
    print(f"Connected to {BROKER} with code: {reason_code}")
    
    # Subscribe to the required topics
    client.subscribe(COMMAND_TOPIC)
    client.subscribe(PUBLIC_TOPIC)
    print(f"Listening on: \n - {COMMAND_TOPIC}\n - {PUBLIC_TOPIC}")

# Callback for when a PUBLISH message is received from the server
def on_message(client, userdata, msg):
    topic = msg.topic
    # Decode the payload from bytes to a standard string
    payload = msg.payload.decode("utf-8") 
    
    print("\n--- Incoming Transmission ---")
    print(f"Topic:   {topic}")
    
    # If the message is a direct command, execute the fake action
    if topic == COMMAND_TOPIC:
        print(f" ACTION REQUIRED: {payload} ")
    elif topic == PUBLIC_TOPIC:
        print(f"Broadcast: {payload}")

# Setup the MQTT Client
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

print("Booting Access Controller...")
client.connect(BROKER, PORT, 60)

# loop_forever() blocks the program and keeps it listening indefinitely
client.loop_forever()