import time
import board
import busio

import adafruit_gps

# Create a serial connection for the GPS connection using default speed and
# a slightly higher timeout (GPS modules typically update once a second).
# These are the defaults you should use for the GPS FeatherWing.
# For other boards set RX = GPS module TX, and TX = GPS module RX pins.
#uart = busio.UART(board.TX, board.RX, baudrate=9600, timeout=10)

# for a computer, use the pyserial library for uart access
import serial
uart = serial.Serial("/dev/ttyUSB0", baudrate=9600, timeout=10)

# If using I2C, we'll create an I2C interface to talk to using default pins
#i2c = busio.I2C(board.SCL, board.SDA)

# Create a GPS module instance.
gps = adafruit_gps.GPS(uart) 

def getPositionData(gps):
        nx=gpsd.next()
        if nx['class'] == 'TPV':
            latitude = getattr(nx, 'lat',"Unknown")
            longitude = getattr(nx, 'lon', "Unknown")
            GPStime= getattr(nx,'time',"Unknown")
            print("Your postion: lon= " +str(longitude))
