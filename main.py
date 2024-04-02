# greenhouse-iot-system
# Author: Efraim Manurung
# MSc Thesis in Information Technology Group, Wageningen University

# Import libraries that needed for the project
import time
import smbus2

# Import sensor classes
from misc.SensorBme280 import SensorBme280
from misc.SensorBh1750 import SensorBh1750
from misc.SensorMhz19 import SensorMhz19
from misc.LoggingData import LoggingData

# Import actuator class
from misc.ActuatorLED import ActuatorLED

# Initialize I2C bus
bus = smbus2.SMBus(1)

# List of addresses
bme280_addresses = [0x76, 0x77]
# mhz19_address = '/dev/ttyUSB0'
bh1750_addresses = [0x23] 

# List of GPIOs
LED_GPIO = 13

# Create an instance of the Classes
bme280_sensors = SensorBme280(bus)
# mhz19_sensor = SensorMhz19(mhz19_address)
bh1750_sensors = SensorBh1750(bus)
logging_data = LoggingData()
LED_actuators = ActuatorLED(LED_GPIO)

LED_actuators.actuate_LED(5, 10)

# Main loop 
try:
    iteration = 0
    while True:
        iteration += 1
        time.sleep(1)
        
        print("Iteration : ", iteration)
        
        if iteration == 10:            
            # mh_z19b sensors
            # co2, temperature_co2 = mhz19_sensor.read_sensor_data()
                  
            # bme280 sensors
            for address in bh1750_addresses:
                light = bh1750_sensors.read_sensor_data(address)
                averaged_light = bh1750_sensors.average_sensor_data(3, address, light)
                # Send data to InfluxDB, omitting co2 and temperature_co2 if they are None
                logging_data.send_to_influxdb("greenhouse_measurements", address, None, None, None, averaged_light, None, None)
    
            for address in bme280_addresses:
                temperature, humidity, pressure = bme280_sensors.read_sensor_data(address)
                averaged_temperature, averaged_humidity, averaged_pressure = bme280_sensors.average_sensor_data(3, address, temperature, humidity, pressure)
                # Send data to InfluxDB, omitting co2 and temperature_co2 if they are None
                logging_data.send_to_influxdb("greenhouse_measurements", address, averaged_temperature, averaged_pressure, averaged_humidity, None, None, None)
    
            iteration = 0
            
except KeyboardInterrupt:
    print('Program stopped')

except Exception as e:
    print('An unexpected error occurred:', str(e))
