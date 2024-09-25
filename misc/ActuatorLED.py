'''
Author: Efraim Manurung
Information Technology Group, Wageningen University
 
efraim.manurung@gmail.com
'''

import RPi.GPIO as GPIO

class ActuatorLED:
    def __init__ (self, LED_GPIO, _frequency):
        self.choosen_pin = LED_GPIO
        
        print("ActuatorLED Start!")
         # Set up GPIO mode
        GPIO.setmode(GPIO.BCM)
        
        # Set up GPIO pin
        GPIO.setup(self.choosen_pin, GPIO.OUT)
        
        # Set up PWM pin
        self._PWM = GPIO.PWM(self.choosen_pin, _frequency)
        
        # Start the PWM pin with 0% duty cycle
        self._PWM.start(0)
        
    def LED_ON(self, duty_cycle):
        self._PWM.ChangeDutyCycle(duty_cycle)
        
    def GPIO_cleanup(self):
        GPIO.cleanup()
        
        
        

