# Import libraries that needed for the project
import time
import smbus2
from simple_pid import PID

from misc.ActuatorGPIO import ActuatorGPIO
from misc.OutdoorSensors import OutdoorSensors

outdoor_sensor_adress = '/dev/ttyUSB0'
outdoor_sensor_adress_baudrate = 9600

temperature_setpoint = 35.0

outdoor_sensors = OutdoorSensors(outdoor_sensor_adress, outdoor_sensor_adress_baudrate)

HEATER_GPIO = 6
FAN_HEATER_GPIO = 5

HEATER_actuator = ActuatorGPIO(HEATER_GPIO)
FAN_HEATER_actuator = ActuatorGPIO(FAN_HEATER_GPIO)

# pid = PID(5, 0.01, 0.1, setpoint=humidity_setpoint)
# pid = PID(5, 10, 1, setpoint=humidity_setpoint)
# pid = PID(4, 1, 2, setpoint=temperature_setpoint)
pid = PID(2, 3, 1, setpoint=temperature_setpoint) # Good enough!
pid.output_limits = (0, 5000)

count = 0

try:
    while True:
        time.sleep(0.2)
        count += 1
        
        lux, temp, hum, ccs_co2, ccs_tvco2, co2, temp_co2  = outdoor_sensors.read_sensor_data()
        
        output = pid(temp)
        
        print("temperature: {}, output: {}, count: {}".format(temp, output, count))
        
        # Turn on the heater for the duration specified by the PID output
        if output > 0:
            HEATER_actuator.actuate_GPIO_HIGH()  # Turn heater on
            FAN_HEATER_actuator.actuate_GPIO_HIGH() # Turn FAN heater on
            time.sleep(output / 1000)            # Keep heater on for output milliseconds
            HEATER_actuator.actuate_GPIO_LOW()   # Turn heater off
            FAN_HEATER_actuator.actuate_GPIO_LOW() # Turn FAN heater off
        
except KeyboardInterrupt:
    HEATER_actuator.GPIO_cleanup()
    
    print('Program stopped')

            
except KeyboardInterrupt:
    HEATER_actuator.GPIO_cleanup()
    
    print('Program stopped')