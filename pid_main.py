# Import libraries that needed for the project
import time
import smbus2
from simple_pid import PID

from misc.ActuatorGPIO import ActuatorGPIO
from misc.SensorBme280 import SensorBme280

window_size = 5000
window_start_time = time.time() * 1000

humidity_setpoint = 87.0

# Initialize I2C bus
bus = smbus2.SMBus(1)

# bme280_addresses = [0x76]
# Create an instance of the sensor classes
bme280_sensors = SensorBme280(bus)

HUMIDIFIER_GPIO = 16
HUMIDIFIER_actuator = ActuatorGPIO(HUMIDIFIER_GPIO)

# pid = PID(5, 0.01, 0.1, setpoint=humidity_setpoint)
pid = PID(5, 10, 1, setpoint=humidity_setpoint)
pid.output_limits = (0, window_size)

count = 0

try:
    while True:
        time.sleep(0.5)
        count += 1
        
        temperature, humidity, pressure = bme280_sensors.read_sensor_data(0x77)
        
        output = pid(humidity)
        
        print("humidity: {}, output: {}, count: {}".format(humidity, output, count))

        if (time.time() * 1000) - window_start_time > window_size:
            # Time to shift the relay window
            window_start_time += window_size
        
        if (output < time.time()*1000 - window_start_time):
            # HUMIDIFIER_actuator.actuate_GPIO_HIGH()
            HUMIDIFIER_actuator.actuate_GPIO_LOW()
        else:
            # HUMIDIFIER_actuator.actuate_GPIO_LOW()
            HUMIDIFIER_actuator.actuate_GPIO_HIGH()

except KeyboardInterrupt:
    HUMIDIFIER_actuator.GPIO_cleanup()
    print('Program stopped')