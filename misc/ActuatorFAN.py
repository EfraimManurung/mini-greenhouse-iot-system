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
        
    def actuate_FAN(self, current_value, set_point, duty_cycle):
        print("CURRENT VALUE  HUM(%) OR TEMP(°C): {:.2f}".format(current_value))
        print("SET POINT  HUM(%) OR TEMP(°C): {:.2f}".format(set_point))
        
        if current_value > set_point:
            self._PWM.ChangeDutyCycle(duty_cycle)
            print("FAN TURN ON!!")
        else:
            self._PWM.ChangeDutyCycle(0)
            print("FAN TURN OFF!!")
        
        
        
        

