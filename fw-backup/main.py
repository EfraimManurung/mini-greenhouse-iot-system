'''
mini-greenhouse-iot-system
Author: Efraim Manurung
MSc Thesis in Information Technology Group, Wageningen University

 
efraim.manurung@gmail.com

Main program
'''

# Import libraries that needed for the project
import time
import smbus2

# Import sensor classes
from misc.SensorBme280 import SensorBme280
from misc.SensorBh1750 import SensorBh1750
from misc.SensorMhz19 import SensorMhz19
from misc.OutdoorSensors import OutdoorSensors
from misc.LoggingData import LoggingData

# Import actuator classes
from misc.ActuatorLED import ActuatorLED
from misc.ActuatorFAN import ActuatorFAN
from misc.ActuatorGPIO import ActuatorGPIO

# Initialize I2C bus
bus = smbus2.SMBus(1)

# List of addresses
bme280_addresses = [0x76, 0x77]
mhz19_address = '/dev/ttyAMA0'
bh1750_addresses = [0x23, 0x5c] 
outdoor_sensor_adress = '/dev/ttyUSB0'
outdoor_sensor_adress_baudrate =9600

# List of GPIOs
LEDStrip_GPIO = 13
LEDBlink_GPIO = 12

FAN_GPIO = 26
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

# Main loop 
try:
    iteration = 0
    
    # Prompt the user for the set point value
    # light_set_point = float(input("Enter the set point value: "))
    light_set_point = 1000.0
    
    while True:
        # Control for FAN 
        # def actuate_FAN(self, current_value, set_point)
        # FAN_actuator.actuate_FAN(27.0, 25.0, 0)

        # Testing ALL THE ACTUATORS with this METHODS
        HUMIDIFIER_actuator.actuate_GPIO_HIGH()
        FAN_actuator.actuate_FAN(27.0, 25.0, 100)
        LEDStrip_actuator.actuate_LED(10.0, light_set_point, 100)
    
        iteration += 1
        print("Iteration : ", iteration)
        LEDBlink_actuator.LED_ON(DT_blink)
        
        # Delay per 1 second
        time.sleep(1)
        
        if iteration == 10:    
            # Control again the actuator
            # FAN_actuator.actuate_FAN(27.0, 29.0, 50)
            
            # Stop LED Blink
            LEDBlink_actuator.LED_ON(100)
            # LEDStrip_actuator.actuate_LED(10.0, light_set_point, 100)
                    
            # mh_z19b sensors
            co2, temperature_co2 = mhz19_sensor.read_sensor_data()
            averaged_co2, averaged_temperature_co2 = mhz19_sensor.average_sensor_data(3, co2, temperature_co2)
            
            if averaged_co2 is not None and averaged_temperature_co2 is not None:
                # Send data to InfluxDB, omitting co2 and temperature_co2 if they are None
                logging_data.send_to_influxdb("greenhouse_measurements", "inside", None, None, None, None, averaged_co2, averaged_temperature_co2, None, None)
                    
            # bh1750 sensors
            for address in bh1750_addresses:
                light = bh1750_sensors.read_sensor_data(address)
                if light is not None:
                    averaged_light = bh1750_sensors.average_sensor_data(3, address, light)
                    
                    if averaged_light is not None:                        
                        # Send data to InfluxDB, omitting co2 and temperature_co2 if they are None
                        logging_data.send_to_influxdb("greenhouse_measurements", address, None, None, None, averaged_light, None, None, None, None)

            # bme280 sensors
            for address in bme280_addresses:
                temperature, humidity, pressure = bme280_sensors.read_sensor_data(address)
                if all(v is not None for v in [temperature, humidity, pressure]):
                    averaged_temperature, averaged_humidity, averaged_pressure = bme280_sensors.average_sensor_data(3, address, temperature, humidity, pressure)
                    
                    # Control humidity with HUMIDIFIER
                    # if averaged_humidity < 71.0:
                    #     HUMIDIFIER_actuator.actuate_GPIO_HIGH()
                    # else:
                    #     HUMIDIFIER_actuator.actuate_GPIO_LOW()
                    
                    # # Control humidity with FAN
                    # if averaged_humidity > 70.0:
                    #     FAN_actuator.actuate_FAN_HIGH(100)
                    # else:
                    #     FAN_actuator.actuate_FAN_HIGH(0)
                    
                    if all(v is not None for v in [averaged_temperature, averaged_humidity, averaged_pressure]):
                        # Send data to InfluxDB, omitting co2 and temperature_co2 if they are None
                        logging_data.send_to_influxdb("greenhouse_measurements", address, averaged_temperature, averaged_pressure, averaged_humidity, None, None, None, None, None)

            # outdoor sensor with serial connection
            lux, temp, hum, ccs_co2, ccs_tvco2, co2, temp_co2  = outdoor_sensors.read_sensor_data()
            av_lux, av_temp, av_hum, av_ccs_co2, av_ccs_tvco2, av_co2, av_temp_co2 = outdoor_sensors.average_sensor_data(5, lux, temp, hum, ccs_co2, ccs_tvco2, co2, temp_co2)
            if any(val is not None for val in [av_lux, av_temp, av_hum, av_ccs_co2, av_ccs_tvco2, av_co2, av_temp_co2]):
                # Send data to InfluxDB, omitting co2 and temperature_co2 if they are None
                # Logs the data to your InfluxDB
                # def send_to_influxdb(self, measurement = None, location = None, temperature = None, pressure = None, 
                #                      humidity = None , light = None, co2 = None, temperature_co2 = None, ccs_co2 = None, ccs_tvco2 = None):
                
                logging_data.send_to_influxdb("greenhouse_measurements", "outdoor", av_temp, None, av_hum, av_lux, av_co2, av_temp_co2, av_ccs_co2, av_ccs_tvco2)

            iteration = 0
            
except KeyboardInterrupt:
    HUMIDIFIER_actuator.GPIO_cleanup()
    print('Program stopped')
    
except Exception as e:
    print('An unexpected error occurred:', str(e))