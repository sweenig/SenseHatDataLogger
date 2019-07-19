##### Libraries #####
from sense_hat import SenseHat
from time import sleep
from Adafruit_IO import Client
import sys
##### Create complex objects #####
aio = Client(sys.argv[1], sys.argv[2])
sense = SenseHat() #create the sense hat object
##### Logging Settings #####
TEMP_H=True
TEMP_P=True
HUMIDITY=True
PRESSURE=True
ORIENTATION=False
ACCELERATION=False
MAG=False
GYRO=False
DELAY=60 #number of seconds between data point gatherings
##### Functions #####
while True:
	sense_data=[]
	if TEMP_H:
		aio.send('temp_h',sense.get_temperature_from_humidity())
	if TEMP_P:
		aio.send('temp_p',sense.get_temperature_from_pressure())
	if HUMIDITY:
		aio.send('humidity',sense.get_humidity())
	if PRESSURE:
		aio.send('pressure',sense.get_pressure())
	if ORIENTATION:
		o = sense.get_orientation()
		aio.send('yaw',o["yaw"])
		aio.send('pitch',o["pitch"])
		aio.send('roll',o["roll"])
	if MAG:
		mag = sense.get_compass_raw()
		aio.send('mag_x',mag["x"])
		aio.send('mag_y',mag["y"])
		aio.send('mag_z',mag["z"])
	if ACCELERATION:
		acc = sense.get_accelerometer_raw()
		aio.send('x',acc["x"])
		aio.send('y',acc["y"])
		aio.send('z',acc["z"])
	if GYRO:
		gyro = sense.get_gyroscope_raw()
		aio.send('gyro_x',gyro["x"])
		aio.send('gyro_y',gyro["y"])
		aio.send('gyro_z',gyro["z"])
	sleep(DELAY) #wait before getting the next data point
