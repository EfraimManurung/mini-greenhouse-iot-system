# greenhouse-iot-system
# Efraim Manurung
# MSc Thesis in Information Technology Group, Wageningen University

# Import libraries that needed for the project
import time
import smbus2
import os
from misc.Sensors import Sensors

# Initialize I2C bus
bus = smbus2.SMBus(1)

# List of addresses to read from
addresses = [0x76, 0x77]

# Create an instance of the Sensors class
sensors = Sensors(bus)

# Check if the file exists before opening it in 'a' mode (append mode)
file_exists = os.path.isfile('sensor_readings.txt')
file = open('sensor_readings.txt', 'a')

# Write the header to the file if the file does not exist
if not file_exists:
    file.write('Time and Data, sensor address, temperature (ºC), humidity (%), pressure (hPa)\n')

# Main loop 
try:
    iteration = 0
    while True:
        iteration += 1
        print("Iteration : ", iteration)
        for address in addresses:
            # Read sensor data
            temperature, humidity, pressure = sensors.read_sensor_data(address)
            
            # Averaging the sensor data
            averaged_temperature, averaged_humidity, averaged_pressure = sensors.average_sensor_data(address, temperature, humidity, pressure)
            
            # Write it on the txt file
            sensors.write_sensor_data(address, averaged_temperature, averaged_humidity, averaged_pressure, file)

        # Wait for a few seconds before the next reading
        # time.sleep(10)
        print("")
        print("")
        
except KeyboardInterrupt:
    print('Program stopped')

except Exception as e:
    print('An unexpected error occurred:', str(e))

finally:
    file.close()

