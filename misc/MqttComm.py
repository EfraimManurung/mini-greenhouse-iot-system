'''
mini-greenhouse-iot-system
Author: Efraim Manurung
MSc Thesis in Information Technology Group, Wageningen University

 
efraim.manurung@gmail.com

MqttComm for the IoT sytem
'''
import numpy as np
import json

import paho.mqtt.client as mqtt

class MqttComm:
    def __init__(self):
        print("MqttComm Start!")
        
        # Initiate the MQTT client for publishing data
        self.client_pub = mqtt.Client()
        
        # Initialize the MQTT client for subscribing data
        self.client_sub = mqtt.Client(client_id="", protocol=mqtt.MQTTv5)
        
        self.message_received = False  # Initialize message_received flag
        self.received_data = None # To store received data
    
    def format_data_in_JSON(self, time, par_out, par_in, temp_out, temp_in, hum_out, hum_in, co2_out, co2_in, leaf_temp):
        '''
        Convert data to JSON format and print it.
        
        Outdoor measurements:
        - time: from main loop iteration in 1 s
        - lux: Need to be converted to W / m^2
        - temperature
        - humidity
        - co2
        - leaf temperature
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
            "par_out": [convert_to_native(v) for v in par_out],
            "par_in": [convert_to_native(v) for v in par_in],
            "temp_out": [convert_to_native(v) for v in temp_out],
            "temp_in": [convert_to_native(v) for v in temp_in],
            "hum_out": [convert_to_native(v) for v in hum_out],
            "hum_in": [convert_to_native(v) for v in hum_in],
            "co2_out": [convert_to_native(v) for v in co2_out],
            "co2_in": [convert_to_native(v) for v in co2_in],
            "leaf_temp": [convert_to_native(v) for v in leaf_temp]
        }

        json_data = json.dumps(data, indent=4)
        # print("JSON DATA: ", json_data)
        return json_data
    
    def publish_mqtt_data(self, json_data, broker="localhost", port=1883, topic="greenhouse-iot-system/outdoor-indoor-measurements"):
        '''
        Publish JSON data to a MQTT broker.
        
        Parameters:
        - json_data: JSON formatted data to publish
        - broker: MQTT broker address
        - port: MQTT broker port
        - topic: MQTT topic to publish data to
        '''
        
        def on_connect(client, userdata, flags, rc):
            print("Connected with result code PUBLISH MQTT " + str(rc))
            client.publish(topic, str(json_data))
        
        self.client_pub.on_connect = on_connect
        
        self.client_pub.connect(broker, port, 60)
        self.client_pub.loop_start()

    def subscribe_mqtt_data(self, broker="localhost", port=1883, topic="greenhouse-iot-system/drl-controls"):
        '''
        Subscribe JSON data from a MQTT broker.
        
        Parameters:
        - json_data: JSON formatted data to publish
        - broker: MQTT broker address
        - port: MQTT broker port
        - topic: MQTT topic to publish data to
        '''
        
        def on_connect(client, userdata, flags, reason_code, properties):
            print("Connected with result code SUBSCRIBE MQTT " + str(reason_code))
            client.subscribe(topic)
            
        def on_message(client, userdata, msg):
            # print(msg.topic + " " + str(msg.payload.decode()))
            # Parse the JSON data
            data = json.loads(msg.payload.decode())
            
            # Process the received data
            self.received_data = self.process_received_data(data) 
        
            # Set the flag to indicate a message was received
            self.message_received = True
            self.client_sub.loop_stop()  # Stop the loop
    
        self.message_received = False # Reset message_received flag
        self.client_sub.on_connect = on_connect
        self.client_sub.on_message = on_message

        self.client_sub.connect(broker, port, 60)
        self.client_sub.loop_start()  # Start the loop in a separate thread
    
        # Wait for a message to be received
        while not self.message_received:
            continue
        
        self.client_sub.loop_stop()  # Ensure the loop is stopped
        self.client_sub.disconnect()  # Disconnect the client
        
        # return True
        return self.received_data
        
    def process_received_data(self, data):
        '''
        Process the controls from the PC server.
        
        Controls:
        
        action (discrete integer):
        -  u1(t) Fan (-)                       0-1 (1 is fully open) 
        -  u2(t) Toplighting status (-)        0/1 (1 is on)
        -  u3(t) Heating (-)                   0/1 (1 is on)
        '''
        
        # Extract variables
        time = data.get("time", [])
        ventilation = data.get("ventilation", [])
        toplights = data.get("toplights", [])
        heater = data.get("heater", [])
        
        return time, ventilation, toplights, heater
    