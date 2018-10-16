import time
from pympler import asizeof
from pympler import tracker
from pympler import classtracker
import os, os.path
from time import sleep
import subprocess
class Tester:
	def __init__(self):
		self.initTime = 0
		self.endTime = 0
		self.obj_tr= tracker.SummaryTracker()
		self.cls_tr = classtracker.ClassTracker()
		self.output_snap = len([name for name in os.listdir('.') if os.path.isfile(name)]);
	def startTimer(self):
		self.initTime = time.time()
	def stopTimer(self):
		self.endTime = time.time()
	def Time(self):
		start = self.initTime
		end = self.endTime
		return(end - start)
	def check_object_size(self,obj):
		asizeof.asizeof(obj)
	def print_object_profile(self,obj):
		print asizeof.asized(obj, detail=1).format()
	def track_object(self):
		self.obj_tr.print_diff()
	def init_class_tracker(self,obj):
		self.cls_tr.track_class(obj)
		self.cls_tr.create_snapshot()
	def snapshot_class(self):
		self.cls_tr.create_snapshot()	
	def get_class_summary(self):
		self.cls_tr.stats.print_summary()
	def init_output_file_check(self):
		self.output_snap = len([name for name in os.listdir('.') if os.path.isfile(name)])
		print(str(self.output_snap)+" files recorded.")
	def output_file_count(self):
		new = len([name for name in os.listdir('.') if os.path.isfile(name)])
		return (new - self.output_snap)



class test_class:
	def __init__(self,a,b,c):
		self.A = a
		self.B = b
		self.C = c

def test():
	print("Creating an instance...")
	myTester = Tester()
	print("setting up class tracking...")
	myTester.init_class_tracker(test_class)
	print("creating a an instance of test class")
	my_test_class = test_class(1,2,3)
	print("__________")
	print("Timing test:")
	myTester.startTimer()
	sleep(0.254)
	myTester.stopTimer()
	print("Original time is 0.254, Function returned: "+ str(myTester.Time()))
	print("__________")
	print("Generating a random object...")
	obj = [1, 2, (3, 4), 'text']
	print(obj)
	print("checking object size, memory and profile:")
	myTester.check_object_size(obj)
	myTester.print_object_profile(obj)
	myTester.track_object()
	print("__________")
	print("checking Class size, memory and profile:")
	myTester.snapshot_class()
	myTester.get_class_summary()
	print("__________")
	print("checking for output files added:")
	myTester.init_output_file_check()
	print("so far there have been "+str(myTester.output_file_count())+" files added.")
	print("creating a tmp file...")
	os.system("echo \"<To be deleted>\" >> test.txt")
	print("checking for output files added:")
	print("so far there have been "+str(myTester.output_file_count())+" files added.")
	print("deleting the tmp file...")
	os.system("rm test.txt")
	
test()
