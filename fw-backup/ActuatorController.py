'''
Author: Efraim Manurung
Information Technology Group, Wageningen University
 
efraim.manurung@gmail.com

Project source: 
https://github.com/m-lundberg/simple-pid/tree/master
https://github.com/m-lundberg/simple-pid/blob/master/examples/water_boiler/water_boiler.py
https://github.com/br3ttb/Arduino-PID-Library/blob/master/examples/PID_RelayOutput/PID_RelayOutput.ino
'''

from simple_pid import PID
import time

# input from the user window_size = 5000

class ActuatorController:
    
    def __init__(self, kp, ki, kd, setpoint, window_size):
        print("ActuatorController start!")
        self._pid = PID(kp, ki, kd, setpoint=setpoint)
        self._pid.output.limits = (0, window_size)
        self.window_size = window_size
        self.window_start_time = time.time() * 1000 # in milliseconds
         
    def PID_control(self, current_value):
        output = self._pid(current_value)
        return output
    

        