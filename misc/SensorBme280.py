# import relevant libraries
import time
import bme280 
import os

class SensorBme280:
    def __init__(self, bus):
        self.bus = bus

    def read_sensor_data(self, address):
        # Load calibration parameters
        calibration_params = bme280.load_calibration_params(self.bus, address)

        try:
            # Read sensor data
            data = bme280.sample(self.bus, address, calibration_params)

            # Extract temperature, pressure, and humidity
            temperature = data.temperature
            pressure = data.pressure
            humidity = data.humidity
            
        except Exception as e:
            print('ERROR: An unexpected bme280 error occurred at address 0x{:02X}:'.format(address), str(e))
            temperature = None
            pressure = None
            humidity = None
        
        return temperature, pressure, humidity

    def average_sensor_data(self, address, temperature, humidity, pressure):
        count = 10
        temperature_total = 0
        humidity_total = 0
        pressure_total = 0
        
        for x in range(count):
            temperature_total += temperature
            humidity_total += humidity
            pressure_total += pressure
            time.sleep(1)
        
        _averaged_temperature = temperature_total / count
        _averaged_humidity = humidity_total / count
        _averaged_pressure = pressure_total / count
        
        print("AVERAGED VALUES from Address 0x{:02X}, Av_Temp={:.2f}ºC, Av_Humidity={:.2f}, Av_Pressure={:.2f}".format(address, _averaged_temperature, _averaged_humidity, _averaged_pressure))

        return _averaged_temperature, _averaged_humidity, _averaged_pressure

    def write_sensor_data(self, address, temperature, humidity, pressure):
        # Check if the file exists before opening it in 'a' mode (append mode)
        file_exists = os.path.isfile('sensor_readings_bme280.txt')
        
        # Open the file using a context manager
        with open('sensor_readings_bme280.txt', 'a') as file:
            # Write the header to the file if the file does not exist
            if not file_exists:
                file.write('Time and Data, sensor address, temperature (ºC), humidity (%), pressure (hPa)\n')
            
            # Write sensor data to the file
            file.write(time.strftime('%H:%M:%S %d/%m/%Y') + ', 0x{:02X}, {:.2f}, {:.2f}, {:.2f}\n'.format(address, temperature, humidity, pressure))