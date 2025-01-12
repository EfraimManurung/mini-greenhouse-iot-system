import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

# Ventilation
GPIO.setup(26, GPIO.OUT)

# Toplights
GPIO.setup(17, GPIO.OUT)

# Heater and heater fan
GPIO.setup(5, GPIO.OUT)
GPIO.setup(6, GPIO.OUT)

fan  = GPIO.PWM(26, 50)
ledStrip = GPIO.PWM(17, 50)

# Heater and heater fan
GPIO.output(5, GPIO.LOW)
GPIO.output(6, GPIO.LOW)

fan.start(100)
ledStrip.start(100)

while True:
    print("Debugging")