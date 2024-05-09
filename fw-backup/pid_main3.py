from simple_pid import PID
import time

from misc.ActuatorGPIO import ActuatorGPIO
from misc.ActuatorHEATER import ActuatorHEATER
from misc.OutdoorSensors import OutdoorSensors

outdoor_sensor_adress = '/dev/ttyUSB0'
outdoor_sensor_adress_baudrate = 9600

outdoor_sensors = OutdoorSensors(outdoor_sensor_adress, outdoor_sensor_adress_baudrate)

# Define PID parameters
Kp = 2
Ki = 5
Kd = 1
temperature_setpoint = 35.0

# Initialize PID controller
pid = PID(Kp, Ki, Kd, setpoint=temperature_setpoint)
pid.output_limits = (0, 5000)  # Output limits based on the window size

# Define the heater GPIO pin
HEATER_GPIO = 6
HEATER_actuator = ActuatorGPIO(HEATER_GPIO)

# Define the window size
WindowSize = 5000
windowStartTime = time.time() * 1000  # Convert seconds to milliseconds

count = 0

try:
    while True:
        count += 1
        time.sleep(0.2)

        # Read temperature from outdoor sensor
        lux, temp, hum, ccs_co2, ccs_tvco2, co2, temp_co2 = outdoor_sensors.read_sensor_data()

        # Calculate PID output
        output = pid(temp)
        
        # Debugging
        print("temperature: {}, output: {}, count: {}".format(temp, output, count))

        # Adjust window start time if needed
        if time.time() * 1000 - windowStartTime > WindowSize:
            windowStartTime += WindowSize

        # Control the heater based on PID output
        if output < time.time() * 1000 - windowStartTime:
            # Turn heater on
            HEATER_actuator.actuate_GPIO_HIGH()
            print("HEATER_actuator.actuate_GPIO_HIGH()")
        else:
            # Turn heater off
            HEATER_actuator.actuate_GPIO_LOW()
            print("HEATER_actuator.actuate_GPIO_LOW()")

except KeyboardInterrupt:
    HEATER_actuator.GPIO_cleanup()
    print('Program stopped')
