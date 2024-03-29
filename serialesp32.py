#!/usr/bin/env python3
# import serial

# if __name__ == '__main__':
#     ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
#     ser.reset_input_buffer()

#     while True:
#         if ser.in_waiting > 0:
#             line = ser.readline().decode('utf-8').rstrip()
#             print(line)

#!/usr/bin/env python3
import serial

if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
    ser.reset_input_buffer()

    co2_value = None
    temp_value = None

    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip()
            if line.startswith("co2: "):
                co2_value = float(line.split(" ")[1])
            elif line.startswith("temp: "):
                temp_value = float(line.split(" ")[1])
            
            # If both CO2 and temperature values are received, print and reset variables
            if co2_value is not None and temp_value is not None:
                print("CO2:", co2_value)
                print("Temperature:", temp_value)
                co2_value = None
                temp_value = None

