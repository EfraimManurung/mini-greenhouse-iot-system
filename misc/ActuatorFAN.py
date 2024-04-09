'''
Author: Efraim Manurung
Information Technology Group, Wageningen University

v1.0: Make a simple class for the FAN actuator
'''

import RPi.GPIO as GPIO
import time

class ActuatorFAN:
    def __init__ (self, LED_GPIO):
        self.choosen_pin = LED_GPIO
        
        print("ActuatorFAN Start!")
        # Set up GPIO mode
        GPIO.setmode(GPIO.BCM)
        
        # Set up GPIO pin
        GPIO.setup(self.choosen_pin, GPIO.OUT)
        
    def actuate_FAN(self, current_value, set_point):
        print("CURRENT VALUE  HUM(%) OR TEMP(°C): {:.2f}°C".format(current_value))
        print("SET POINT  HUM(%) OR TEMP(°C): {:.2f}".format(set_point))
        
        if current_value > set_point:
            GPIO.output(self.choosen_pin, GPIO.LOW)
            print("FAN TURN ON!!")
        else:
            GPIO.output(self.choosen_pin, GPIO.HIGH)
            print("FAN TURN OFF!!")
        
        
        
        

