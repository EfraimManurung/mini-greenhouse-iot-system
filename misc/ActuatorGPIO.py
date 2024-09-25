'''
Author: Efraim Manurung
Information Technology Group, Wageningen University
 
efraim.manurung@gmail.com
'''

import RPi.GPIO as GPIO

class ActuatorGPIO:
    def __init__ (self, SERVO_GPIO):
        self.choosen_pin = SERVO_GPIO
        
        print("ActuatorGPIO Start!")
        # Set up GPIO mode
        GPIO.setmode(GPIO.BCM)
        
        # Set up GPIO pin
        GPIO.setup(self.choosen_pin, GPIO.OUT)
        
    def actuate_GPIO_HIGH(self):
        GPIO.output(self.choosen_pin, GPIO.LOW)
    
    def actuate_GPIO_LOW(self):
        GPIO.output(self.choosen_pin, GPIO.HIGH)
    
    def GPIO_cleanup(self):
        GPIO.cleanup()
        

