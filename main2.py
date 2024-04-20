from misc.OutdoorSensors import OutdoorSensors

outdoor_sensors = OutdoorSensors()
averaged_data = outdoor_sensors.average_sensor_data(5)
print(*averaged_data)