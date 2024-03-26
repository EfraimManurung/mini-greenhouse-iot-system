# greenhouse-iot-system
# Efraim Manurung
# MSc Thesis in Information Technology Group, Wageningen University

# Import libraries that needed for the project
import smbus2
from misc.SensorBme280 import SensorBme280
from misc.SensorBh1750 import SensorBh1750

# Initialize I2C bus
bus = smbus2.SMBus(1)

# List of addresses
bme280_addresses = [0x76, 0x77]
bh1750_addresses = [0x23]
bh1750_command_read_address = [0x10]

# Create an instance of the Sensors class
bme280_sensors = SensorBme280(bus)
bh1750_sensors = SensorBh1750(bus)

# Main loop 
try:
    iteration = 0
    while True:
        iteration += 1
        print("Iteration : ", iteration)
        
        # bme280 sensors
        for address in bme280_addresses:
            # Read sensor data
            temperature, humidity, pressure = bme280_sensors.read_sensor_data(address)
            
            # Averaging the sensor data
            averaged_temperature, averaged_humidity, averaged_pressure = bme280_sensors.average_sensor_data(address, temperature, humidity, pressure)
            
            # Write it on the txt file
            bme280_sensors.write_sensor_data(address, averaged_temperature, averaged_humidity, averaged_pressure)
        
        # mh_z19b sensors
        
        
        # bh1750 sensors
        # for address in bh1750_addresses:
        #     # Read sensor data
        #     light = bh1750_sensors.read_sensor_data(address, bh1750_command_read_address)
        
except KeyboardInterrupt:
    print('Program stopped')

except Exception as e:
    print('An unexpected error occurred:', str(e))

