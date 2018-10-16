import time
import sys
import serial
class SerialWrapper:
	def __init__(self, device):
		self.ser = serial.Serial(device, 9600)
		print(self.ser.name)
		self.ser.flush()
	def sendData(self, data):
		self.ser.flush()
		data += "\r\n"
		self.ser.write(data.encode())
	def readData(self):
		self.ser.flush()
		data = ""
		line = []
		for c in self.ser.read():
			line.append(c)
			if c == '\n':
				data = line
				line = None
				break
		return data
	def close(self):
		if(self.ser.is_open):
			self.ser.close()

def main():
	outdata = "r"
	if(len(sys.argv) > 1):
		print("executing: "+sys.argv[1]+" -> "+str(len(sys.argv[1]))+" characters detected.")
		outdata = str(sys.argv[1])
	else:
		print("Homing...")
		outdata = "h"
	mySerial = SerialWrapper('/dev/ttyUSB0')
	mySerial.sendData(outdata)
	time.sleep(0.25)
	mySerial.close()
main()
