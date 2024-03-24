# greenhouse-iot-system
# Efraim Manurung
# MSc Thesis in Information Technology Group, Wageningen University

# Import libraries that needed for the project
import time
import smbus2
import bme280
import os

# Declared variables
iteration = 0

# Create a variable to control the while loop
running = True

# Functions that will be used
def celsius_to_fahrenheit(celsius):
    return (celsius * 9/5) + 32

def read_sensor_data(bus, address):
    # Load calibration parameters
    calibration_params = bme280.load_calibration_params(bus, address)

    try:
        # Read sensor data
        data = bme280.sample(bus, address, calibration_params)

        # Extract temperature, pressure, and humidity
        temperature_celsius = data.temperature
        pressure = data.pressure
        humidity = data.humidity

        # Print the readings on the shell
        print("Address 0x{0:02X}, Temp={1:0.1f}ºC, Humidity={2:0.1f}, Pressure={3:0.1f}".format(address, temperature_celsius, humidity, pressure))

    except Exception as e:
        print('An unexpected error occurred at address 0x{:02X}:'.format(address), str(e))
    
    return temperature_celsius, pressure, humidity
    
def write_sensor_data(temperature_celsius, humidity, pressure):
    #save time, data, temperature, and humidity in .txt file
    file.write(time.strftime('%H:%M:%S %d/%m/%Y') + ', 0x{:02X}, {:.2f}, {:.2f}, {:.2f}\n'.format(address, temperature_celsius, humidity, pressure))
        
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
            temperature_celsius, humidity, pressure = read_sensor_data(bus, address)
            
            write_sensor_data(temperature_celsius, humidity, pressure)

        # Wait for a few seconds before the next reading
        time.sleep(10)
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

