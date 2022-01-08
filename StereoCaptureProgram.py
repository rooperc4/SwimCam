import numpy as np
import cv2 as cv
from datetime import datetime
import os
import os.path as path
import sqlite3
import ms5837
import time
import tsys01
import inspect
import board
import busio
import adafruit_gps
import serial
import RPi.GPIO as GPIO


GPIO.setmode(GPIO.BCM)
GPIO.setup(23,GPIO.OUT)
GPIO.output(23,GPIO.HIGH)

#gps connection
uart = serial.Serial("/dev/ttyUSB0", baudrate=9600, timeout=10)
gps = adafruit_gps.GPS(uart) 
gps.send_command(b'PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0')
gps.send_command(b'PMTK220,1000')
print("starting gps")
last_print=time.monotonic()
current1=time.monotonic()
while True:
    gps.update()
    current=time.monotonic()
    if current-last_print>=1.0:
        last_print=current
        if not gps.has_fix and current1-current>30:
            print("Waiting for fix...")
            current1=time.monotonic()
            continue
 #   print(str(round(gps.longitude,5)))
 #     print('Latitude: {0:.6f} degrees'.format(gps.latitude))
 #     print('Longitude: {0:.6f} degrees'.format(gps.longitude))
        break

print("starting depth sensor")
depthsensor = ms5837.MS5837_30BA(5) # Default I2C bus is 1 (Raspberry Pi 3)
depthsensor.init()
print("starting temperature sensor")
tempsensor = tsys01.TSYS01(5) # Specify I2C bus 0
tempsensor.init()

print("making directories and initiating database")
os.chdir("/home/camtrawl/Data")
date1=datetime.now().strftime('D%Y%m%d-T%H%M%S')
os.mkdir(date1)
os.chdir(date1)
os.mkdir("images")
os.mkdir("logs")
os.mkdir("settings")

print("make log files")
f=open('./logs/ImageLogger2.log','w+')
f.write("Hello")
f.close()

f=open('./logs/CamTrawlAcquisition.log','w+')
f.write('placeholder')
f.close()

os.mkdir("images/right")
os.mkdir("images/left")

right_dir="./images/right"
left_dir="./images/left"
EXTENSION="jpg"
right_name="R_IMX322USB"
left_name="L_IMX322USB" 
frame_interval=1000

file_name_format="{:05d}_D{:s}_{:s}.{:s}"
cap = cv.VideoCapture(0)
print( "Frame default resolution: (" +str(cap.get(cv.CAP_PROP_FRAME_WIDTH)) + "; " + str(cap.get(cv.CAP_PROP_FRAME_HEIGHT)) + ")")
cap.set(cv.CAP_PROP_FRAME_WIDTH,800)
cap.set(cv.CAP_PROP_FRAME_HEIGHT,600)
cap.set(cv.CAP_PROP_FPS,1)
print( "Frame default frame rate: (" +str(cap.get(cv.CAP_PROP_FPS)) + ")")
cap1 = cv.VideoCapture(4)
cap1.set(cv.CAP_PROP_FRAME_WIDTH,800)
cap1.set(cv.CAP_PROP_FRAME_HEIGHT,600)
cap1.set(cv.CAP_PROP_FPS,1)
print( "Frame default resolution: (" +str(cap.get(cv.CAP_PROP_FRAME_WIDTH)) + "; " +str(cap.get(cv.CAP_PROP_FRAME_HEIGHT)) + ")")

conn=sqlite3.connect('./logs/CamTrawlMetadata.db3')
c=conn.cursor()
c.execute('''CREATE TABLE async_data
                (time text,sensor_id text, header text,data text)''')
c.execute('''CREATE TABLE cameras
                (camera text,mac_address text, model text,label text,rotation text)''')
c.execute("INSERT INTO cameras VALUES (?,?,?,?,?)",('PiCam','NA', left_name ,'left','none'))
c.execute("INSERT INTO cameras VALUES (?,?,?,?,?)",('PiCam','NA', right_name ,'right','none'))
c.execute('''CREATE TABLE deployment_data
                (image_extension text,parameter_value text)''')
c.execute("INSERT INTO deployment_data VALUES (?,?)",('image_extension','jpg'))
c.execute('''CREATE TABLE dropped
                (number text,camera text, time text)''')
c.execute('''CREATE TABLE images
                (number text,camera text, time text, name text, exposure_us text)''')
c.execute('''CREATE TABLE sensor_data
                (number text,sensor_id text, header text, data text)''')
conn.commit()


GPIO.setup(16,GPIO.OUT)
GPIO.setup(18,GPIO.OUT)
print("Start lights")
GPIO.output(16,GPIO.HIGH)
print("collect data and images")
print("press q to stop execution")
frame_count = 0
GPIO.output(23,GPIO.LOW)

while(True):
    GPIO.output(18,GPIO.HIGH)
    gps.update()
    frame_count += 1
    for x in range(4):
        ret, frame = cap.read()
        ret1, frame1 = cap1.read()

    ret, frame = cap.read()
    ret1, frame1 = cap1.read()

    cv.imshow('frame',frame)  #show all frames
    cv.imshow('frame1', frame1)

    #date=datetime.now().strftime('%Y%m%d-T%H%M%S.%f')[:-3]
    date=datetime.now()
    dater=datetime.strftime(date,'%Y-%m-%d %H:%M:%S.%f')[:-3]
    date=datetime.strftime(date,'%Y%m%d-T%H%M%S.%f')[:-3]
    file_namer=file_name_format.format(frame_count,date,right_name,EXTENSION)
    file_path=path.normpath(path.join(right_dir,file_namer))
    cv.imwrite(file_path, frame) #write specific frames 

    #date=datetime.now().strftime('%Y%m%d-T%H%M%S.%f')[:-3]
    date=datetime.now()
    datel=datetime.strftime(date,'%Y-%m-%d %H:%M:%S.%f')[:-3]
    date=datetime.strftime(date,'%Y%m%d-T%H%M%S.%f')[:-3]
    file_namel=file_name_format.format(frame_count,date,left_name,EXTENSION)
    file_path=path.normpath(path.join(left_dir,file_namel))
    cv.imwrite(file_path, frame1)

    #Collect temperature
    tempsensor.read()
    temperature=str(round(tempsensor.temperature(),1))
    #Collect depth
    depthsensor.read()
    depth=str(round(depthsensor.pressure()/(9.80665*1023.6),2))
    dtemp=depthsensor.temperature()
    #Collect GPS
    if gps.update() == True:
        latitude=str(gps.latitude)
        longitude=str(gps.longitude)
        GPStime="{}/{}/{} {:02}:{:02}:{:02}".format(
                gps.timestamp_utc.tm_mon,  # Grab parts of the time from the
                gps.timestamp_utc.tm_mday,  # struct_time object that holds
                gps.timestamp_utc.tm_year,  # the fix time.  Note you might
                gps.timestamp_utc.tm_hour,  # not get all data like year, day,
                gps.timestamp_utc.tm_min,  # month!
                gps.timestamp_utc.tm_sec,
            )
    else:
        latitude=str(-9999)
        longitude=str(-9999)
        GPStime=str(-9999)        
    #print(GPStime)
    #print(datetime.now().strftime('%m/%d/%Y %H:%M:%S.%f')[:-2])
    #print(latitude)
    #print(depth)
    #print(temperature)
    sdata=str("$OHPR" + ',' + GPStime + ',' + latitude +',' + longitude + ',' + depth + ',' + temperature)
    c.execute("INSERT INTO sensor_data VALUES (?,?,?,?)",(frame_count,'CTControl','$OHPR', sdata))
    c.execute("INSERT INTO images VALUES (?,?,?,?,?)",(frame_count,left_name,datel,file_namel, 'auto'))
    c.execute("INSERT INTO images VALUES (?,?,?,?,?)",(frame_count,right_name,dater,file_namer, 'auto'))
    conn.commit()
    gps.update()
    if cv.waitKey(frame_interval) & 0xFF == ord('q'):
        break

cv.destroyAllWindows()
GPIO.output(16,GPIO.LOW)
