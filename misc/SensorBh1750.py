# Source: https://github.com/AnaviTechnology/anavi-examples/blob/master/sensors/BH1750/python/bh1750.py
# import relevant libraries
import time
import os

class SensorBh1750:
    def __init__(self, bus):
        # Rev 2 of Raspberry Pi and all newer use bus 1
        self.bus = bus
    
    def read_sensor_data(self, address, command_read):
        try:
            # Read sensor data
            data = self.bus.read_i2c_block_data(address, command_read)
            result = (data[1] + (256 * data[0])) / 1.2
            light = format(result,'.0f') 
            
        except Exception as e:
            print('ERROR: An unexpected bh1750 error occurred at address 0x{:02X}:'.format(address), str(e))
            light = None
        except OSError:
            print('ERROR: bh1750 I2C device not found. Please check bh1750 wiring.')
        except:
            print('ERROR: General unknown error')
        
        return light
    
    def average_sensor_data(self, address, light):
        count = 10
        light_total = 0
        
        for x in range(count):
            light_total += light
            time.sleep(1)
        
        _averaged_light = light_total / count
        print("Averaged VALUES from Addres 0x{:02x}, Av_Light={:.2f} lux".format(address, light))
        
        return _averaged_light 
    
    def write_sensor_data(self, address, light):
        # Check if the file exists before opening it in 'a' mode (append mode)
        file_exists = os.path.isfile('sensor_readings_bh1750.txt')
        
        # Open the file using a context manager
        with open('sensor_readings_bh1750.txt', 'a') as file:
            # Write the header to the file if the file does not exist
            if not file_exists:
                file.write('Time and Data, sensor address, light(lux)\n')
            
            # Write sensor data to the file
            file.write(time.strftime('%H:%M:%S %d/%m/%Y') + ', 0x{:02X}, {:.2f}\n'.format(address, light))
            
        