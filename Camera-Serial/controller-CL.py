import serial
class SerialWrapper:
	def __init__(self, device):
		self.ser = serial.Serial(device, 9600)
		print(self.ser.name)
	def sendData(self, data):
		data += "\r\n"
		self.ser.write(data.encode())
	def readData(self):
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
	mySerial = SerialWrapper('/dev/ttyUSB0')
        #misc code here
#	indata = mySerial.readData()
#	print(indata)
#	outdata = "rrrrruuuu"
	outdata = "h"
	mySerial.sendData(outdata)
	mySerial.close()
main()
