import RPi.GPIO as GPIO
import time

# The pin location of the sensor
hallsensor = 17

GPIO.setmode(GPIO.BCM)

GPIO.setup(26, GPIO.OUT)
GPIO.setup(hallsensor, GPIO.IN)

pwm = GPIO.PWM(26, 50)

# Variables used for calculations
NbTopsFan = 0
Calc = 0

# Definitions of the fans
# fanspace = [{'fantype': 0, 'fandiv': 1}, {'fantype': 1, 'fandiv': 2}, {'fantype': 2, 'fandiv': 8}]
# fan = 1

# Function to calculate RPM
def rpm_callback(channel):
    global NbTopsFan
    NbTopsFan += 1
    
# Add event detection to the hall sensor pin
GPIO.add_event_detect(hallsensor, GPIO.RISING, callback=rpm_callback)

pwm.start(100)

try:
    while True:
        NbTopsFan = 0
        # Wait for 1 second
        time.sleep(1)
        
        # Calculate RPM
        # Calc = (NbTopsFan * 60) / fanspace[fan]['fandiv']
        Calc = (NbTopsFan * 60) / 2
        
        # Print RPM
        print("{} rpm".format(Calc))
        Calc = 0

except KeyboardInterrupt:
    GPIO.cleanup()
