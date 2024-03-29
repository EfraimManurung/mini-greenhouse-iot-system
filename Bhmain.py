# Import libraries that needed for the project
import time
import smbus2

# Import custom classes
from misc.SensorBh1750 import SensorBh1750

# Initialize I2C bus
bus = smbus2.SMBus(1)

# List of addresses
bh1750_addresses = [0x23]
bh1750_command_read_address = [0x10]

# Create an instance of the Classes
bh1750_sensors = SensorBh1750(bus)

# Main loop 
try:
    iteration = 0
    while True:
        iteration += 1
        time.sleep(1)
        
        print("Iteration : ", iteration)
        
        if iteration == 3:
            # bh1750 sensors
            for address in bh1750_addresses:
                # Read sensor data
                light = bh1750_sensors.read_sensor_data(address, bh1750_command_read_address)
                
                # Averaging the sensor data
                averaged_light = bh1750_sensors.average_sensor_data(address, light)
                
                # Write it on the txt file
                # bme280_sensors.write_sensor_data(address, averaged_temperature, averaged_humidity, averaged_pressure)
            iteration = 0
          
except KeyboardInterrupt:
    print('Program stopped')

except Exception as e:
    print('An unexpected error occurred:', str(e))
