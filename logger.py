##### Libraries #####
from datetime import datetime
from sense_hat import SenseHat
from time import sleep

##### Logging Settings #####
FILENAME = "SenseData"
OUTPUT_BUFFER_SIZE = 3 #number of data points to accumulate before writing out to a file
MAX_LOG_FILE_SIZE = 1000 #number of data points to write to a file before starting a new file
TEMP_H=True
TEMP_P=False
HUMIDITY=True
PRESSURE=True
ORIENTATION=True
ACCELERATION=True
MAG=True
GYRO=True
DELAY=300 #number of seconds between data point gatherings
WRITE_HEADERS=True #whether or not to write the headers for a CSV

##### Functions #####
def get_sense_data():
	sense_data=[]
	if TEMP_H: sense_data.append(sense.get_temperature_from_humidity())
	if TEMP_P: sense_data.append(sense.get_temperature_from_pressure())
	if HUMIDITY: sense_data.append(sense.get_humidity())
	if PRESSURE: sense_data.append(sense.get_pressure())
	if ORIENTATION:
		o = sense.get_orientation()
		yaw = o["yaw"]
		pitch = o["pitch"]
		roll = o["roll"]
		sense_data.extend([pitch,roll,yaw])
	if MAG:
		mag = sense.get_compass_raw()
		mag_x = mag["x"]
		mag_y = mag["y"]
		mag_z = mag["z"]
		sense_data.extend([mag_x,mag_y,mag_z])
	if ACCELERATION:
		acc = sense.get_accelerometer_raw()
		x = acc["x"]
		y = acc["y"]
		z = acc["z"]
		sense_data.extend([x,y,z])
	if GYRO:
		gyro = sense.get_gyroscope_raw()
		gyro_x = ["x"]
		gyro_y = ["y"]
		gyro_z = ["z"]
		sense_data.extend([gyro_x,gyro_y,gyro_z])
	sense_data.append(datetime.now())
	return sense_data

##### Main Program #####
sense = SenseHat() #create the sense hat object
output_buffer=[] #output queue to contain the data files in memory before writing out to the file
log_size=0 #tracks the current size of the log file currently being written to (in # of lines)
while True:
	output_buffer.append(get_sense_data()) #collect a data point and add it to the output queue
	if log_size==0: #starting a new log, so get a new name and output the headers (if desired)
		filename = FILENAME+"-"+str(datetime.now())+".csv" #generate the new filename
		if WRITE_HEADERS: #write out the CSV headers (optional)
			header =[] #list to contain the column headers
			if TEMP_H: header.append("temp_h")
			if TEMP_P: header.append("temp_p")
			if HUMIDITY: header.append("humidity")
			if PRESSURE: header.append("pressure")
			if ORIENTATION: header.extend(["pitch","roll","yaw"])
			if MAG: header.extend(["mag_x","mag_y","mag_z"])
			if ACCELERATION: header.extend(["accel_x","accel_y","accel_z"])
			if GYRO: header.extend(["gyro_x","gyro_y","gyro_z"])
			header.append("timestamp")
			with open(filename,"w") as f: f.write(",".join(str(value) for value in header)+ "\n") #write the column headers
	if len(output_buffer) >= OUTPUT_BUFFER_SIZE: #if the output queue is full
		print("Writing %s data points to file.." % len(output_buffer)) #give a message to the screen
		log_size += len(output_buffer) #update the log file size
		with open(filename,"a") as f: #append to the current file
			for data_point in output_buffer: #for each data point in the output queue
				f.write(",".join(str(value) for value in data_point) + "\n") #write the data point from the output queue to file
			output_buffer = [] #empty the output queue
	if log_size >= MAX_LOG_FILE_SIZE: log_size=0 #if the log is too big, signal to start a new one
	sleep(DELAY) #wait before getting the next data point
