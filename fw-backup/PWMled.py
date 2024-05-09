import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(13, GPIO.OUT) # LED Strip
# GPIO.setup(16, GPIO.OUT) # FAN Strip

p = GPIO.PWM(13, 60)  # channel=13 frequency=60Hz
# p1 = GPIO.PWM(16, 60) # channel=16 frequency=60Hz

p.start(100)
# p1.start(100)

print("START LED PWM")
time.sleep(2)
try:
    while 1:
        for dc in range(0, 101, 10):
            print("dc up: ", dc)
            p.ChangeDutyCycle(dc)
            #p1.ChangeDutyCycle(dc)
            time.sleep(0.5)
        for dc in range(100, -1, -10):
            print("dc down: ", dc)
            p.ChangeDutyCycle(dc)
            #p1.ChangeDutyCycle(dc)
            time.sleep(0.5)
except KeyboardInterrupt:
    pass
p.stop()
GPIO.cleanup()

# import RPi.GPIO as GPIO
# GPIO.setmode(GPIO.BCM)
# GPIO.setup(13, GPIO.OUT)

# p = GPIO.PWM(13, 0.5)
# p.start(50)
# input('Press return to stop:')   # use raw_input for Python 2
# p.stop()
# GPIO.cleanup()