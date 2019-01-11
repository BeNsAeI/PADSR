#!/usr/bin/env python

class color_code:
	HEADER = '\033[95m'
	OKBLUE = '\033[94m'
	OKGREEN = '\033[92m'
	WARNING = '\033[93m'
	FAIL = '\033[91m'
	ENDC = '\033[0m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'
	Normal = -1
	Header = 0
	Pass = 1
	Successful = 2
	Warning = 3
	Failed = 4

CC = color_code

class Priority:
	AGENT = 0
	HIGH = 1
	MEDIUM = 2
	LOW = 3
	IDLE = 4
	TRY = 5

is_shutting_down = False
#is_shutting_down = True
schedule = []
tilt_port = ''
rpLidar_port = ''
video_capture = None
bd_addr = ''
port = 1
sock = None

def Task_identify(args):
	import time
	import serial
	from rplidar import RPLidar
	import matplotlib.pyplot as plt
	import numpy as np
	import matplotlib.animation as animation
	from subprocess import call
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
	if args[0] == "stand alone":
		global tilt_port
		global rpLidar_port
		tilt_port = port1
		rpLidar_port = port2
	elif args[0] == "return":
		return port1,port2

def Task_impossible(args):
	Task_print_w(["Doing the imposible!", CC.Warning, True])
	return args[0]/0

def Task_print(args):
	print(args[0])

def Task_print_w(args):
	my_string = str(args[0])
	code = args[1]
	is_bold = False
	is_underline = False
	if len(args) > 2:
		is_bold = args[2]
	if len(args) > 3:
		is_underline = args[3]
	error_code = 0
	tmp_str = ""
	if code == CC.Normal:
		tmp_str += ""
	elif code == CC.Header:
		tmp_str += CC.HEADER
		tmp_str += "> "
	elif code == CC.Pass:
		tmp_str += CC.OKBLUE
		tmp_str += "Pass: "
	elif code == CC.Successful:
		tmp_str += CC.OKGREEN
		tmp_str += "Success: "
	elif code == CC.Warning:
		tmp_str += CC.WARNING
		tmp_str += "WARNING: "
	elif code == CC.Failed:
		tmp_str += CC.FAIL
		tmp_str += "FATAL: "
	else:
		print(CC.WARNING + "Warning: Code Unknown!" ++ CC. ENDC)
		error_code = 1
	if is_bold:
		tmp_str += CC.BOLD
	if is_underline:
		tmp_str += CC.UNDERLINE
	tmp_str += my_string + CC.ENDC
	print (tmp_str)
	return error_code

def Task_Navigate(args):
	from subprocess import call
	from multiprocessing import Process
	import time
	angle = args[0]
	distance = args[1]
	call_args = ["python", "Navigate.py",str(angle), str(distance)]
	p = Process(target=call, args=(call_args,))
	p.start()
	Task_print_w(["Navigation was scheduled in OS ...", CC.Header, True])

def Task_diagnostics(args):
	global schedule
	global sock
	Task_print_w(["Running Diagnostics ...", CC.Header, True])
	Task_print_w(["Cooling down for 5 seconds ...", CC.Header, True])
	import time
	time.sleep(5)
	errors = []
	schedule = []
	sock.close()
	schedule.append([Task_test_schedule, [], "Testing scheduler integrity", Priority.HIGH, False])
	schedule.append([Task_identify, ["stand alone"], "re-identifying pereferals", Priority.HIGH, False])
	schedule.append([Task_initialize, [], "re-initialize software", Priority.HIGH, False])
	return errors

def Task_re_schedule(args):
	global schedule
	Task_print_w(["Rescheduling task: " + args[2], CC.Header, True])
	schedule.append(args)

def Task_setup_camera(args):
	Task_print_w(["Setting Up Camera... ", CC.Header])
	import cv2
	import numpy as np
	global video_capture
	if args[0] == "front":
		video_capture = cv2.VideoCapture("nvcamerasrc ! video/x-raw(memory:NVMM), width=(int)640, height=(int)480, format=(string)I420, framerate=(fraction)30/1 ! nvvidconv ! video/x-raw, format=(string)BGRx ! videoconvert ! video/x-raw, format=(string)BGR ! appsink")
	elif args[0] == "dynamic":
		video_capture = cv2.VideoCapture(1)
	Task_print_w(["Done! ", CC.Pass])

def Task_stream(args):
	global video_capture
	Task_print_w(["Streaming Camera... ", CC.Header])
	import cv2
	import numpy as np
	if video_capture.isOpened():
		windowName = "Stream"
		cv2.namedWindow(windowName, cv2.WINDOW_NORMAL)
		cv2.resizeWindow(windowName,1280,720)
		cv2.moveWindow(windowName,0,0)
		font = cv2.FONT_HERSHEY_PLAIN
		showFullScreen = False
		key = -1
		while key != 1048689 and key != 1114081 and key != 1048603:
			if cv2.getWindowProperty(windowName, 0) < 0:
				cv2.destroyAllWindows()
				video_capture.release()
				break
			ret_val, frame = video_capture.read()
			hsv=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
			cv2.imshow(windowName,hsv)
			key=cv2.waitKey(10)
			if key == 27 or key == 'q' or key == 'Q': # Check for ESC or 'q' or 'Q' key
				video_capture.release()
				cv2.destroyAllWindows()
				Task_print_w(["Camera stream terminated.", CC.Header])
				break
			#bluetooth controls sit here:
			if sock != None:
				tosend = raw_input()
				if tosend != 'q':
					sock.send(tosend)
		video_capture.release()
		cv2.destroyAllWindows()
	else:
		Task_print_w(["Camera failed!", CC.Failed])
		exit(1)
	Task_print_w(["Done! ", CC.Pass])
	return 0

def Task_setup_lidar(args):
	Task_print_w(["Setting Up Lidar... ", CC.Header])
	Task_print_w(["Done! ", CC.Pass])
	return 0

def Task_setup_bluetooth(args):
	Task_print_w(["Setting Up Bluetooth... ", CC.Header])
	global bd_addr
	global port
	global sock
	import bluetooth
	import sys
	bd_addr = "20:16:10:31:46:89"
	port = 1
	sock = bluetooth.BluetoothSocket( bluetooth.RFCOMM )
	sock.connect((bd_addr, port))
	sock.settimeout(10.0)
	Task_print_w(["Done! ", CC.Pass])
	return 0

def Task_setup_controls(args):
	Task_print_w(["Setting Up Controls... ", CC.Header])
	Task_print_w(["Done! ", CC.Pass])
	return 0

def Task_test_controls(args):
	Task_print_w(["Testing Controls... ", CC.Header])
	tosend = "www sss aaa ddd"
	sock.send(tosend)
	Task_print_w(["Done! ", CC.Pass])
	return 0

def Task_setup_stream(args):
	Task_print_w(["Setting Up Stream... ", CC.Header])
	Task_print_w(["Done! ", CC.Pass])
	return 0

def Task_shutdown(args):
	global is_shutting_down
	is_shutting_down = True
	return 0

def Task_test_schedule(args):
	schedule.append([Task_impossible, [1], "TRY impossible task", Priority.TRY, False])
	schedule.append([Task_print_w, ["test 1", CC.Warning], "MEDIUM priority print test", Priority.MEDIUM, False])
	schedule.append([Task_print_w, ["test 2", CC.Warning], "LOW priority print test", Priority.LOW, False])
	schedule.append([Task_print_w, ["test 3", CC.Warning], "IDLE priority print test", Priority.IDLE, False])
	schedule.append([Task_print_w, ["test 4", CC.Warning], "TRY priority print test", Priority.TRY, False])

Task_manager_Message = True

def Task_manager(args):
	global schedule
	global is_shutting_down
	global Task_manager_Message
	if Task_manager_Message:
		Task_print_w(["Running Task Manager ...", CC.Header, True])
		Task_manager_Message = False
	if is_shutting_down:
		schedule = []
	return 0

def Task_initialize(args):
	global schedule
	schedule = []
	Task_print_w(["Initializing ...", CC.Header, True])
	#schedule.append([<TASK>, [<ARGS>], "<TASK NAME>", Priority.<PRIORITY>, <QUITE>])
	#Task_test_schedule([])
	schedule.append([Task_identify, ["stand alone"], "Identifying pereferals", Priority.HIGH, False])
	schedule.append([Task_setup_camera, ["dynamic"], "Initiating Camera", Priority.MEDIUM, False])
	schedule.append([Task_setup_lidar, [], "Initiating Lidar", Priority.MEDIUM, False])
	#schedule.append([Task_setup_bluetooth, [], "Initiating Bluetooth controller", Priority.LOW, False])
	schedule.append([Task_setup_controls, [], "Initiating controls and movement", Priority.LOW, False])
	schedule.append([Task_test_controls, [], "Testing controls", Priority.IDLE, False])
	schedule.append([Task_setup_stream, [], "Initiating stream", Priority.HIGH, False])
	schedule.append([Task_manager, [], "Lunching Manager", Priority.AGENT, False])
	schedule.append([Task_test_schedule, [], "Testing scheduler integrity", Priority.HIGH, False])
	schedule.append([Task_stream, [], "Initiating Camera", Priority.IDLE, False])
	schedule.append([Task_shutdown, [], "Schedule to shut down", Priority.TRY, False])
	Task_print_w(["Initial tasks were scheduled.", CC.Pass, True])

def Task_lunch(task, args, task_name, priority = Priority.IDLE, quite = True):
	try:
		task(args)
		str_priority = ""
		if not quite and priority != Priority.AGENT:
			Task_print_w(["Task[-]: \"" + task_name + "\" was successful.", CC.Successful])
	except:
		if priority == Priority.AGENT:
			#agents are never quite on failure!
			Task_print_w(["Task[HIGH]: \"" + task_name + "\" Failed.", CC.Failed])
			exit(1)

		elif priority == Priority.HIGH:
			if not quite:
				Task_print_w(["Task[HIGH]: \"" + task_name + "\" Failed.", CC.Failed])
			Task_lunch(Task_diagnostics, [0] , "Lunching Diagnostics",Priority.HIGH, quite= quite)
			Task_lunch(Task_re_schedule, [task, args, task_name, priority], "Rescheduling a task \"" + task_name +"\"", Priority.HIGH, quite= quite)
		elif priority == Priority.MEDIUM:
			if not quite:
				Task_print_w(["Task[MEDIUM]: \"" + task_name + "\" Failed.", CC.Warning])
			Task_lunch(task, args, task_name, priority - 1, quite= quite)
		elif priority == Priority.LOW:
			if not quite:
				Task_print_w(["Task[LOW]: \"" + task_name + "\" Failed.", CC.Warning])
			Task_lunch(task, args, task_name, priority - 1, quite= quite)
		elif priority == Priority.IDLE:
			if not quite:
				Task_print_w(["Task[IDLE]: \"" + task_name + "\" Failed.", CC.Normal])
			Task_lunch(Task_re_schedule, [task, args, task_name, priority], "Rescheduling a task \"" + task_name +"\"", Priority.HIGH, quite= quite)
		elif priority == Priority.TRY:
			if not quite:
				Task_print_w(["Task[TRY]: \"" + task_name + "\" Failed.", CC.Normal])

def main():
	global schedule
	Task_lunch(Task_initialize,[], "Initializing", Priority.HIGH, quite = False)
	while len(schedule) > 0:
		#Task_print_w(["Executing AGENT priority scheduled items", CC.Normal])
		i = 0
		while (i < len(schedule)) and (i > -1):
			if schedule[i][3] == Priority.AGENT:
				Task_lunch(schedule[i][0], schedule[i][1], schedule[i][2], schedule[i][3], quite=schedule[i][4])
				#Agents are not unscheduled
			i += 1

		#Task_print_w(["Executing HIGH priority scheduled items", CC.Normal])
		i = 0
		while (i < len(schedule)) and (i > -1):
			if schedule[i][3] == Priority.HIGH:
				Task_lunch(schedule[i][0], schedule[i][1], schedule[i][2], schedule[i][3], quite=schedule[i][4])
				schedule.remove(schedule[i])
				i = 0
			else:
				i += 1


		#Task_print_w(["Executing MEDIUM priority scheduled items", CC.Normal])
		i = 0
		while (i < len(schedule)) and (i > -1):
			if schedule[i][3] == Priority.MEDIUM:
				Task_lunch(schedule[i][0], schedule[i][1], schedule[i][2], schedule[i][3], quite=schedule[i][4])
				schedule.remove(schedule[i])
				i = 0
			else:
				i += 1

		i = 0
		while (i < len(schedule)) and (i > -1):
			if schedule[i][3] == Priority.MEDIUM:
				print i
				print schedule
				print schedule[i][2]
				print schedule[i][3]
				exit(1)
			i += 1

		#Task_print_w(["Executing LOW priority scheduled items", CC.Normal])
		i = 0
		while (i < len(schedule)) and (i > -1):
			if schedule[i][3] == Priority.LOW:
				Task_lunch(schedule[i][0], schedule[i][1], schedule[i][2], schedule[i][3], quite=schedule[i][4])
				schedule.remove(schedule[i])
				i = 0
			else:
				i += 1

		#Task_print_w(["Executing IDLE priority scheduled items", CC.Normal])
		i = 0
		while (i < len(schedule)) and (i > -1):
			if schedule[i][3] == Priority.IDLE:
				Task_lunch(schedule[i][0], schedule[i][1], schedule[i][2], schedule[i][3], quite=schedule[i][4])
				schedule.remove(schedule[i])
				i = 0
			else:
				i += 1

		#Task_print_w(["Executing TRY priority scheduled items", CC.Normal])
		i = 0
		while (i < len(schedule)) and (i > -1):
			if schedule[i][3] == Priority.TRY:
				Task_lunch(schedule[i][0], schedule[i][1], schedule[i][2], schedule[i][3], quite=schedule[i][4])
				schedule.remove(schedule[i])
				i = 0
			else:
				i += 1
	return 0

if __name__ == '__main__':
	main()
