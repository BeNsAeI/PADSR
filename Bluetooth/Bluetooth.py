import bluetooth
import sys
bd_addr = "20:16:10:31:46:89"

port = 1
sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
sock.connect((bd_addr, port))
print 'Connected'
sock.settimeout(10.0)
while 1:
	#data = sock.recv(10)
	#print data
	print "Send data or \'q\' to exit: "
	tosend = raw_input()
	if tosend != 'q':
		sock.send(tosend)
	else:
		break

sock.close()
