import ms5837
import time

depthsensor = ms5837.MS5837_30BA() # Default I2C bus is 1 (Raspberry Pi 3)
depthsensor.init()
depthsensor.read()
depthsensor.pressure()
#depthsensor.pressure(ms5837,UNITS_psi)
print(depthsensor.temperature())
# We must initialize the sensor before reading it
#if not sensor.init():
 #       print("Sensor could not be initialized")
 #       exit(1)

# Print readings
#while True:
#        if sensor.read():
#                print("P: %0.1f mbar  %0.3f psi\tT: %0.2f C  %0.2f F") % (
#                sensor.pressure(), # Default is mbar (no arguments)
#                sensor.pressure(ms5837.UNITS_psi), # Request psi
#                sensor.temperature()) # Default is degrees C (no arguments)
                #sensor.temperature(ms5837.UNITS_Farenheit)) # Request Farenheit
#        else:
 #               print("Sensor read failed!")
  #              exit(1)

