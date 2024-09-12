import time
from misc.LeafSensor import LeafSensor


leaf_sensor = LeafSensor(port='/dev/ttyUSB1', baudrate=9600)

while(1):
    leaf_temp = leaf_sensor.read_sensor_data()
    print("leaf_temp: ", leaf_temp)