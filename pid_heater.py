'''
mini-greenhouse-iot-system
Author: Efraim Manurung
MSc Thesis in Information Technology Group, Wageningen University

efraim.efraimpartoginahotasi@wur.nl
efraim.manurung@gmail.com

PID for the heater
'''

# Import libraries that needed for the project
import time
from datetime import datetime
import smbus2
from simple_pid import PID

# Import sensor classes
from misc.SensorBme280 import SensorBme280

# Import actuator classes
from misc.ActuatorGPIO import ActuatorGPIO
from misc.OutdoorSensors import OutdoorSensors

# List of GPIOs
HEATER_GPIO = 6
FAN_HEATER_GPIO = 5

# Initialize I2C bus
bus = smbus2.SMBus(1)

# List of addresses
bme280_addresses = [0x76, 0x77]

# Create an instance of the sensor classes
bme280_sensors = SensorBme280(bus)

HEATER_actuator = ActuatorGPIO(HEATER_GPIO)
FAN_HEATER_actuator = ActuatorGPIO(FAN_HEATER_GPIO)

temperature_set_point_at_night = 18.5           # [°C]
temperature_set_point_at_day = 19.5             # [°C]

# Initialize PID, define PID parameters
Kp = 2
Ki = 5
Kd = 1
output_limits = 60

# Initialized class object of PID and set it default values
pid_heater = PID(Kp, Ki, Kd, setpoint = 0.0)
pid_heater.output_limits  = (0, output_limits)

# Check daytime
def is_daytime():
    # Assuming day time is between 06:00 and 18:00
    now = datetime.now()
    current_time = now.time()
    return current_time >= datetime.strptime("06:00", "%H:%M").time() and \
           current_time <= datetime.strptime("18:00", "%H:%M").time()

# Define the function to control heater
def pid_control_heater(_temperature, iteration):
    if is_daytime():
        temperature_setpoint = temperature_set_point_at_day
    else:
        temperature_setpoint = temperature_set_point_at_night

    pid_heater.setpoint = temperature_setpoint
    output = pid_heater(_temperature)
    
    print("temperature: {}, output: {}, count: {}".format(_temperature, output, iteration))
    
    # Turn on the heater for the duration specified by the PID output
    if output > 0:
            HEATER_actuator.actuate_GPIO_HIGH()     # Turn heater on
            FAN_HEATER_actuator.actuate_GPIO_HIGH() # Turn FAN heater on
            time.sleep(output)               # Keep heater on for output milliseconds
            HEATER_actuator.actuate_GPIO_LOW()      # Turn heater off
            FAN_HEATER_actuator.actuate_GPIO_LOW()  # Turn FAN heater off
            
# Main loop
try:
    iteration = 0
    
    while True:
        iteration += 1
        
        # bme280 sensors
        for address in bme280_addresses:
            temperature, humidity, pressure = bme280_sensors.read_sensor_data(address)
            if all(v is not None for v in [temperature, humidity, pressure]):
                averaged_temperature, averaged_humidity, averaged_pressure = bme280_sensors.average_sensor_data(3, address, temperature, humidity, pressure)
                
                # Call the PID control heater function
                pid_control_heater(averaged_temperature, iteration)

except KeyboardInterrupt:
    # Clean up all the GPIOs
    HEATER_actuator.GPIO_cleanup()
    FAN_HEATER_actuator.GPIO_cleanup()
    
    print('Program stopped')

except Exception as e:
    print('An unexpected error occurred:', str(e))