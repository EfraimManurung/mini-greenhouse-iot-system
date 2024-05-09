import serial
import time

# ser = serial.Serial('/dev/serial0', 9600)  # Adjust baud rate as necessary
ser = serial.Serial('/dev/ttyAMA0', 9600)

print("WORK1")
try:
    while True:
        print("WORK2")
        if ser.in_waiting > 0:
            received_data = ser.readline().decode('utf-8').rstrip()
            print("WORK3")
            print("Raspberry Pi received:", received_data)
            
        ser.write(b"Hello from Raspberry Pi!\n")
        time.sleep(1)

except KeyboardInterrupt:
    ser.close()
