'''
Author: Efraim Manurung
Information Technology Group, Wageningen University
efraim.efraimpartoginahotasi@wur.nl
efraim.manurung@gmail.com

Project source https://pypi.org/project/mh-z19/

v1.0: Encapsulate mh_z19 class from the project source
'''
import time
import os
import mh_z19

class SensorMhz19:
    def __init__(self, UART_address):
        self.UART_address = UART_address
        mh_z19.set_serialdevice(UART_address)
        mh_z19.detection_range_5000()
        print("SensorMhz19 Start!")
        
    def read_sensor_data(self):
        try:
            # Read all co2 sensor values
            sensor_data = mh_z19.read_all()
        
            # Extract CO2 and temperature
            co2 = sensor_data['co2']
            temperature = sensor_data['temperature']
            
        except Exception as e:
            print('ERROR MHZ19: An unexpected mhz19c error occurred at address 0x{}:'.format(self.UART_address), str(e))
            co2 = None
            temperature = None
        
        return co2, temperature
    
    def average_sensor_data(self, _count, co2_value, temp_value):
        count = _count
        co2_value_total = 0
        temp_value_total = 0
        valid_samples = 0  # Counter for valid samples

        for x in range(count):
            if co2_value is not None:
                co2_value_total += co2_value
                valid_samples += 1
            if temp_value is not None:
                temp_value_total += temp_value
                valid_samples += 1
            time.sleep(1)

        _averaged_co2 = co2_value_total / valid_samples if valid_samples != 0 else None
        _averaged_temp = temp_value_total / valid_samples if valid_samples != 0 else None

        if _averaged_co2 is not None and _averaged_temp is not None:
            print("Averaged VALUES from CO2 {}, Av_CO2={:.2f} ppm, Av_Temp={:.2f}".format(
                self.UART_address, _averaged_co2, _averaged_temp))
        else:
            print("No valid data to average from CO2 sensor at address {}".format(self.UART_address))

        return _averaged_co2, _averaged_temp

    def write_sensor_data(self, _averaged_co2, _averaged_temp):
        # Check if the file exists before opening it in 'a' mode (append mode)
        file_exists = os.path.isfile('sensor_readings_mhz19c.txt')
        
        # Open the file using a context manager
        with open('sensor_readings_mhz19c.txt', 'a') as file:
            # Write the header to the file if the file does not exist
            if not file_exists:
                file.write('Time and Data, co2(ppm), temperature(ºC)\n')
            
            # Write sensor data to the file
            file.write(time.strftime('%H:%M:%S %d/%m/%Y') + ', {:.2f}, {:.2f}\n'.format(_averaged_co2, _averaged_temp))
