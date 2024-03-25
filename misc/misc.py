# Miscellaneous functions to support the main loop

# Import libraries
import time

def average_sensor_data(address, temperature, humidity, pressure):
    count = 10
    temperature_total = 0
    humidity_total = 0
    pressure_total = 0
    
    for x in range(count):
        temperature_total += temperature
        humidity_total += humidity
        pressure_total += pressure
        time.sleep(1)
        # Print the readings on the shell
        # print("Count {0:.0f}, Address 0x{0:02X}, Temp_tot={1:0.1f}ºC, Humidity_tot={2:0.1f}, Pressure_tot={3:0.1f}".format(x, address, temperature_total, humidity_total, pressure_total))

    
    _averaged_temperature = temperature_total / count
    _averaged_humidity = humidity_total / count
    _averaged_pressure = pressure_total / count
    
    # Print the readings on the shell
    print("AVERAGED VALUES from Address 0x{:02X}, Av_Temp={:.2f}ºC, Av_Humidity={:.2f}, Av_Pressure={:.2f}".format(address, _averaged_temperature, _averaged_humidity, _averaged_pressure))

    return _averaged_temperature, _averaged_humidity, _averaged_pressure
