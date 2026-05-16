import paho.mqtt.client as mqtt
import json

# Configuration
BROKER = "broker.hivemq.com"
PORT = 1883
STUDENT_ID = "104390459" # Ensure this matches the other files!
SENSOR_TOPIC = f"{STUDENT_ID}/audit/logs/server-A"
COMMAND_TOPIC = f"{STUDENT_ID}/admin/access_control"

# Global variable to track suspicious activity
failed_login_count = 0
THRESHOLD = 3 # How many failed logins before we lock it down?

def on_connect(client, userdata, flags, reason_code, properties=None):
    print(f"Monitor Dashboard Online. Connected to {BROKER}")
    client.subscribe(SENSOR_TOPIC)
    print(f"Monitoring logs on: {SENSOR_TOPIC}")

def on_message(client, userdata, msg):
    global failed_login_count
    
    # Read the incoming log
    payload = msg.payload.decode("utf-8")
    
    try:
        # Convert the JSON string back into a Python dictionary
        log_data = json.loads(payload)
        event_type = log_data.get("event")
        source_ip = log_data.get("source_ip")
        
        print(f"[LOG DETECTED] {log_data['timestamp']} | {event_type} | IP: {source_ip}")
        
        # --- THE HIGH DISTINCTION AUTOMATION LOGIC ---
        if event_type == "Failed Login":
            failed_login_count += 1
            print(f"  ⚠️ Warning: Failed login count is now {failed_login_count}/{THRESHOLD}")
            
            if failed_login_count >= THRESHOLD:
                print("\n🚨 THRESHOLD REACHED! INITIATING AUTOMATED LOCKDOWN 🚨")
                
                # Craft the automated command
                action_message = f"LOCKDOWN TRIGGERED: Blocked IP {source_ip} after {THRESHOLD} failed attempts."
                
                # Publish the command to the Access Controller
                client.publish(COMMAND_TOPIC, action_message)
                
                # Reset the counter after lockdown
                failed_login_count = 0 
                
    except json.JSONDecodeError:
        print("Received malformed log data.")

# Setup the MQTT Client
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER, PORT, 60)
client.loop_forever()