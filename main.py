# greenhouse-iot-system
# Author: Efraim Manurung
# MSc Thesis in Information Technology Group, Wageningen University

# Import libraries that needed for the project
import time
import smbus2

# Import custom classes
from misc.SensorBme280 import SensorBme280
from misc.SensorBh1750 import SensorBh1750
from misc.SensorMhz19 import SensorMhz19
from misc.LoggingData import LoggingData

# Initialize I2C bus
bus = smbus2.SMBus(1)

# List of addresses
bme280_addresses = [0x76, 0x77]
# mhz19_address = '/dev/ttyUSB0'
bh1750_addresses = 0x23 #[0x23]
bh1750_command_read_address = [0x10]

# Create an instance of the Classes
bme280_sensors = SensorBme280(bus)
# mhz19_sensor = SensorMhz19(mhz19_address)
bh1750_sensors = SensorBh1750(bus)
logging_data = LoggingData()

# Main loop 
try:
    iteration = 0
    while True:
        iteration += 1
        time.sleep(1)
        
        print("Iteration : ", iteration)
        
        if iteration == 5:
            sensor_data = {}
            
            # mh_z19b sensors
            # co2, temperature_co2 = mhz19_sensor.read_sensor_data()
            co2 = 0.0
            temperature_co2 = 0.0
            
            # bh1750 sensors
            light = bh1750_sensors.read_sensor_data(bh1750_addresses)
            averaged_light = bh1750_sensors.average_sensor_data(3, bh1750_addresses, light)
                
            # bme280 sensors
            for address in bme280_addresses:
                temperature, humidity, pressure = bme280_sensors.read_sensor_data(address)
                averaged_temperature, averaged_humidity, averaged_pressure = bme280_sensors.average_sensor_data(3, address, temperature, humidity, pressure)
                
                # Send data to InfluxDB, omitting co2 and temperature_co2 if they are None
                logging_data.send_to_influxdb("greenhouse_measurements", address, temperature, pressure, humidity, light, co2, temperature_co2)
  
            iteration = 0
        
except KeyboardInterrupt:
    print('Program stopped')

except Exception as e:
    print('An unexpected error occurred:', str(e))
