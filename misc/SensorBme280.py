'''
Author: Efraim Manurung
Information Technology Group, Wageningen University
efraim.manurung@gmail.com
'''

# import relevant libraries
import time
import bme280 
import os

class SensorBme280:
    def __init__(self, bus):
        self.bus = bus
        print("SensorBme280 Start!")

    def read_sensor_data(self, address):
        try:
            # Load calibration parameters
            calibration_params = bme280.load_calibration_params(self.bus, address)

            # Read sensor data
            data = bme280.sample(self.bus, address, calibration_params)

            # Extract temperature, pressure, and humidity
            temperature = data.temperature
            humidity = data.humidity
            pressure = data.pressure
            
        except Exception as e:
            print('ERROR BME280: An unexpected bme280 error occurred at address 0x{:02X}:'.format(address), str(e))
            temperature = None
            pressure = None
            humidity = None
        except OSError:
            print('ERROR BME280: BME280 I2C device not found. Please check BME280 wiring.')
            temperature = None
            pressure = None
            humidity = None
        except:
            print('ERROR BME280: General unknown error')
            temperature = None
            pressure = None
            humidity = None
        
        return temperature, humidity, pressure

    def average_sensor_data(self, _count, address, temperature, humidity, pressure):
        count = _count
        temperature_total = 0
        humidity_total = 0
        pressure_total = 0
        
        if None in [temperature, humidity, pressure]:
            print("No valid data to average from sensor at address 0x{:02X}".format(address))
            return None
        
        for x in range(count):
            temperature_total += temperature
            humidity_total += humidity
            pressure_total += pressure
            time.sleep(0.2)
        
        _averaged_temperature = temperature_total / count
        _averaged_humidity = humidity_total / count
        _averaged_pressure = pressure_total / count
        
        print("AVERAGED VALUES from Address 0x{:02X}, Av_Temp={:.2f}ºC, Av_Humidity={:.2f}, Av_Pressure={:.2f}".format(address, _averaged_temperature, _averaged_humidity, _averaged_pressure))

        return _averaged_temperature, _averaged_humidity, _averaged_pressure