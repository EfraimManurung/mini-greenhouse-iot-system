'''
Author: Efraim Manurung
Information Technology Group, Wageningen University

10 April 2024
v1.0: Make a simple class for the SERVO actuator
'''

import RPi.GPIO as GPIO

class ActuatorSERVO:
    def __init__ (self, SERVO_GPIO, _frequency):
        self.choosen_pin = SERVO_GPIO
        
        print("ActuatorSERVO Start!")
        # Set up GPIO mode
        GPIO.setmode(GPIO.BCM)
        
        # Set up GPIO pin
        GPIO.setup(self.choosen_pin, GPIO.OUT)
        
        # Set up PWM pin
        self._PWM = GPIO.PWM(self.choosen_pin, _frequency)
        
        # Start the PWM pin with 0% duty cycle
        self._PWM.start(0)
    
    # def actuate_window_open(self, duty_cycle_open = 12):
    #     print("WINDOW OPEN!")
    #     self._PWM.ChangeDutyCycle(duty_cycle_open)
        
    def actuate_SERVO(self, current_value, set_point, duty_cycle):
        print("CURRENT VALUE  CO2: {:.2f} ppm".format(current_value))
        print("SET POINT VALUE CO2: {:.2f} ppm".format(set_point))
        
        if current_value > set_point:
            self._PWM.ChangeDutyCycle(duty_cycle)
            print("WINDOW OPEN!!")
        else:
            self._PWM.ChangeDutyCycle(2)
            print("WINDOW CLOSE!!")
    
    def close_window(self, duty_cycle):
        print("FORCE CLOSE WINDOW!!")
        self._PWM.ChangeDutyCycle(duty_cycle)
        
        

