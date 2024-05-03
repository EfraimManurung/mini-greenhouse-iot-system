import serial

if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
    ser.reset_input_buffer()

    print("TRUE!")
    
    lux_value = None
    temp_value = None
    hum_value = None
    ccs_co2_value = None
    ccs_tvco2_value = None
    co2_value = None
    temp_co2_value = None

    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip()
            if line.startswith("lux: "):
                lux_value = float(line.split(" ")[1])
            elif line.startswith("temp: "):
                temp_value = float(line.split(" ")[1])
            elif line.startswith("hum: "):
                hum_value = float(line.split(" ")[1])
            elif line.startswith("ccs_co2: "):
                ccs_co2_value = float(line.split(" ")[1])
            elif line.startswith("ccs_tvco2: "):
                ccs_tvco2_value = float(line.split(" ")[1])
            elif line.startswith("co2: "):
                co2_value = float(line.split(" ")[1])
            elif line.startswith("temp_co2: "):
                temp_co2_value = float(line.split(" ")[1])
            
            # If both CO2 and temperature values are received, print and reset variables
            if lux_value is not None and temp_value is not None and hum_value is not None and ccs_co2_value is not None and ccs_tvco2_value is not None and co2_value is not None and temp_co2_value is not None:
                print("lux: ", lux_value)
                print("temp: ", temp_value)
                print("hum: ", hum_value)
                print("CCS_CO2: ", ccs_co2_value)
                print("CCS_TVCO2: ", ccs_tvco2_value)
                print("CO2: ", co2_value)
                print("TEMP_CO2: ", temp_co2_value)
                print("")
                
                lux_value = None
                temp_value = None
                hum_value = None
                ccs_co2_value = None
                ccs_tvco2_value = None
                co2_value = None
                temp_co2_value = None
