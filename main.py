import time
import smbus2
import bme280

# Declare variables
iteration = 0

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

        # Convert temperature to Fahrenheit
        temperature_fahrenheit = celsius_to_fahrenheit(temperature_celsius)

        # Print the readings
        print("Address 0x{:02X} - Temperature: {:.2f} °C, {:.2f} °F".format(address, temperature_celsius, temperature_fahrenheit))
        print("Address 0x{:02X} - Pressure: {:.2f} hPa".format(address, pressure))
        print("Address 0x{:02X} - Humidity: {:.2f} %".format(address, humidity))

    except Exception as e:
        print('An unexpected error occurred at address 0x{:02X}:'.format(address), str(e))

# Initialize I2C bus
bus = smbus2.SMBus(1)
#time.sleep(2) #wait here to aovid 121 IO Error

# List of addresses to read from
addresses = [0x76, 0x77]

try:
    while True:
        iteration += 1
        print("Iteration : ", iteration)
        for address in addresses:
            read_sensor_data(bus, address)

        # Wait for a few seconds before the next reading
        time.sleep(2)
        print("")
        print("")

except KeyboardInterrupt:
    print('Program stopped')
except Exception as e:
    print('An unexpected error occurred:', str(e))
