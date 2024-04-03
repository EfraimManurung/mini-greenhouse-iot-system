''' 
Complete Project Details: https://RandomNerdTutorials.com/raspberry-pi-ds18b20-python/
Based on the Adafruit example: https://github.com/adafruit/Adafruit_Learning_System_Guides/blob/main/Raspberry_Pi_DS18B20_Temperature_Sensing/code.py

Remake in class SensorDs18b20
Author: Efraim Manurung
Information Technology Group, Wageningen University

v1.0: Try to refactor to make as a class 
'''

import os
import glob
import time

class SensorDs18b20:
    def __init__(self):
        print("SensorDs18b20 Start!")
        os.system('modprobe w1-gpio')
        os.system('modprobe w1-therm')
        base_dir = '/sys/bus/w1/devices/'
        device_folder = glob.glob(base_dir + '28*')[0]
        self.device_file = device_folder + '/w1_slave'
 
    def _read_temp_raw(self):
        f = open(self.device_file, 'r')
        lines = f.readlines()
        f.close()
        return lines

    def read_sensor_data(self):
        lines = self._read_temp_raw()
        while lines[0].strip()[-3:] != 'YES':
            time.sleep(0.2)
            lines = self._read_temp_raw()
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            temp_string = lines[1][equals_pos+2:]
            temp_c = float(temp_string) / 1000.0
            # temp_f = temp_c * 9.0 / 5.0 + 32.0
            return temp_c
    
    def average_sensor_data(self, _count, address, temperature):
        count = _count
        temperature_total = 0
        
        for x in range(count):
            temperature_total += temperature
            time.sleep(1)
        
        _averaged_temperature = temperature_total / count
        
        print("AVERAGED VALUES from Address {}, Av_Temp={:.2f}ºC".format(address, _averaged_temperature))

        return _averaged_temperature
    