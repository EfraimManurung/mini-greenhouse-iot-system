# code sources: 
# https://sandyjmacdonald.github.io/2021/12/29/setting-up-influxdb-and-grafana-on-the-raspberry-pi-4/
# https://sandyjmacdonald.github.io/2021/12/29/logging-raspberry-pi-environmental-data-to-influxdb/

# import libraries
import datetime
import pytz  # Import the pytz module for timezone manipulation
from influxdb import InfluxDBClient

# Set up InfluxDB
host = '192.168.1.228'  # Change this as necessary
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
    def send_to_influxdb(self, measurement, location, temperature, pressure, humidity, light, co2, temperature_co2):
        # Get the current UTC timestamp
        timestamp_utc = datetime.datetime.now(datetime.timezone.utc)
        
        # Define the timezone you want to convert to (e.g., Europe/Amsterdam)
        target_timezone = pytz.timezone('Europe/Amsterdam')
        
        # Convert the UTC timestamp to the target timezone
        timestamp = timestamp_utc.astimezone(target_timezone)
        
        # Adjust the timestamp by one hour
        timestamp += datetime.timedelta(hours=1)
        
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
                    "co2_temp": temperature_co2
                }
            }
        ]
        
        # Print the payload
        print("Payload:", payload)
        
        # Write data to InfluxDB
        client.write_points(payload)