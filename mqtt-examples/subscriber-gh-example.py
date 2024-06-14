import paho.mqtt.client as mqtt

broker = "localhost"
port = 1883
topic = "greenhouse/drl-controls"

client = mqtt.Client(client_id="", protocol=mqtt.MQTTv5)

def on_connect(client, userdata, flags, reason_code, properties):
    print("Connected with result code " + str(reason_code))
    client.subscribe(topic)

def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload.decode()))

client.on_connect = on_connect
client.on_message = on_message

client.connect(broker, port, 60)
client.loop_forever()
