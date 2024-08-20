import paho.mqtt.client as mqtt
import json

broker = "localhost"
port = 1883
topic = "greenhouse/drl-controls"

client = mqtt.Client(client_id="", protocol=mqtt.MQTTv5)

def on_connect(client, userdata, flags, reason_code, properties):
    print("Connected with result code " + str(reason_code))
    client.subscribe(topic)

def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload.decode()))
    # Parse the JSON data
    data = json.loads(msg.payload.decode())
    
    # Extract variables
    time = data.get("time", [])
    ventilation = data.get("ventilation", [])
    lamps = data.get("lamps", [])
    heater = data.get("heater", [])
    
    # Choose the first data point for each variable
    first_time = time[0] if time else None
    first_ventilation = ventilation[0] if ventilation else None
    first_lamps = lamps[0] if lamps else None
    first_heater = heater[0] if heater else None
    
    # Print the first data points
    print("First Time:", first_time)
    print("First Ventilation:", first_ventilation)
    print("First Lamps:", first_lamps)
    print("First Heater:", first_heater)

client.on_connect = on_connect
client.on_message = on_message

client.connect(broker, port, 60)
client.loop_forever()
