# greenhouse-iot-system
# Efraim Manurung
# MSc Thesis in Information Technology Group, Wageningen University

# Import libraries that needed for the project
import time
import smbus2
import bme280
import os
# Import custom miscellaneous functions
from misc.misc import average_sensor_data

# Declared variables
iteration = 0

# Create a variable to control the while loop
running = True

# Functions that will be used
def read_sensor_data(bus, address):
    # Load calibration parameters
    calibration_params = bme280.load_calibration_params(bus, address)

    try:
        # Read sensor data
        data = bme280.sample(bus, address, calibration_params)

        # Extract temperature, pressure, and humidity
        temperature = data.temperature
        pressure = data.pressure
        humidity = data.humidity
        
    except Exception as e:
        print('An unexpected error occurred at address 0x{:02X}:'.format(address), str(e))
    
    return temperature, pressure, humidity
    
def write_sensor_data(temperature, humidity, pressure):
    #save time, data, temperature, and humidity in .txt file
    file.write(time.strftime('%H:%M:%S %d/%m/%Y') + ', 0x{:02X}, {:.2f}, {:.2f}, {:.2f}\n'.format(address, temperature, humidity, pressure))


# Initialize I2C bus
bus = smbus2.SMBus(1)

# List of addresses to read from
addresses = [0x76, 0x77]

# Check if the file exists before opening it in 'a' mode (append mode)
file_exists = os.path.isfile('sensor_readings.txt')
file = open('sensor_readings.txt', 'a')

# Write the header to the file if the file does not exist
if not file_exists:
    file.write('Time and Data, sensor address, temperature (ºC), humidity (%), pressure (hPa)\n')

# Main loop 
while running:
    try:
        iteration += 1
        print("Iteration : ", iteration)
        for address in addresses:
            # Read sensor data
            temperature, humidity, pressure = read_sensor_data(bus, address)
            
            # Averaging the sensor data
            averaged_temperature, averaged_humidity, averaged_pressure = average_sensor_data(address, temperature, humidity, pressure)
            
            # Write it on the txt file
            write_sensor_data(averaged_temperature, averaged_humidity, averaged_pressure)

        # Wait for a few seconds before the next reading
        # time.sleep(10)
        print("")
        print("")
        
    except RuntimeError as error:
        # Errors happen fairly often, just keep going
        print(error.args[0])
        time.sleep(2.0)
        continue

    except KeyboardInterrupt:
        print('Program stopped')
        running = False
        file.close()
        
    except Exception as e:
        print('An unexpected error occurred:', str(e))
        running = False
        file.close()

