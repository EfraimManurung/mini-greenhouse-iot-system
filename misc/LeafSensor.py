'''
Author: Efraim Manurung
Information Technology Group, Wageningen University

efraim.manurung@gmail.com
'''

import serial
import time

class LeafSensor:
    def __init__(self, port='/dev/ttyUSB1', baudrate=9600):
        self.port = port
        self.baudrate = baudrate
        try:
            self.ser = serial.Serial(port, baudrate, timeout=1)
            self.ser.reset_input_buffer()
            print("LeafSensor Start!")
        except Exception as e:
            print(f"Error: Failed to initialize LeafSensor: {e}")
            self.ser = None

    def read_sensor_data(self):
        try:
            if self.ser is None:
                return None

            leaf_temp_value = None
            
            while True:
                if self.ser.in_waiting > 0:
                    line = self.ser.readline().decode('utf-8').strip()
                    
                    try:
                        # Check for the correct format and split the data
                        if line.startswith("leaf_temp:"):
                            leaf_temp_value = float(line.split(" ")[1].strip())
                    
                    except ValueError as e:
                        # Handle incorrect data formatting and log the issue
                        print(f"Data format error: {e}. Raw line: {line}")
                        continue

                    # If the value is valid (not None, 0, or 0.0), return it
                    if leaf_temp_value not in (None, 0, 0.0):
                        return leaf_temp_value

        except Exception as e:
            print(f"Error in reading sensor data: {e}")
            return None

    def average_sensor_data(self, _count, leaf_temp):
        try:
            # Ensure the temperature value is valid
            if leaf_temp is None:
                return None

            leaf_temp_total = 0

            for _ in range(_count):
                leaf_temp_total += leaf_temp
                time.sleep(0.2)

            averaged_leaf_temp = leaf_temp_total / _count

            print("AVERAGED VALUES from leaf sensor leaf temp={}".format(averaged_leaf_temp))

            return averaged_leaf_temp
        
        except Exception as e:
            print(f"Error in averaging sensor data: {e}")
            return None