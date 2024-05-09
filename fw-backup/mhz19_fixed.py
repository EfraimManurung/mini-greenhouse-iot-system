import mh_z19

mh_z19.set_serialdevice("/dev/ttyAMA0")
mh_z19.detection_range_5000()

# Read all sensor values
sensor_data = mh_z19.read_all()

# Extract CO2 and temperature
co2 = sensor_data['co2']
temperature = sensor_data['temperature']

print("CO2:", co2)
print("Temperature:", temperature)
