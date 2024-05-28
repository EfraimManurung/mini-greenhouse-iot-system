import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

GPIO.setup(26, GPIO.OUT)
GPIO.setup(17, GPIO.OUT)

fan  = GPIO.PWM(26, 50)
ledStrip = GPIO.PWM(17, 50)

fan.start(100)
ledStrip.start(100)

while True:
    print("Debugging")