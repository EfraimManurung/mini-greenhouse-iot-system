# Source website to work on the serial
# https://roboticsbackend.com/raspberry-pi-arduino-serial-communication/
# Try to manipulate it MH-Z19C (UART) -> (UART) ESP32 (USB-Serial)-> (USB-Serial) Raspberry Pi

import serial
import time
import os

class SensorMhz19:
    def __init__(self, usb_address):
        self.ser = serial.Serial(usb_address, 9600, timeout=1)
        self.ser.reset_input_buffer()
        self.co2_value = None
        self.temp_value = None
    
    #def read_write_sensor_data(self):
    def read_sensor_data(self):
        try:
            # Read sensor data
            if self.ser.in_waiting > 0:
                line = self.ser.readline().decode('utf-8').rstrip()
                if line.startswith("co2: "):
                    self.co2_value = float(line.split(" ")[1])
                elif line.startswith("temp: "):
                    self.temp_value = float(line.split(" ")[1])
                
                # If both CO2 and temperature values are received, print and reset variables
                if self.co2_value is not None and self.temp_value is not None:
                    print("CO2:", self.co2_value)
                    print("Temperature:", self.temp_value)
                    
                    #  Check if the file exists before opening it in 'a' mode (append mode)
                    # file_exists = os.path.isfile('sensor_readings_mhz19c.txt')
                    
                    # # Open the file using a context manager
                    # with open('sensor_readings_mhz19c.txt', 'a') as file:
                    #     # Write the header to the file if the file does not exist
                    #     if not file_exists:
                    #         file.write('Time and Data, co2(ppm), temperature(ºC)\n')
                        
                    #     # Write sensor data to the file
                    #     file.write(time.strftime('%H:%M:%S %d/%m/%Y') + ', {:.2f}, {:.2f}\n'.format(self.co2_value, self.temp_value))
                
                    # self.co2_value = None
                    # self.temp_value = None
            
        except Exception as e:
            print('ERROR:', str(e))
        
        return self.co2_value, self.temp_value
    
    # def average_sensor_data(self, co2_value, temp_value):
    #     count = 10
    #     co2_value_total = 0
    #     temp_value_total = 0
        
    #     for x in range(count):
    #         co2_value_total += co2_value
    #         temp_value_total += temp_value
    #         time.sleep(1)
        
    #     _averaged_co2 =  co2_value_total / count
    #     _averaged_temp = temp_value_total / count
        
    #     print("Averaged VALUES from CO2, Av_CO2={:.2f} ppm, Av_Temp={:.2f}".format(_averaged_co2, _averaged_temp))
        
    #     return _averaged_co2, _averaged_temp
        
    def write_sensor_data(self, _averaged_co2, _averaged_temp):
        # Check if the file exists before opening it in 'a' mode (append mode)
        file_exists = os.path.isfile('sensor_readings_mhz19c.txt')
        
        # Open the file using a context manager
        with open('sensor_readings_mhz19c.txt', 'a') as file:
            # Write the header to the file if the file does not exist
            if not file_exists:
                file.write('Time and Data, co2(ppm), temperature(ºC)\n')
            
            # Write sensor data to the file
            file.write(time.strftime('%H:%M:%S %d/%m/%Y') + ', {:.2f}, {:.2f}\n'.format(_averaged_co2, _averaged_temp))
    