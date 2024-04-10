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
from misc.SensorDs18b20 import SensorDs18b20
from misc.LoggingData import LoggingData

# Import actuator class
from misc.ActuatorLED import ActuatorLED
from misc.ActuatorFAN import ActuatorFAN
from misc.ActuatorSERVO import ActuatorSERVO

# Initialize I2C bus
bus = smbus2.SMBus(1)

# List of addresses
bme280_addresses = [0x76, 0x77]
mhz19_address = '/dev/ttyAMA0'
bh1750_addresses = [0x23, 0x5c] 
ds18b20_address = "GPIO4-One-Wire"

# List of GPIOs
LEDStrip_GPIO = 13
LEDBlink_GPIO = 12

FANFront_GPIO = 16
FANBack_GPIO = 26

SERVO_GPIO = 6

# PWM Frequency
PWM_frequency = 50
PWM_blink = 2

# Duty cycle in percentage
DT_blink = 50

# Create an instance of the sensor classes
bme280_sensors = SensorBme280(bus)
mhz19_sensor = SensorMhz19(mhz19_address)
bh1750_sensors = SensorBh1750(bus)
ds18b20_sensor = SensorDs18b20()
logging_data = LoggingData()

# Create an instance of the actuator classes
LEDStrip_actuator = ActuatorLED(LEDStrip_GPIO, PWM_frequency)
LEDBlink_actuator = ActuatorLED(LEDBlink_GPIO, PWM_blink)

FANFront_actuator = ActuatorFAN(FANFront_GPIO, PWM_frequency)
FANBack_actuator = ActuatorFAN(FANBack_GPIO, PWM_frequency)

SERVO_actuator = ActuatorSERVO(SERVO_GPIO, PWM_frequency)

# Main loop 
try:
    iteration = 0
    
    # Prompt the user for the set point value
    # light_set_point = float(input("Enter the set point value: "))
    light_set_point = 15.0
    
    while True:
        # Control for FAN 
        # def actuate_FAN(self, current_value, set_point)
        FANFront_actuator.actuate_FAN(27.0, 25.0, 50)
        FANBack_actuator.actuate_FAN(27.0, 25.0, 50)
            
        # Testing SERVO with this method
        SERVO_actuator.actuate_SERVO(700.0, 500.0, 12)
    
        iteration += 1
        print("Iteration : ", iteration)
        LEDBlink_actuator.blink_LED(DT_blink)
        
        # Delay per 1 second
        time.sleep(1)
        
        if iteration == 10:    
            # Control again the actuator
            FANFront_actuator.actuate_FAN(27.0, 29.0, 50)
            FANBack_actuator.actuate_FAN(27.0, 29.0, 50)
            
            # Close the window with the servo
            SERVO_actuator.close_window(2)
            
            # Stop LED Blink
            # LEDBlink_actuator.stop_blink_LED()
            LEDBlink_actuator.blink_LED(100)
                    
            # mh_z19b sensors
            co2, temperature_co2 = mhz19_sensor.read_sensor_data()
            averaged_co2, averaged_temperature_co2 = mhz19_sensor.average_sensor_data(3, co2, temperature_co2)
            
            # Send data to InfluxDB, omitting co2 and temperature_co2 if they are None
            logging_data.send_to_influxdb("greenhouse_measurements", None, None, None, None, None, averaged_co2, averaged_temperature_co2, None)
                  
            # bme280 sensors
            for address in bh1750_addresses:
                light = bh1750_sensors.read_sensor_data(address)
                averaged_light = bh1750_sensors.average_sensor_data(3, address, light)
                
                # Actuating
                # actuate_LED(self, current_value, set_point, duty_cycle)
                LEDStrip_actuator.actuate_LED(averaged_light, light_set_point, 100)

                # Send data to InfluxDB, omitting co2 and temperature_co2 if they are None
                logging_data.send_to_influxdb("greenhouse_measurements", address, None, None, None, averaged_light, None, None, None)
    
            for address in bme280_addresses:
                temperature, humidity, pressure = bme280_sensors.read_sensor_data(address)
                averaged_temperature, averaged_humidity, averaged_pressure = bme280_sensors.average_sensor_data(3, address, temperature, humidity, pressure)
                # Send data to InfluxDB, omitting co2 and temperature_co2 if they are None
                logging_data.send_to_influxdb("greenhouse_measurements", address, averaged_temperature, averaged_pressure, averaged_humidity, None, None, None, None)

            # ds18b20 sensor with 1-Wire
            tank_temperature = ds18b20_sensor.read_sensor_data()
            averaged_tank_temperature = ds18b20_sensor.average_sensor_data(3, ds18b20_address, tank_temperature)
            # Send data to InfluxDB
            logging_data.send_to_influxdb("greenhouse_measurements", address, None, None, None, None, None, None, averaged_tank_temperature)

            
            iteration = 0
            
except KeyboardInterrupt:
    print('Program stopped')

except Exception as e:
    print('An unexpected error occurred:', str(e))
