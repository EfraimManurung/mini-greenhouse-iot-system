'''
Author: Efraim Manurung
Information Technology Group, Wageningen University

v1.0: Make a simple class for the actuator
'''

import RPi.GPIO as GPIO
import time

class ActuatorLED:
    def __init__ (self, LED_GPIO):
        self.choosen_pin = LED_GPIO
        
        print("ActuatorLED Start!")
        # Set up GPIO mode
        GPIO.setmode(GPIO.BCM)
        
        # Set up GPIO pin
        GPIO.setup(self.choosen_pin, GPIO.OUT)
        
    def actuate_LED(self, current_value, set_point):
        if current_value < set_point:
            GPIO.output(self.choosen_pin, GPIO.HIGH)
        else:
            GPIO.output(self.choosen_pin, GPIO.LOW)
        
        

