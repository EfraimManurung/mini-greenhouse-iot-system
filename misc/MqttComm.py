import numpy as np
import json

import paho.mqtt.client as mqtt

class MqttComm:
    def __init__(self):
        print("MqttComm Start!")
        
        # Initiate the MQTT client
        self.client = mqtt.Client()
    
    def format_data_in_JSON(self, time, lux, temperature, humidity, co2):
        '''
        Convert data to JSON format and print it.
        
        Outdoor measurements:
        - time: from main loop iteration in 1 s
        - lux: Need to be converted to W / m^2
        - temperature
        - humidity
        - co2
        '''
        
        def convert_to_native(value):
            if isinstance(value, np.ndarray):
                return value.tolist()
            elif isinstance(value, (np.int32, np.int64, np.float32, np.float64)):
                return value.item()
            else:
                return value

        # Max steps for 20 minutes
        # max_steps = 4
        
        # time_max = (self.max_steps + 1) * 900 # for e.g. 4 steps * 900 (15 minutes) = 60 minutes
        # time_steps_seconds = np.linspace(300, time_max, (self.max_steps + 1) * 3)  # Time steps in seconds
        # time_max = self.max_steps * 900 # for e.g. 4 steps * 900 (15 minutes) = 60 minutes
        # time_steps_seconds = np.linspace(300, time_max, self.max_steps  * 3)  # Time steps in seconds
        
        data = {
            "time": [convert_to_native(v) for v in time],
            "lux": [convert_to_native(v) for v in lux],
            "temperature": [convert_to_native(v) for v in temperature],
            "humidity": [convert_to_native(v) for v in humidity],
            "co2": [convert_to_native(v) for v in co2]
        }

        json_data = json.dumps(data, indent=4)
        print("JSON DATA: ", json_data)
        return json_data
    
    def publish_mqtt_data(self, json_data, broker="localhost", port=1883, topic="greenhouse/outdoor-measurements"):
        '''
        Publish JSON data to a MQTT broker.
        
        Parameters:
        - json_data: JSON formatted data to publish
        - broker: MQTT broker address
        - port: MQTT broker port
        - topic: MQTT topic to publish data to
        '''
        
        def on_connect(client, userdata, flags, rc):
            print("Connected with result code " + str(rc))
            client.publish(topic, str(json_data))
        
        self.client.on_connect = on_connect
        
        self.client.connect(broker, port, 60)
        self.client.loop_start()
