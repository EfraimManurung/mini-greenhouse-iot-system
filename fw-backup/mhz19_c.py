#!/usr/bin/python
# FT232R+MH-Z19B Python3

import serial
import time
import sys

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

# try to open serial port
# port = '/dev/serial0'
port = '/dev/ttyAMA0'

sys.stderr.write('Trying port %s\n' % port)

try:
    # try to read a line of data from the serial port and parse
    with serial.Serial(port, 9600, timeout=2.0) as ser:
        # 'warm up' with reading one input
        #result = ser.write(b"\xff\x01\x86\x00\x00\x00\x00\x00\x79")
        result=ser.write(b"xffx01x86x00x00x00x00x00x79")
        time.sleep(0.1)
        s = ser.read(9)
        z = bytearray(s)
        # Calculate crc
        crc = crc8(s)
        if crc != z[8]:
            sys.stderr.write('CRC error calculated %d bytes= %d:%d:%d:%d:%d:%d:%d:%d crc= %d\n' % (
            crc, z[0], z[1], z[2], z[3], z[4], z[5], z[6], z[7], z[8]))
        else:
            while True:
                # Send "read value" command to MH-Z19 sensor
                #result = ser.write(b"\xff\x01\x86\x00\x00\x00\x00\x00\x79")
                result=ser.write(b"xffx01x86x00x00x00x00x00x79")
                time.sleep(0.1)
                s = ser.read(9)
                z = bytearray(s)
                crc = crc8(s)
                # Calculate crc
                if crc != z[8]:
                    sys.stderr.write('CRC error calculated %d bytes= %d:%d:%d:%d:%d:%d:%d:%d crc= %d\n' % (
                    crc, z[0], z[1], z[2], z[3], z[4], z[5], z[6], z[7], z[8]))
                else:
                    if s[0] == 0xff and s[1] == 0x86:
                        co2 = (s[2] * 256) + s[3]
                        print("CO2:", co2)
                # Sample every 10s, synced to local time
                measuretime = 10
                time.sleep(measuretime)
except Exception as e:
    sys.stderr.write('Error reading serial port %s: %s\n' % (type(e).__name__, e))
except KeyboardInterrupt:
    sys.stderr.write('Ctrl+C pressed, exiting\n')
