import serial

if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
    ser.reset_input_buffer()

    lux_value = None
    temp_value = None
    hum_value = None
    co2_value = None
    tvco2_value = None

    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip()
            if line.startswith("lux: "):
                lux_value = float(line.split(" ")[1])
            elif line.startswith("temp: "):
                temp_value = float(line.split(" ")[1])
            elif line.startswith("hum: "):
                hum_value = float(line.split(" ")[1])
            elif line.startswith("co2: "):
                co2_value = float(line.split(" ")[1])
            elif line.startswith("tvco2: "):
                tvco2_value = float(line.split(" ")[1])
            
            # If both CO2 and temperature values are received, print and reset variables
            if lux_value is not None and temp_value is not None and hum_value is not None and co2_value is not None and tvco2_value is not None:
                print("lux: ", lux_value)
                print("temp: ", temp_value)
                print("hum: ", hum_value)
                print("CO2: ", co2_value)
                print("TVCO2: ", tvco2_value)
                print("")
                lux_value = None
                temp_value = None
                hum_value = None
                co2_value = None
                tvco2_value = None
