'''
Author: Efraim Manurung
Information Technology Group, Wageningen University

v1.0: Make a simple class for the FAN actuator
'''

import RPi.GPIO as GPIO

class ActuatorFAN:
    def __init__ (self, FAN_GPIO, _frequency):
        self.choosen_pin = FAN_GPIO
        
        print("ActuatorFAN Start!")
        # Set up GPIO mode
        GPIO.setmode(GPIO.BCM)
        
        # Set up GPIO pin
        GPIO.setup(self.choosen_pin, GPIO.OUT)
        
        # Set up PWM pin
        self._PWM = GPIO.PWM(self.choosen_pin, _frequency)
        
        # Start the PWM pin with 0% duty cycle
        self._PWM.start(0)
    
    def actuate_FAN(self, duty_cycle):
        self._PWM.ChangeDutyCycle(duty_cycle)
    
    def GPIO_cleanup(self):
        GPIO.cleanup()
        
        
        
        

