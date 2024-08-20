'''
Author: Efraim Manurung
Information Technology Group, Wageningen University
efraim.efraimpartoginahotasi@wur.nl
efraim.manurung@gmail.com

Project source: https://github.com/AnaviTechnology/anavi-examples/blob/master/sensors/BH1750/python/bh1750.py
'''
# import relevant libraries
import time
import os

class SensorBh1750:
    def __init__(self, bus):
        # Rev 2 of Raspberry Pi and all newer use bus 1
        self.bus = bus
        print("SensorBh1750 Start!")
    
    def read_sensor_data(self, address):
        try:
            # Read sensor data
            data = self.bus.read_i2c_block_data(address, 0x10, 2)
            result = (data[1] + (256 * data[0])) / 1.2
            light = format(result, '.0f') 
            
            # For debugging
            # print("Light Intensity (Lux): ", light)
            
        except Exception as e:
            print('ERROR BH1750: An unexpected bh1750 error occurred at address 0x{:02X}:'.format(address), str(e))
            light = None
        except OSError:
            print('ERROR BH1750: bh1750 I2C device not found. Please check bh1750 wiring.')
            light = None
        except:
            print('ERROR BH1750: General unknown error')
            light = None
        
        return light

    def average_sensor_data(self, _count, address, light):
        count = _count
        light_total = 0
        valid_samples = 0  # Counter for valid samples
        
        if light is None:
            print("No valid data to average from sensor at address 0x{:02X}".format(address))
            return None

        try:
            light = float(light)  # Convert to float if it's a string
        except ValueError:
            print("ERROR: Invalid value for light:", light)
            return None
        
        for x in range(count):
            light_total += light
            valid_samples += 1
            time.sleep(0.2)
        
        _averaged_light = light_total / valid_samples if valid_samples != 0 else None
        
        if _averaged_light is not None:
            print("AVERAGED VALUES from Address 0x{:02x}, Av_Light={:.2f} lux".format(address, _averaged_light))
        
        return _averaged_light 