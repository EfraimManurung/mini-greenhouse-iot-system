import serial
import time

class OutdoorSensors:
    def __init__(self, port='/dev/ttyUSB0', baudrate=9600):
        self.port = port
        self.baudrate = baudrate
        try:
            self.ser = serial.Serial(port, baudrate, timeout=1)
            self.ser.reset_input_buffer()
            print("OutdoorSensor Start!")
        except Exception as e:
            print(f"Error: Failed to initialize OutdoorSensors: {e}")
            self.ser = None

    def read_sensor_data(self):
        try:
            if self.ser is None:
                return None, None, None, None, None

            lux_value = None
            temp_value = None
            hum_value = None
            co2_value = None
            tvco2_value = None

            while True:
                if self.ser.in_waiting > 0:
                    line = self.ser.readline().decode('utf-8').rstrip()
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

                    # If all variables are received, return them
                    if all(v is not None for v in [lux_value, temp_value, hum_value, co2_value, tvco2_value]):
                        return lux_value, temp_value, hum_value, co2_value, tvco2_value
        except Exception as e:
            print(f"Error in reading sensor data: {e}")
            return None, None, None, None, None

    def average_sensor_data(self, _count, lux, temp, hum, co2, tvco2):
        try:
            if any(val is None for val in [lux, temp, hum, co2, tvco2]):
                return None, None, None, None, None

            lux_total = 0
            temp_total = 0
            hum_total = 0
            co2_total = 0
            tvco2_total = 0

            for _ in range(_count):
                lux_total += lux
                temp_total += temp
                hum_total += hum
                co2_total += co2
                tvco2_total += tvco2
                time.sleep(0.2)

            averaged_lux = lux_total / _count
            averaged_temp = temp_total / _count
            averaged_hum = hum_total / _count
            averaged_co2 = co2_total / _count
            averaged_tvco2 = tvco2_total / _count

            print("Averaged VALUES: lux={}, temp={}, hum={}, CO2={}, TVCO2={}".format(
                averaged_lux, averaged_temp, averaged_hum, averaged_co2, averaged_tvco2))

            return averaged_lux, averaged_temp, averaged_hum, averaged_co2, averaged_tvco2
        except Exception as e:
            print(f"Error in averaging sensor data: {e}")
            return None, None, None, None, None
