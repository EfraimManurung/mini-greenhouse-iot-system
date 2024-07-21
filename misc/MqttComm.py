import numpy as np
import json

import paho.mqtt.client as mqtt

class MqttComm:
    def __init__(self):
        print(" MqttComm initiated!")
        
        # Initiate the MQTT client
        self.client = mqtt.Client()
    
    def format_data_in_JSON(self, time, ventilation, lamps, heater):
        '''
        Convert data to JSON format and print it.
        
        Parameters:
        - time: List of time values
        - ventilation: List of ventilation control values
        - lamps: List of lamps control values
        - heater: List of heater control values
        '''
        
        def convert_to_native(value):
            if isinstance(value, np.ndarray):
                return value.tolist()
            elif isinstance(value, (np.int32, np.int64, np.float32, np.float64)):
                return value.item()
            else:
                return value

        data = {
            "time": [convert_to_native(v) for v in time],
            "ventilation": [convert_to_native(v) for v in ventilation],
            "lamps": [convert_to_native(v) for v in lamps],
            "heater": [convert_to_native(v) for v in heater]
        }

        json_data = json.dumps(data, indent=4)
        print("JSON DATA: ", json_data)
        return json_data
    
    def publish_mqtt_data(self, json_data, broker="localhost", port=1883, topic="greenhouse/outdoor-measurements"):
        '''
        Publish JSON data to an MQTT broker.
        
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
