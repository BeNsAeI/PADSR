import time
import serial
from rplidar import RPLidar
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
from subprocess import call

def update_line(num, iterator, line):
	scan = next(iterator)
	offsets = np.array([(np.radians(-meas[1]), meas[2]) for meas in scan])
	line.set_offsets(offsets)
	intens = np.array([meas[0] for meas in scan])
	line.set_array(intens)
	return line,

def identify():
	ser = serial.Serial(
		port='/dev/ttyUSB1',
		baudrate=9600,
		parity=serial.PARITY_ODD,
		stopbits=serial.STOPBITS_TWO,
		bytesize=serial.SEVENBITS
	)
	ser.isOpen()
	print "identifying the tilt/shift port..."
	time.sleep(1)
	ser.write('\r\n')
	out = ''
	# let's wait one second before reading output (let's give device time to answer)
	time.sleep(1)
	while ser.inWaiting() > 0:
		out += ser.read(1)
	if(out == 'Ready\r\n'):
		port1='/dev/ttyUSB1'
		port2='/dev/ttyUSB0'
	else:
		port1='/dev/ttyUSB0'
		port2='/dev/ttyUSB1'
	print("Tilt/shift Port Identified: "+ port1)
	print("rpLidar Port Identified: "+ port2)
	ser.close()
	return port1,port2

class MAP:
	def __init__(self,tilt_port, rpLidar_port):
		self.tilt_port = tilt_port
		self.rpLidar_port = rpLidar_port
		self.ser = serial.Serial(
			port=tilt_port,
			baudrate=9600,
			parity=serial.PARITY_ODD,
			stopbits=serial.STOPBITS_TWO,
			bytesize=serial.SEVENBITS
		)
		self.ser.isOpen()
		time.sleep(2)

		self.DMAX = 4000
		self.IMIN = 0
		self.IMAX = 50

	def runLidar(self):
		command = "python animate.py "+self.rpLidar_port+" &"
		print("Calling: "+ command)
		call(command, shell=True)

	def getCoord(self):
		'''Main function'''
		lidar = RPLidar(self.rpLidar_port)
		lidar.stop()
		info = lidar.get_info()
		print(info)
		health = lidar.get_health()
		print(health)
		lidar.stop()
		try:
			print('Recording measurments... Press Crl+C to stop.')
			for i in range (0,10):
				scan = next(lidar.iter_scans())
				for measurment in scan:
					lidar.stop()
					line = '\t'.join(str(v) for v in  measurment)
					#print(line)
				lidar.stop()
				time.sleep(0.0625)
			#for scan in lidar.iter_scans():
			#	print(scan)
		except KeyboardInterrupt:
			print('Stoping.')
		lidar.stop()
		lidar.disconnect()

	def radar(self):
		lidar = RPLidar(self.rpLidar_port)
		lidar.stop()
		fig = plt.figure()
		ax = plt.subplot(111, projection='polar')
		line = ax.scatter([0, 0], [0, 0], s=5, c=[self.IMIN, self.IMAX],
							   cmap=plt.cm.Greys_r, lw=0)
		ax.set_rmax(self.DMAX)
		ax.grid(True)

		iterator = lidar.iter_scans()
		ani = animation.FuncAnimation(fig, update_line,
			fargs=(iterator, line), interval=50)
		plt.show()
		lidar.stop()
		lidar.disconnect()

	def sweep_front(self):
		self.ser.write('h\r\n')
		time.sleep(2)
		self.ser.write('dddddddddddd\r\n')
		time.sleep(2)
		for i in range(0,20):
			self.ser.write('u\r\n')
			time.sleep(2)
		time.sleep(2)
	def sweep_sides(self):
		self.ser.write('h\r\n')
		time.sleep(2)
		self.ser.write('rrrrrrrrrrrrrrrrrrr\r\n')
		time.sleep(2)
		self.ser.write('dddddddddddd\r\n')
		time.sleep(2)
		for i in range(0,20):
			self.ser.write('u\r\n')
			time.sleep(2)
		time.sleep(2)
		self.ser.write('lllllllllllllllllll\r\n')
		time.sleep(2)
		self.ser.write('dddddddddddd\r\n')
		time.sleep(2)
		for i in range(0,20):
			self.ser.write('u\r\n')
			time.sleep(2)
		time.sleep(2)
	def drive_unit(self, command):
		print("Processing command: "+ str(command))
	def init_map(self):
		print("Mapping area and callibrating ...")
		# scan for a while and build a model of surrounding
		# this is the initial position grid(x,y)

	def locate(self):
		print("Locating current coordinates...")
		# scan for a while and build a model of surrounding
		# find the matrix transformation from initial map to current map
		# return the x and y compared to initial position: grid(x,y)

	def navigate(self, Angle, Range):
		print("Navigating...")
		print("Finding the shortest path...")
		#current_grid = [locate()[0],locate()[1]]
		#if obstacles (if the distance from lidar on angle is shorter than range):
			#navigate to obstacle - safety distance
			#go around obstacle
			#find andgle and distance to new_grid
			#navigate to new grid
		#else:
		print("connecting to drive unit...")
		print("Sendng commands...")
		print("Assessing position ...")
		print("Adjusting for error ...")
		print("disconnecting from drive unit...")
		print("updating current location...")
		print("Done!")
	def Close(self):
		self.ser.write('h\r\n')
		time.sleep(5)
		self.ser.close()



myMap = MAP(identify()[0], identify()[1])
#myMap.runLidar()
#myMap.getCoord()
#myMap.radar()
#myMap.sweep_front()
#myMap.sweep_sides()
myMap.Close()
