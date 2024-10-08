'''
mini-greenhouse-iot-system

mini greenhouse IoT system firmware using DRL model from PC server that can controls actuators and
get measurements from sensors with Raspberry Pi 5.

Author: Efraim Manurung
Information Technology Group, Wageningen University

efraim.manurung@gmail.com

Main program
'''

# Import libraries that needed for the project
import time
from datetime import datetime
import smbus2
import numpy as np

# Import sensor classes
from misc.SensorBme280 import SensorBme280
from misc.SensorBh1750 import SensorBh1750
from misc.SensorMhz19 import SensorMhz19
from misc.OutdoorSensors import OutdoorSensors
from misc.LeafSensor import LeafSensor

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
leaf_sensor_address = '/dev/ttyUSB1'
outdoor_sensor_adress_baudrate = 9600
leaf_sensor_address_baudrate = 9600

# List of GPIOs
LEDStrip_GPIO = 17
LEDBlink_GPIO = 12

FAN_GPIO = 26
HEATER_GPIO = 6
FAN_HEATER_GPIO = 5

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
leaf_sensor = LeafSensor(leaf_sensor_address, leaf_sensor_address_baudrate)

# Create an instance of the logging data class
logging_data = LoggingData()

# Create an instance of the actuator class
LEDStrip_actuator = ActuatorLED(LEDStrip_GPIO, PWM_frequency)
LEDBlink_actuator = ActuatorLED(LEDBlink_GPIO, PWM_frequency_for_blinking)

FAN_actuator = ActuatorFAN(FAN_GPIO, PWM_frequency)
HEATER_actuator = ActuatorGPIO(HEATER_GPIO)
FAN_HEATER_actuator = ActuatorGPIO(FAN_HEATER_GPIO)

# Create an instance of the MQTT communication class
mqtt_comm = MqttComm()

# Send data every 30 seconds
time_period = 20           

# Initialize time tracking
last_5_minutes = datetime.now() # for the measurements
last_20_minutes = datetime.now() # for the controls

# Sum variables for 5 minutes intervals
sum_5_minutes_lux_out = 0
sum_5_minutes_temp_out = 0
sum_5_minutes_hum_out = 0
sum_5_minutes_co2_out = 0

sum_5_minutes_lux_in = 0
sum_5_minutes_temp_in = 0
sum_5_minutes_hum_in = 0
sum_5_minutes_co2_in = 0
sum_5_minutes_leaf_temp = 0

count_5_minutes = 0

# Average variables for 5 minutes intervals
avg_5_minutes_lux_in = 0
avg_5_minutes_temp_in = 0
avg_5_minutes_hum_in = 0
avg_5_minutes_co2_in = 0
avg_5_minutes_leaf_temp = 0

# Count for time measurements and publish
count_time_measurements = 0
count_publish = 0

# List for the outdoor measurements
time_measurements = []
lux_outdoor_measurements = []
temp_outdoor_measurements = []
hum_outdoor_measurements = []
co2_outdoor_measurements = []

# List for the indoor measurements
lux_indoor_measurements = []
temp_indoor_measurements = []
hum_indoor_measurements = []
co2_indoor_measurements = []
leaf_temp_measurements = []

# flag for publish and subscribe
publish_mqtt_flag = True
subscribe_mqtt_flag = False

# flag for controls
controls_flag = True

# Count for how many publish the data
# Needed for the DRL model twice
count_publish_mqtt_flag = 0

# Initialize the sum of variables to average two sensors
co2_in_sum = 0
temp_in_sum = 0
hum_in_sum = 0
light_in_sum = 0

count_co2 = 0
count_temp = 0
count_hum = 0
count_light = 0

av_leaf_temp = 0
av_lux = av_temp = av_hum = av_ccs_co2 = av_ccs_tvco2 = av_co2 = av_temp_co2 = 0

# Function to handle NaN and append the previous value
def handle_nan_and_append(measurements_list, new_value):
    if np.isnan(new_value):
        # If the list is not empty, append the last valid value
        if measurements_list:
            new_value = measurements_list[-1]  # Use previous value

    measurements_list.append(new_value)

# Main loop 
try:
    iteration = 0
    
    while True:
        # Reset the sum of variables
        co2_in_sum = 0
        temp_in_sum = 0
        hum_in_sum = 0
        light_in_sum = 0
        
        count_co2 = 0
        count_temp = 0
        count_hum = 0
        count_light = 0
        
        # Track current time
        current_time = datetime.now()
            
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

            # Add averaged co2 to the sum
            co2_in_sum += averaged_co2
            count_co2 += 1
            
            # if iteration % time_period == 0:
                # Send data to InfluxDB, omitting co2 and temperature_co2 if they are None
                # logging_data.send_to_influxdb("greenhouse_measurements", "inside", None, None, None, None, averaged_co2, averaged_temperature_co2, None, None)
                    
        # bh1750 sensors
        for address in bh1750_addresses:
            light = bh1750_sensors.read_sensor_data(address)
            if light is not None:
                averaged_light = bh1750_sensors.average_sensor_data(3, address, light)
                
                # Add averaged light to the sum
                light_in_sum += averaged_light 
                count_light += 1
                
                # if iteration % time_period == 0:                       
                    # Send data to InfluxDB, omitting co2 and temperature_co2 if they are None
                    # logging_data.send_to_influxdb("greenhouse_measurements", address, None, None, None, averaged_light, None, None, None, None)

        # bme280 sensors
        for address in bme280_addresses:
            temperature, humidity, pressure = bme280_sensors.read_sensor_data(address)
            if all(val is not None for val in [temperature, humidity, pressure]):
                averaged_temperature, averaged_humidity, averaged_pressure = bme280_sensors.average_sensor_data(3, address, temperature, humidity, pressure)
                
                # Add averaged temperature to the sum
                temp_in_sum += averaged_temperature
                count_temp += 1
                
                # Add averaged humitidy to the sum
                hum_in_sum += averaged_humidity
                count_hum += 1
                
                # if iteration % time_period == 0: 
                    # Send data to InfluxDB, omitting co2 and temperature_co2 if they are None
                    # logging_data.send_to_influxdb("greenhouse_measurements", address, averaged_temperature, averaged_pressure, averaged_humidity, None, None, None, None, None)
        
        # LT-1T-SDI12 sensor
        leaf_temp = leaf_sensor.read_sensor_data()
        if any(val is not None for val in [leaf_temp]):
            
            av_leaf_temp = leaf_sensor.average_sensor_data(3, leaf_temp)
            # if iteration % time_period == 0:
                # logging_data.send_to_influxdb("greenhouse_measurements", "inside", None, None, None, None, None, None, None, None, av_leaf_temp)
            
        # outdoor sensor with serial connection
        lux, temp, hum, ccs_co2, ccs_tvco2, co2, temp_co2  = outdoor_sensors.read_sensor_data()
        
        # Send the data to the database (InfluxDB)
        if any(val is not None for val in [lux, temp, hum, ccs_co2, ccs_tvco2, co2, temp_co2]):
            av_lux, av_temp, av_hum, av_ccs_co2, av_ccs_tvco2, av_co2, av_temp_co2 = outdoor_sensors.average_sensor_data(3, lux, temp, hum, ccs_co2, ccs_tvco2, co2, temp_co2)
        
            # Send data to InfluxDB, omitting co2 and temperature_co2 if they are None
            # if iteration % time_period == 0:
                # logging_data.send_to_influxdb("greenhouse_measurements", "outdoor", av_temp, None, av_hum, av_lux, av_co2, av_temp_co2, av_ccs_co2, av_ccs_tvco2)
        
        # Calculate the overall average temperature
        if count_light > 0 and count_temp > 0 and count_co2 > 0 and count_hum > 0:
            overall_average_light = (light_in_sum / count_light) * 0.0079               # information about the unit https://www.researchgate.net/post/Howto_convert_solar_intensity_in_LUX_to_watt_per_meter_square_for_sunlight#:~:text=The%20LUX%20meter%20is%20used,of%20the%20incident%20solar%20radiation.&text=multiply%20lux%20to%200.0079%20which%20give%20you%20value%20of%20w%2Fm2.
            overall_average_temperature = temp_in_sum / count_temp
            overall_average_humidity = hum_in_sum / count_hum
            overall_average_co2 = co2_in_sum / count_co2
            
            print(f"Overall average light: {overall_average_light}")
            print(f"Overall average temperature: {overall_average_temperature}")
            print(f"Overall average humidity: {overall_average_humidity}")
            print(f"Overall average co2: {overall_average_co2}")
        
        if publish_mqtt_flag == True:
            # Accumulate 5-minutes outdoor measurements
            sum_5_minutes_lux_out += av_lux * 0.0079
            sum_5_minutes_temp_out += av_temp
            sum_5_minutes_hum_out += av_hum
            sum_5_minutes_co2_out += av_co2
            
            # Accumulate 5-minutes indoor measurements
            sum_5_minutes_lux_in += overall_average_light
            sum_5_minutes_temp_in += overall_average_temperature
            sum_5_minutes_hum_in += overall_average_humidity
            sum_5_minutes_co2_in += overall_average_co2
            sum_5_minutes_leaf_temp += av_leaf_temp
            
            count_5_minutes += 1
            
            # Calculate and send 5-minutes average data

            # if (current_time - last_5_minutes).seconds >= 300:
            if (current_time - last_5_minutes).seconds >= 3:
                
                # Count if exceed 4 times then it is equal to 20 minutes
                count_time_measurements += 1
                print("COUNT TIME MEASUREMENTS : ", count_time_measurements)
                
                # Average the data 
                avg_5_minutes_lux_out = sum_5_minutes_lux_out / count_5_minutes
                avg_5_minutes_temp_out = sum_5_minutes_temp_out / count_5_minutes
                avg_5_minutes_hum_out = sum_5_minutes_hum_out / count_5_minutes
                avg_5_minutes_co2_out = sum_5_minutes_co2_out / count_5_minutes
                
                avg_5_minutes_lux_in = sum_5_minutes_lux_in / count_5_minutes
                avg_5_minutes_temp_in = sum_5_minutes_temp_in / count_5_minutes
                avg_5_minutes_hum_in = sum_5_minutes_hum_in / count_5_minutes
                avg_5_minutes_co2_in = sum_5_minutes_co2_in / count_5_minutes
                avg_5_minutes_leaf_temp = sum_5_minutes_leaf_temp / count_5_minutes
                
                # Reset 5-minutes accumulators
                sum_5_minutes_lux_out = 0
                sum_5_minutes_temp_out = 0
                sum_5_minutes_hum_out = 0
                sum_5_minutes_co2_out = 0
                
                sum_5_minutes_lux_in = 0
                sum_5_minutes_temp_in = 0
                sum_5_minutes_hum_in = 0
                sum_5_minutes_co2_in = 0
                sum_5_minutes_leaf_temp = 0
                
                count_5_minutes = 0
                
                last_5_minutes = current_time
                
                print("5-minutes averages outdoor:", avg_5_minutes_lux_out, avg_5_minutes_temp_out, avg_5_minutes_hum_out, avg_5_minutes_co2_out)
                print("5-minutes averages indoor:", avg_5_minutes_lux_in, avg_5_minutes_temp_in, avg_5_minutes_hum_in, avg_5_minutes_co2_in, avg_5_minutes_leaf_temp)
                
                # Appending the new measurements to the list
                calculate_time = count_time_measurements * 300
                time_measurements.append(calculate_time)
                
                # Append twice because the DRL model need 4 data but in real experiment only need 3
                # Outdoor measurements
                handle_nan_and_append(lux_outdoor_measurements, avg_5_minutes_lux_out)
                handle_nan_and_append(temp_outdoor_measurements, avg_5_minutes_temp_out)
                handle_nan_and_append(hum_outdoor_measurements, avg_5_minutes_hum_out)
                handle_nan_and_append(co2_outdoor_measurements, avg_5_minutes_co2_out)

                # Indoor measurements
                handle_nan_and_append(lux_indoor_measurements, avg_5_minutes_lux_in)
                handle_nan_and_append(temp_indoor_measurements, avg_5_minutes_temp_in)
                handle_nan_and_append(hum_indoor_measurements, avg_5_minutes_hum_in)
                handle_nan_and_append(co2_indoor_measurements, avg_5_minutes_co2_in)
                handle_nan_and_append(leaf_temp_measurements, avg_5_minutes_leaf_temp)
                
                print("TIME OUTDOOR MEASUREMENTS: ", time_measurements)
                print("LUX OUTDOOR MEASUREMENTS: ", lux_outdoor_measurements[-4:])
                print("TEMP OUTDOOR MEASUREMENTS: ", temp_outdoor_measurements[-4:])
                print("HUM OUTDOOR MEASUREMENTS: ", hum_outdoor_measurements[-4:])
                print("CO2 OUTDOOR MEASUREMENTS: ", co2_outdoor_measurements[-4:])
                
                print("LUX INDOOR MEASUREMENTS: ", lux_indoor_measurements[-4:])
                print("TEMP INDOOR MEASUREMENTS: ", temp_indoor_measurements[-4:])
                print("HUM INDOOR MEASUREMENTS: ", hum_indoor_measurements[-4:])
                print("CO2 INDOOR MEASUREMENTS: ", co2_indoor_measurements[-4:])
                print("LEAF TEMP INDOOR MEASUREMENTS: ", leaf_temp_measurements[-4:])
                
                if count_time_measurements == 4:
                    
                    # Count 
                    count_publish_mqtt_flag += 1
                    print("COUNT PUBLISH MQTT FLAG : ", count_publish_mqtt_flag)
                    
                    # Change publish and subscribe flags               
                    publish_mqtt_flag = False
                    subscribe_mqtt_flag = True
                    
                    # Reset count_time_measurements
                    count_time_measurements = 0
                    
                    # Format data into JSON format
                    json_data = mqtt_comm.format_data_in_JSON(time_measurements, \
                                                            lux_outdoor_measurements[-4:], \
                                                            lux_indoor_measurements[-4:], \
                                                            temp_outdoor_measurements[-4:], \
                                                            temp_indoor_measurements[-4:], \
                                                            hum_outdoor_measurements[-4:], \
                                                            hum_indoor_measurements[-4:], \
                                                            co2_outdoor_measurements[-4:], \
                                                            co2_indoor_measurements[-4:], \
                                                            leaf_temp_measurements[-4:])
                                
                    # Publish it to the server
                    mqtt_comm.publish_mqtt_data(json_data)
                    
                    # Reset the outdoor measurements
                    # List for the outdoor measurements
                    time_measurements = []
                    # lux_outdoor_measurements = []
                    # temp_outdoor_measurements = []
                    # hum_outdoor_measurements = []
                    # co2_outdoor_measurements = []
                    
                    # lux_indoor_measurements = []
                    # temp_indoor_measurements = []
                    # hum_indoor_measurements = []
                    # co2_indoor_measurements = []
                    # leaf_temp_measurements = []
                    
        if subscribe_mqtt_flag == True and controls_flag == True:
            drl_time, drl_ventilation, drl_toplights, drl_heater = mqtt_comm.subscribe_mqtt_data()
            
            print("")
            print("ACTIONS OR CONTROLS FROM PC SERVER!")
            print("drl_time : ", drl_time)
            print("drl_ventilation : ", drl_ventilation)
            print("drl_lamps : ", drl_toplights)
            print("drl_heater : ", drl_heater)
            print("")
            
            # Change flags for the MQTT and controls
            publish_mqtt_flag = True
            subscribe_mqtt_flag = False
            controls_flag = False
            
            '''
            TO-DO: Turn on the actuators based on the actions from DRL model
            '''
            
            # Take the controls variables, to control the actuators
            # There are 4 data or [0, 1, 2, 3]
            # But we only use the first one, because all of it the same for 15 minutes
            current_ventilation = drl_ventilation[0]
            current_lamps = drl_toplights[0]
            current_heater = drl_heater[0]
            
            # Turn on or off the actuators based on the controls
            # Control ventilation/fan
            if current_ventilation > 0.0:
                print("VENTILATION TURN ON!")
                FAN_actuator.actuate_FAN(100) # Turn on FAN
            else:
                print("VENTILATION TURN OFF")
                FAN_actuator.actuate_FAN(0)   # Turn off FAN
                
            # Control lamps/LED Strip
            if current_lamps > 0.0:
                print("TOPLIGHTS TURN ON!")
                LEDStrip_actuator.LED_ON(100) # Turn on LED
            else:
                print("TOPLIGHTS TURN OFF!")
                LEDStrip_actuator.LED_ON(0)  # Turn off LED
                
            # Control heater
            if current_heater > 0.0:
                print("HEATER TURN ON!")
                HEATER_actuator.actuate_GPIO_HIGH()     # Turn heater on
                FAN_HEATER_actuator.actuate_GPIO_HIGH() # Turn FAN heater on
            else:
                print("HEATER TURN OFF!")
                HEATER_actuator.actuate_GPIO_LOW()     # Turn heater off
                FAN_HEATER_actuator.actuate_GPIO_LOW() # Turn FAN heater off
            
        # Calculate 20-minutes interval
        # if (current_time - last_20_minutes).seconds >= 1200:
        if (current_time - last_20_minutes).seconds >= 12:
            last_20_minutes = current_time
            controls_flag = True
            print("CONTROLS FLAG TRUE!!")
                
except KeyboardInterrupt:
    # Clean up all the GPIOs
    LEDStrip_actuator.GPIO_cleanup()
    LEDBlink_actuator.GPIO_cleanup()
    FAN_actuator.GPIO_cleanup()
    HEATER_actuator.GPIO_cleanup()
    FAN_HEATER_actuator.GPIO_cleanup()
    
    print('Program stopped')
    
except Exception as e:
    print('An unexpected error occurred:', str(e))
