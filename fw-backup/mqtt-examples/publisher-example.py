import paho.mqtt.client as mqtt

broker = "localhost"
port = 1883
topic = "test/efraim11"

client = mqtt.Client(client_id="", protocol=mqtt.MQTTv5)

def on_connect(client, userdata, flags, reason_code, properties):
    print("Connected with result code " + str(reason_code))
    client.publish(topic, "Hello EFRAIM EFRAIM MQTT")

client.on_connect = on_connect

client.connect(broker, port, 60)
client.loop_forever()
