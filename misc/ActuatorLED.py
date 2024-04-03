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
        print("CURRENT VALUE : ", current_value)
        print("SET POINT : ", set_point)
        
        if current_value < set_point:
            GPIO.output(self.choosen_pin, GPIO.LOW)
            print("LIGHT TURN ON!!")
        else:
            GPIO.output(self.choosen_pin, GPIO.HIGH)
            print("LIGHT TURN OFF!!")
    
    def blink_LED(self, _count):
        for x in range (_count):
            GPIO.output(self.choosen_pin, GPIO.LOW)
            time.sleep(0.2)
            GPIO.output(self.choosen_pin, GPIO.HIGH)
            time.sleep(0.2)
        
        
        

