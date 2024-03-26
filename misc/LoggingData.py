# code sources: 
# https://sandyjmacdonald.github.io/2021/12/29/setting-up-influxdb-and-grafana-on-the-raspberry-pi-4/
# https://sandyjmacdonald.github.io/2021/12/29/logging-raspberry-pi-environmental-data-to-influxdb/
# import libraries
import time
import datetime
from influxdb import InfluxDBClient

# Set up InfluxDB
host = '192.168.1.228'  # Change this as necessary
port = 8086
username = ''  # Change this as necessary
password = ''  # Change this as necessary
db = 'greenhouse_database'  # Change this as necessary

# InfluxDB client to write to
client = InfluxDBClient(host, port, username, password, db)

class LoggingData:
    def __init__(self):
        print("InfluxDB Start!")
    
    # Logs the data to your InfluxDB
    def send_to_influxdb(self, measurement, location, temperature, pressure, humidity, light):
        timestamp = datetime.datetime.now(datetime.UTC)
        payload = [
            {"measurement": measurement,
                "tags": {
                    "location": location,
                },
                "time": timestamp,
                "fields": {
                    "temperature" : temperature,
                    "humidity": humidity,
                    "pressure": pressure,
                    "light": light
                }
            }
            ]
        client.write_points(payload)