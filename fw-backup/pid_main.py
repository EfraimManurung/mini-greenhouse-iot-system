# Import libraries that needed for the project
import time
import smbus2
from simple_pid import PID

from misc.ActuatorGPIO import ActuatorGPIO
from misc.SensorBme280 import SensorBme280
from misc.OutdoorSensors import OutdoorSensors

outdoor_sensor_adress = '/dev/ttyUSB0'
outdoor_sensor_adress_baudrate = 9600

window_size = 5000
window_start_time = time.time() * 1000

humidity_setpoint = 87.0
temperature_setpoint = 35.0

# Initialize I2C bus
bus = smbus2.SMBus(1)

# bme280_addresses = [0x76]
# Create an instance of the sensor classes
bme280_sensors = SensorBme280(bus)

outdoor_sensors = OutdoorSensors(outdoor_sensor_adress, outdoor_sensor_adress_baudrate)

HUMIDIFIER_GPIO = 16
HEATER_GPIO = 6

HUMIDIFIER_actuator = ActuatorGPIO(HUMIDIFIER_GPIO)
HEATER_actuator = ActuatorGPIO(HEATER_GPIO)

# pid = PID(5, 0.01, 0.1, setpoint=humidity_setpoint)
# pid = PID(5, 10, 1, setpoint=humidity_setpoint)
pid = PID(2, 5, 1, setpoint=temperature_setpoint)
pid.output_limits = (0, window_size)

count = 0

try:
    while True:
        time.sleep(0.1)
        count += 1
        
        # temperature, humidity, pressure = bme280_sensors.read_sensor_data(0x77)
         # outdoor sensor with serial connection
        lux, temp, hum, ccs_co2, ccs_tvco2, co2, temp_co2  = outdoor_sensors.read_sensor_data()
        
        # output = pid(humidity)
        # output = pid(temperature)
        output = pid(temp)
        
        # print("humidity: {}, output: {}, count: {}".format(humidity, output, count))
        print("temperature: {}, output: {}, count: {}".format(temp, output, count))
        
        if (time.time() * 1000) - window_start_time > window_size:
            # Time to shift the relay window
            window_start_time += window_size
        
        if (output < (time.time()*1000) - window_start_time):
            # HUMIDIFIER_actuator.actuate_GPIO_HIGH()
            # HUMIDIFIER_actuator.actuate_GPIO_LOW()
            HEATER_actuator.actuate_GPIO_LOW()
            print("HEATER_actuator.actuate_GPIO_LOW()")
            # HEATER_actuator.actuate_GPIO_HIGH()
            # print("HEATER_actuator.actuate_GPIO_HIGH()")
        else:
            # HUMIDIFIER_actuator.actuate_GPIO_LOW()
            # HUMIDIFIER_actuator.actuate_GPIO_HIGH()
            # HEATER_actuator.actuate_GPIO_LOW()
            # print("HEATER_actuator.actuate_GPIO_LOW()")
            HEATER_actuator.actuate_GPIO_HIGH()
            print("HEATER_actuator.actuate_GPIO_HIGH()")
            
except KeyboardInterrupt:
    HUMIDIFIER_actuator.GPIO_cleanup()
    HEATER_actuator.GPIO_cleanup()
    
    print('Program stopped')