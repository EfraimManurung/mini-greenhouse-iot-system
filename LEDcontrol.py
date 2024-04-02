# import RPi.GPIO as GPIO
# import time

# # Set up GPIO mode
# GPIO.setmode(GPIO.BCM)

# # Set up GPIO pin
# GPIO.setup(26, GPIO.OUT)

# try:
#     while True:
#         # Turn GPIO pin 4 on (HIGH)
#         GPIO.output(26, GPIO.HIGH)
#         print("GPIO 26 is HIGH")
        
#         # Wait for 5 seconds
#         time.sleep(1)
        
#         # Turn GPIO pin 4 off (LOW)
#         GPIO.output(26, GPIO.LOW)
#         print("GPIO 26 is LOW")
        
#         # Wait for 5 seconds
#         time.sleep(1)

# finally:
#     # Clean up GPIO
#     GPIO.cleanup()

#Import all neccessary features to code.
import RPi.GPIO as GPIO
from time import sleep

#If code is stopped while the solenoid is active it stays active
#This may produce a warning if the code is restarted and it finds the GPIO Pin, which it defines as non-active in next line, is still active
#from previous time the code was run. This line prevents that warning syntax popping up which if it did would stop the code running.
GPIO.setwarnings(False)
#This means we will refer to the GPIO pins
#by the number directly after the word GPIO. A good Pin Out Resource can be found here https://pinout.xyz/
GPIO.setmode(GPIO.BCM)
#This sets up the GPIO 18 pin as an output pin
GPIO.setup(13, GPIO.OUT)

while (True):    
    
    #This Turns Relay Off. Brings Voltage to Max GPIO can output ~3.3V
    GPIO.output(13, 1)
    print("GPIO 13 is HIGH")
    #Wait 1 Seconds
    sleep(5)
    #Turns Relay On. Brings Voltage to Min GPIO can output ~0V.
    GPIO.output(13, 0)
    print("GPIO 13 is LOW")
    #Wait 1 Seconds
    sleep(5)