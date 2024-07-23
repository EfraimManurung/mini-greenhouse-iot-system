'''
mini-greenhouse-iot-system
Author: Efraim Manurung
MSc Thesis in Information Technology Group, Wageningen University

efraim.efraimpartoginahotasi@wur.nl
efraim.manurung@gmail.com

Main program
'''

# Import libraries that needed for the project
import time
from datetime import datetime, timedelta
import smbus2

# Import sensor classes
from misc.SensorBme280 import SensorBme280
from misc.SensorBh1750 import SensorBh1750
from misc.SensorMhz19 import SensorMhz19
from misc.OutdoorSensors import OutdoorSensors

# Import for logging data
from misc.LoggingData import LoggingData

# Import actuator classes
from misc.ActuatorLED import ActuatorLED
from misc.ActuatorFAN import ActuatorFAN
from misc.ActuatorGPIO import ActuatorGPIO

# Import MQTT communication class
from misc.MqttComm import MqttComm

# Initialize I2C bus
bus = smbus2.SMBus(1)

# List of addresses
bme280_addresses = [0x76, 0x77]
mhz19_address = '/dev/ttyAMA0'
bh1750_addresses = [0x23, 0x5c] 
outdoor_sensor_adress = '/dev/ttyUSB0'
outdoor_sensor_adress_baudrate = 9600

# List of GPIOs
LEDStrip_GPIO = 17
LEDBlink_GPIO = 12

FAN_GPIO = 26
HUMIDIFIER_GPIO = 16
# HEATER_GPIO = 6
# FAN_HEATER_GPIO = 5

# PWM Frequency
PWM_frequency = 50
PWM_frequency_for_blinking = 2

# Duty cycle in percentage
DT_blink = 50

# Create an instance of the sensors class
bme280_sensors = SensorBme280(bus)
mhz19_sensor = SensorMhz19(mhz19_address)
bh1750_sensors = SensorBh1750(bus)
outdoor_sensors = OutdoorSensors(outdoor_sensor_adress, outdoor_sensor_adress_baudrate)

# Create an instance of the logging data class
logging_data = LoggingData()

# Create an instance of the actuator class
LEDStrip_actuator = ActuatorLED(LEDStrip_GPIO, PWM_frequency)
LEDBlink_actuator = ActuatorLED(LEDBlink_GPIO, PWM_frequency_for_blinking)

FAN_actuator = ActuatorFAN(FAN_GPIO, PWM_frequency)
HUMIDIFIER_actuator = ActuatorGPIO(HUMIDIFIER_GPIO)
# HEATER_actuator = ActuatorGPIO(HEATER_GPIO)
# FAN_HEATER_actuator = ActuatorGPIO(FAN_HEATER_GPIO)

# Create an instance of the MQTT communication class
mqtt_comm = MqttComm()

# Initialized setpoints
# Control parameters                            Unit                    Descriptions
co2_set_point = 1000.0                          # [ppm]                 There is no control for co2 
global_solar_radiation_threshold = 50632.0      # [lux]                 400 / 0.0079 = 50632.0, for the sun there is an approximate conversion of 0.0079W/m2 per Lux. 
humidity_set_point = 87.0                       # [%]
temperature_set_point_at_night = 18.5           # [°C]
temperature_set_point_at_day = 19.5             # [°C]

# Send data every seconds
time_period = 20                                # s

# For send the data to the PC server
# outdoor_measurements_interval = 300             # s
# sum_av_lux = 0
# sum_av_temp = 0
# sum_av_hum = 0
# sum_av_co2 = 0 

# Initialize time tracking
last_5_minutes = datetime.now()

# Sum variables for 5 minutes intervals
sum_5_minutes_lux = 0
sum_5_minutes_temp = 0
sum_5_minutes_hum = 0
sum_5_minutes_co2 = 0
count_5_minutes = 0

# Count for time measurements and publish
count_time_measurements = 0
count_publish = 0

# List for the outdoor measurements
time_measurements = []
lux_outdoor_measurements = []
temp_outdoor_measurements = []
hum_outdoor_measurements = []
co2_outdoor_measurements = []

# Check daytime
def is_daytime_led():
    # Assuming day time is between 00:00 and 18:00
    #     setParam(gl, 'lampsOn', 0);            % time of day (in morning) to switch on lamps 													[hours since midnight] 					0
    #     setParam(gl, 'lampsOff', 18);          % time of day (in evening) to switch off lamps 
    now = datetime.now()
    current_time = now.time()
    return current_time >= datetime.strptime("00:00", "%H:%M").time() and \
           current_time <= datetime.strptime("18:00", "%H:%M").time()

def is_daytime():
    # Assuming day time is between 06:00 and 18:00
    now = datetime.now()
    current_time = now.time()
    return current_time >= datetime.strptime("06:00", "%H:%M").time() and \
           current_time <= datetime.strptime("18:00", "%H:%M").time()
    
# Define the function to check time and control the LED
def control_LED_strip(global_solar_radiation, iteration):
    
    # Check if current time is between 00:00 and 18:00
    if is_daytime_led():
           # Check if the global solar radiation is below the threshold
            if global_solar_radiation < global_solar_radiation_threshold:
                LEDStrip_actuator.LED_ON(100)   # Turn LED on
                if iteration % time_period == 0:
                    # def send_to_influxdb_data_control(self, measurement = None, actuator = None, value = None):
                    logging_data.send_to_influxdb_data_control("greenhouse_measurements", "led", 1)
            else:
                LEDStrip_actuator.LED_ON(0)     # Turn LED off
                if iteration % time_period == 0:
                    # def send_to_influxdb_data_control(self, measurement = None, actuator = None, value = None):
                    logging_data.send_to_influxdb_data_control("greenhouse_measurements", "led", 0)
    else:
        LEDStrip_actuator.LED_ON(0)             # Turn LED off
        if iteration % time_period == 0:
                    # def send_to_influxdb_data_control(self, measurement = None, actuator = None, value = None):
                    logging_data.send_to_influxdb_data_control("greenhouse_measurements", "led", 0)

# Define the function to control the LED
def control_fan(temperature, humidity, iteration):
    if is_daytime():
        temperature_setpoint = temperature_set_point_at_day
    else:
        temperature_setpoint = temperature_set_point_at_night
            
    # Ventilation due to excess heat
    if temperature > temperature_setpoint + 5:
        FAN_actuator.actuate_FAN(100)
        if iteration % time_period == 0:
            # def send_to_influxdb_data_control(self, measurement = None, actuator = None, value = None):
            logging_data.send_to_influxdb_data_control("greenhouse_measurements", "fan", 1)
    
    # Ventilation due to excess humidity
    elif humidity > humidity_set_point:
        FAN_actuator.actuate_FAN(100)
        if iteration % time_period == 0:
            # def send_to_influxdb_data_control(self, measurement = None, actuator = None, value = None):
            logging_data.send_to_influxdb_data_control("greenhouse_measurements", "fan", 1)

    # Close ventilation if indoor temperature is 1 degree below heating setpoint
    elif temperature < temperature_setpoint - 1:
        FAN_actuator.actuate_FAN(0)
        if iteration % time_period == 0:
            # def send_to_influxdb_data_control(self, measurement = None, actuator = None, value = None):
            logging_data.send_to_influxdb_data_control("greenhouse_measurements", "fan", 0)
    
    else:
        # No need for ventilation
        FAN_actuator.actuate_FAN(0)
        if iteration % time_period == 0:
            # def send_to_influxdb_data_control(self, measurement = None, actuator = None, value = None):
            logging_data.send_to_influxdb_data_control("greenhouse_measurements", "fan", 0)
    
# Main loop 
try:
    iteration = 0
    
    # Testing
    # FAN_actuator.actuate_FAN(100)
    # LEDStrip_actuator.LED_ON(100)
    
    while True:
        # Track current time
        current_time = datetime.now()
        
        # Testing ALL THE ACTUATORS with this METHODS
        # HUMIDIFIER_actuator.actuate_GPIO_HIGH()
        # FAN_actuator.actuate_FAN(100)
        # LEDStrip_actuator.actuate_LED(10.0, light_set_point, 100)
    
        iteration += 1
        print("Iteration : ", iteration)
        LEDBlink_actuator.LED_ON(DT_blink)
        
        # Delay per 1 second
        time.sleep(1)
        
        # Stop LED Blink make it turn on without blinking
        LEDBlink_actuator.LED_ON(100)
                
        # mh_z19b sensors
        co2, temperature_co2 = mhz19_sensor.read_sensor_data()
        if co2 is not None and temperature_co2 is not None:
            averaged_co2, averaged_temperature_co2 = mhz19_sensor.average_sensor_data(3, co2, temperature_co2)
        
            if iteration % time_period == 0:
                # Send data to InfluxDB, omitting co2 and temperature_co2 if they are None
                logging_data.send_to_influxdb("greenhouse_measurements", "inside", None, None, None, None, averaged_co2, averaged_temperature_co2, None, None)
                    
        # bh1750 sensors
        for address in bh1750_addresses:
            light = bh1750_sensors.read_sensor_data(address)
            if light is not None:
                averaged_light = bh1750_sensors.average_sensor_data(3, address, light)
                
                if iteration % time_period == 0:                       
                    # Send data to InfluxDB, omitting co2 and temperature_co2 if they are None
                    logging_data.send_to_influxdb("greenhouse_measurements", address, None, None, None, averaged_light, None, None, None, None)

        # bme280 sensors
        temp_sum = 0  # Variable to store the sum of averaged temperatures
        count = 0     # Variable to store the count of addresses with valid temperature readings
        
        for address in bme280_addresses:
            temperature, humidity, pressure = bme280_sensors.read_sensor_data(address)
            if all(v is not None for v in [temperature, humidity, pressure]):
                averaged_temperature, averaged_humidity, averaged_pressure = bme280_sensors.average_sensor_data(3, address, temperature, humidity, pressure)
                
                # Add averaged temperature to the sum
                temp_sum += averaged_temperature
                count += 1
                
                if iteration % time_period == 0: 
                    # Send data to InfluxDB, omitting co2 and temperature_co2 if they are None
                    logging_data.send_to_influxdb("greenhouse_measurements", address, averaged_temperature, averaged_pressure, averaged_humidity, None, None, None, None, None)
        
        # Calculate the overall average temperature
        if count > 0:
            overall_average_temperature = temp_sum / count
            
            print(f"Overall average temperature: {overall_average_temperature}")

            # Call the control function control_fan(temperature, humidity, iteration)
            control_fan(overall_average_temperature, averaged_humidity, iteration)
        
        # outdoor sensor with serial connection
        lux, temp, hum, ccs_co2, ccs_tvco2, co2, temp_co2  = outdoor_sensors.read_sensor_data()
        av_lux, av_temp, av_hum, av_ccs_co2, av_ccs_tvco2, av_co2, av_temp_co2 = outdoor_sensors.average_sensor_data(2, lux, temp, hum, ccs_co2, ccs_tvco2, co2, temp_co2)
        
        '''
        TO-DO: Send the weather datasets every 20 minutes to the server (in this case is a PC).
        
        Average per 5 minutes.
        
        Convert data to JSON format use format_data_in_JSON method in the MqttComm class
        
        Outdoor measurements:
        - lux: Need to be converted to W / m^2
        - temperature
        - humidity
        - co2
        '''
        
        # Accumulate 5-minutes measurements
        sum_5_minutes_lux += av_lux
        sum_5_minutes_temp += av_temp
        sum_5_minutes_hum += av_hum
        sum_5_minutes_co2 += av_co2
        count_5_minutes += 1
        
        # Calculate and send 5-minutes average data
        if (current_time - last_5_minutes).seconds >= 10:
            
            # Count if exceed 4 times then it is equal to 20 minutes
            count_time_measurements += 1
            # count_publish += 1
            
            # Average the data 
            avg_5_minutes_lux = sum_5_minutes_lux / count_5_minutes
            avg_5_minutes_temp = sum_5_minutes_temp / count_5_minutes
            avg_5_minutes_hum = sum_5_minutes_hum / count_5_minutes
            avg_5_minutes_co2 = sum_5_minutes_co2 / count_5_minutes
            
            # Reset 5-minutes accumulators
            sum_5_minutes_lux = 0
            sum_5_minutes_temp = 0
            sum_5_minutes_hum = 0
            sum_5_minutes_co2 = 0
            count_5_minutes = 0
            
            last_5_minutes = current_time
            
            print("5-minutes averages:", avg_5_minutes_lux, avg_5_minutes_temp, avg_5_minutes_hum, avg_5_minutes_co2)
            
            # Appending the new measurements to the list
            calculate_time = count_time_measurements * 300
            time_measurements.append(calculate_time)
            lux_outdoor_measurements.append(avg_5_minutes_lux)
            temp_outdoor_measurements.append(avg_5_minutes_temp)
            hum_outdoor_measurements.append(avg_5_minutes_hum)
            co2_outdoor_measurements.append(avg_5_minutes_co2)
            
            print("LUX OUTDOOR MEASUREMENTS: ", lux_outdoor_measurements)
            print("TEMP OUTDOOR MEASUREMENTS: ", temp_outdoor_measurements)
            
            #if count_publish == 4:
            if count_time_measurements == 4:
                # Reset count_time_measurements
                count_time_measurements = 0
                # count_publish = 0
                
                # Format data into JSON format
                json_data = mqtt_comm.format_data_in_JSON(time_measurements, \
                                                        lux_outdoor_measurements, \
                                                        temp_outdoor_measurements, \
                                                        hum_outdoor_measurements, \
                                                        co2_outdoor_measurements)
                            
                # Publish it to the server
                mqtt_comm.publish_mqtt_data(json_data)
                
                # Reset the outdoor measurements
                # List for the outdoor measurements
                time_measurements = []
                lux_outdoor_measurements = []
                temp_outdoor_measurements = []
                hum_outdoor_measurements = []
                co2_outdoor_measurements = []
        
        # Send the data to the database (InfluxDB)
        if any(val is not None for val in [av_lux, av_temp, av_hum, av_ccs_co2, av_ccs_tvco2, av_co2, av_temp_co2]):

            # Call the control function control_LED_strip(global_solar_radiation):
            control_LED_strip(av_lux, iteration)
            
            # Send data to InfluxDB, omitting co2 and temperature_co2 if they are None
            # Logs the data to your InfluxDB
            # def send_to_influxdb(self, measurement = None, location = None, temperature = None, pressure = None, 
            #                      humidity = None , light = None, co2 = None, temperature_co2 = None, ccs_co2 = None, ccs_tvco2 = None):
            if iteration % time_period == 0:
                logging_data.send_to_influxdb("greenhouse_measurements", "outdoor", av_temp, None, av_hum, av_lux, av_co2, av_temp_co2, av_ccs_co2, av_ccs_tvco2)

        # MQTT Communication
        # json_data = "HAI FROM RASPBERRY PI - EFRAIM"
        # mqtt_comm.publish_mqtt_data(json_data)
        
except KeyboardInterrupt:
    # Clean up all the GPIOs
    LEDStrip_actuator.GPIO_cleanup()
    LEDBlink_actuator.GPIO_cleanup()
    FAN_actuator.GPIO_cleanup()
    HUMIDIFIER_actuator.GPIO_cleanup()
    # HEATER_actuator.GPIO_cleanup()
    # FAN_HEATER_actuator.GPIO_cleanup()
    
    print('Program stopped')
    
except Exception as e:
    print('An unexpected error occurred:', str(e))
