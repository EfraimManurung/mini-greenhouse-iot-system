import serial
import time
import sys
import datetime

# Function to calculate MH-Z19 crc according to datasheet
def crc8(a):
    crc = 0x00
    count = 1
    b = bytearray(a)
    while count < 8:
        crc += b[count]
        count += 1
    # Truncate to 8 bit
    crc %= 256
    # Invert number with xor
    crc = ~crc & 0xFF
    crc += 1
    return crc

try:
    # port = '/dev/ttyAMA10'
    port = '/dev/ttyAMA10'
    sys.stderr.write('Trying port %s\n' % port)
    
    with serial.Serial(port, 9600, timeout=2.0) as ser:
        # 'warm up' with reading one input
        result=ser.write(b"xffx01x86x00x00x00x00x00x79")
        time.sleep(0.1)
        s = ser.read(9)
        z = bytearray(s)
        # Calculate crc
        crc = crc8(s) 
        if crc != z[8]:
            sys.stderr.write('CRC error calculated %d bytes= %d:%d:%d:%d:%d:%d:%d:%d crc= %d\n' % (crc, z[0], z[1], z[2], z[3], z[4], z[5], z[6], z[7], z[8]))
        else:
            sys.stderr.write('Logging data on %s\n' % port)
            
        # loop will exit with Ctrl-C, which raises a KeyboardInterrupt
        while True:
            # Send "read value" command to MH-Z19 sensor
            result=ser.write(b"xffx01x86x00x00x00x00x00x79")
            time.sleep(0.1)
            s = ser.read(9)
            z = bytearray(s)
            crc = crc8(s)
            # Calculate crc
            if crc != z[8]:
                sys.stderr.write('CRC error calculated %d bytes= %d:%d:%d:%d:%d:%d:%d:%d crc= %d\n' % (crc, z[0], z[1], z[2], z[3], z[4], z[5], z[6], z[7], z[8]))
            else:       
                if s[0] == 0xFF and s[1] == 0x86:
                    co2 = ord(s[2]) * 256 + ord(s[3])
                    print("CO2:", co2)
                    
            # Sample every minute, synced to local time
            t = datetime.datetime.now()
            sleeptime = 60 - t.second
            time.sleep(sleeptime)
except Exception as e:
    sys.stderr.write('Error reading serial port %s: %s\n' % (type(e).__name__, e))
except KeyboardInterrupt:
    sys.stderr.write('\nCtrl+C pressed, exiting log\n')
