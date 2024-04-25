'''
Author: Efraim Manurung
Information Technology Group, Wageningen University
efraim.efraimpartoginahotasi@wur.nl
efraim.manurung@gmail.com

Project source:
https://sandyjmacdonald.github.io/2021/12/29/setting-up-influxdb-and-grafana-on-the-raspberry-pi-4/
https://sandyjmacdonald.github.io/2021/12/29/logging-raspberry-pi-environmental-data-to-influxdb/

'''

# import libraries
import datetime
import pytz  # Import the pytz module for timezone manipulation
from influxdb import InfluxDBClient

# Set up InfluxDB
# host = '192.168.1.131'  # Change this as necessary
host = 'localhost'
port = 8086
username = ''  # Change this as necessary
password = ''  # Change this as necessary
db = 'greenhouse_iot_database'  # Change this as necessary

# InfluxDB client to write to
client = InfluxDBClient(host, port, username, password, db)

class LoggingData:
    def __init__(self):
        print("LoggingData Start!")
    
    # Logs the data to your InfluxDB
    def send_to_influxdb(self, measurement = None, location = None, temperature = None, pressure = None, 
                         humidity = None , light = None, co2 = None, temperature_co2 = None, tank_temperature = None):
        # Get the current UTC timestamp
        timestamp = datetime.datetime.now(datetime.timezone.utc)

        # Add 2 hours to the UTC timestamp
        # timestamp = utc_timestamp + datetime.timedelta(hours=2)
        
        # Create the payload
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
                    "light": light,
                    "co2": co2,
                    "co2_temp": temperature_co2,
                    "tank_temp": tank_temperature
                }
            }
        ]
        
        # Print the payload
        print("Payload:", payload)
        
        # Write data to InfluxDB
        client.write_points(payload)