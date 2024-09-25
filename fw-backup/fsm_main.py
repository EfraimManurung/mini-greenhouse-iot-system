'''
greenhouse-iot-system
Author: Efraim Manurung
MSc Thesis in Information Technology Group, Wageningen University

 
efraim.manurung@gmail.com

Refactor main program with finite state machine
'''

# Import libraries taht needed for the project
import time
import smbus2

# Import sensor classes
from misc.SensorBme280 import SensorBme280
from misc.SensorBh1750 import SensorBh1750
from misc.SensorMhz19 import SensorMhz19
from misc.OutdoorSensors import OutdoorSensors

# Import logging data class
from misc.LoggingData import LoggingData

# Import actuator class
from misc.ActuatorLED import ActuatorLED
from misc.ActuatorFAN import ActuatorFAN
from misc.ActuatorGPIO import ActuatorGPIO

# Initialize I2C bus
bus = smbus2.SMBus(1)

# List of sensors addresses
bme280_addresses                 = [0x76, 0x77]
mhz19_address                    = '/dev/ttyAMA0'
bh1750_addresses                 = [0x23, 0x5c] 
outdoor_sensor_adress            = '/dev/ttyUSB0'
outdoor_sensor_adress_baudrate   = 9600

# List of GPIOs
LEDStrip_GPIO   = 13
LEDBlink_GPIO   = 12

FAN_GPIO        = 26
HUMIDIFIER_GPIO = 16

# PWM Frequency
PWM_frequency = 50
PWM_frequency_for_blinking = 2

# Duty cycle in percentage
DT_blink = 50

# Create an instance of the sensor classes
bme280_sensors = SensorBme280(bus)
mhz19_sensor = SensorMhz19(mhz19_address)
bh1750_sensors = SensorBh1750(bus)
outdoor_sensors = OutdoorSensors(outdoor_sensor_adress, outdoor_sensor_adress_baudrate)
logging_data = LoggingData()

# Create an instance of the actuator classes
LEDStrip_actuator = ActuatorLED(LEDStrip_GPIO, PWM_frequency)
LEDBlink_actuator = ActuatorLED(LEDBlink_GPIO, PWM_frequency_for_blinking)

FAN_actuator = ActuatorFAN(FAN_GPIO, PWM_frequency)
HUMIDIFIER_actuator = ActuatorGPIO(HUMIDIFIER_GPIO)

def setPointsState():
    print("Set points state")
    
    # Define setpoints of the system
    setPoints = {
        "TEMP_SP": 25,
        "HUM_SP": 70
        # "CO2_SP": 410,
        # "LUX_SP": 1500
    }
    
    return "MONITOR"

iteration = 0

def monitorState():
    print("Monitor state")
    
    # Start main loop to measuring the environment inside and outside greenhouse
    # The data will send to InfluxDB
    # iteration = 0
    time.sleep(1)

    iteration += 1
    # Control flow for the iteration
    if iteration == 10:
        
        iteration = 0
        
        # mh_z19b sensors
        co2, temperature_co2 = mhz19_sensor.read_sensor_data()
        averaged_co2, averaged_temperature_co2 = mhz19_sensor.average_sensor_data(3, co2, temperature_co2)
        
        if averaged_co2 is not None and averaged_temperature_co2 is not None:
            # Send data to InfluxDB, omitting co2 and temperature_co2 if they are None
            logging_data.send_to_influxdb("greenhouse_measurements", "inside", None, None, None, None, averaged_co2, averaged_temperature_co2, None)
        
        # bh1750 sensors
        for address in bh1750_addresses:
            light = bh1750_sensors.read_sensor_data(address)
            if light is not None:
                averaged_light = bh1750_sensors.average_sensor_data(3, address, light)
                
                if averaged_light is not None:                        
                    # Send data to InfluxDB, omitting co2 and temperature_co2 if they are None
                    logging_data.send_to_influxdb("greenhouse_measurements", address, None, None, None, averaged_light, None, None, None)

        # bme280 sensors
        for address in bme280_addresses:
            temperature, humidity, pressure = bme280_sensors.read_sensor_data(address)
            if all(v is not None for v in [temperature, humidity, pressure]):
                averaged_temperature, averaged_humidity, averaged_pressure = bme280_sensors.average_sensor_data(3, address, temperature, humidity, pressure)

                # Control humidity with HUMIDIFIER
                
        
    
    return "MONITOR"

def actuateState():
    print("Actuate state")
    return "TERMINATE"

def actuateLEDState():
    print("Actuate LED state")
    return "MONITOR"

def actuateFanState():
    print("Actuate fan state")
    return "MONITOR"

def actuateHumidifierState():
    print("Actuate humidifier state")
    return "MONITOR"
    
def terminateState():
    print("Terminate state")
    return "MONITOR"

# Define possible states of the system
states = {
    "SETPOINTS": setPointsState,
    "MONITOR": monitorState,
    "ACTUATE": actuateState,
    "ACTUATE_LED": actuateLEDState,
    "ACTUATE_FAN": actuateFanState,
    "ACTUATE_HUMIDIFIER": actuateHumidifierState,
    "TERMINATE": terminateState
}
current_state = "MONITOR"

# Main loop for finite state machine
while True:
    next_state = states[current_state]()
    if next_state in states:
        current_state = next_state
    else:
        print("Unknown state")
        break

