'''
Author: Efraim Manurung
Information Technology Group, Wageningen University

v1.0: Make a simple class for the LED actuator
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
        
    def actuate_LED(self, current_value, set_point, duty_cycle):
        print("CURRENT VALUE LIGHT: ", current_value)
        print("SET POINT LIGHT: ", set_point)
        
        if current_value < set_point:
            self._PWM.ChangeDutyCycle(duty_cycle)
            print("LIGHT TURN ON!!")
        else:
            self._PWM.ChangeDutyCycle(0)
            print("LIGHT TURN OFF!!")
    
    def blink_LED(self, duty_cycle):
        # Start the PWM pin set as 50% so it can blink 
        self._PWM.start(duty_cycle)
    
    def stop_blink_LED(self):
        # Stop the PWM pin 
        self._PWM.stop()
    
    # def clean_LED(self):
    #     GPIO.cleanup
        
        
        

