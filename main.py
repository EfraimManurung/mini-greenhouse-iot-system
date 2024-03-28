# greenhouse-iot-system
# Author: Efraim Manurung
# MSc Thesis in Information Technology Group, Wageningen University

# Import libraries that needed for the project
import time
import smbus2
from misc.SensorBme280 import SensorBme280
from misc.SensorBh1750 import SensorBh1750
from misc.SensorMhz19 import SensorMhz19
from misc.LoggingData import LoggingData

# Initialize I2C bus
bus = smbus2.SMBus(1)

# List of addresses
bme280_addresses = [0x76, 0x77]
bh1750_addresses = [0x23]
bh1750_command_read_address = [0x10]
mhz19_address = '/dev/ttyUSB0'

# Create an instance of the Classes
bme280_sensors = SensorBme280(bus)
bh1750_sensors = SensorBh1750(bus)
mhz19_sensor = SensorMhz19(mhz19_address)
logging_data = LoggingData()

# Main loop 
try:
    iteration = 0
    while True:
        iteration += 1
        print("Iteration : ", iteration)
        
        # bme280 sensors
        # for address in bme280_addresses:
        #     # Read sensor data
        #     temperature, humidity, pressure = bme280_sensors.read_sensor_data(address)
            
        #     # Averaging the sensor data
        #     averaged_temperature, averaged_humidity, averaged_pressure = bme280_sensors.average_sensor_data(address, temperature, humidity, pressure)
            
        #     # Write it on the txt file
        #     bme280_sensors.write_sensor_data(address, averaged_temperature, averaged_humidity, averaged_pressure)
            
        #     # logging Raspberry Pi environmental data to InfluxDB
        #     logging_data.send_to_influxdb("greenhouse_measurements", address, averaged_temperature, averaged_humidity, averaged_pressure, 50.5)
        
        # mh_z19b sensors
        # Read sensor data
        time.sleep(10.0)
        co2, temperature_co2 = mhz19_sensor.read_sensor_data()
        #mhz19_sensor.read_write_sensor_data()
        
        # AVeraging the sensor data
        # averaged_co2, averaged_temperature_co2 = mhz19_sensor.average_sensor_data(co2, temperature_co2)
        
        # Write it on the txt file
        # mhz19_sensor.write_sensor_data(averaged_co2, averaged_temperature_co2)
        #mhz19_sensor.write_sensor_data(co2, temperature_co2)
        
        # bh1750 sensors
        # for address in bh1750_addresses:
        #     # Read sensor data
        #     light = bh1750_sensors.read_sensor_data(address, bh1750_command_read_address)
        
except KeyboardInterrupt:
    print('Program stopped')

except Exception as e:
    print('An unexpected error occurred:', str(e))

