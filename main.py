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
	HIGH = 1
	MEDIUM = 2
	LOW = 3
	IDLE = 4
	TRY = 5

schedule = []

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

def Task_diagnostics(args):
	Task_print_w(["Running Diagnostics ...", CC.Header, True])
	errors = []
	return errors

def Task_re_schedule(args):
	global schedule
	Task_print_w(["Rescheduling task: " + args[2], CC.Header, True])
	schedule.append(args)

def Task_initialize(args):
	global schedule
	schedule = []
	Task_print_w(["Initializing ...", CC.Header, True])
	schedule.append([Task_impossible, [1], "Trying to do something impossible", Priority.TRY, False])
	print schedule

def Task_lunch(task, args, task_name, priority = Priority.IDLE, quite = True):
	try:
		task(args)
		str_priority = ""
		if not quite:
			Task_print_w(["Task[-]: \"" + task_name + "\" was successful.", CC.Successful])
	except:
		if priority == Priority.HIGH:
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
	Task_print_w(["Executing HIGH priority scheduled items", CC.Normal])
	for i in schedule:
		if i[3] == Priority.HIGH:
			Task_lunch(i[0], i[1], i[2], i[3], quite=i[4])

	Task_print_w(["Executing MEDIUM priority scheduled items", CC.Normal])
	for i in schedule:
		if i[3] == Priority.MEDIUM:
			Task_lunch(i[0], i[1], i[2], i[3], quite=i[4])

	Task_print_w(["Executing LOW priority scheduled items", CC.Normal])
	for i in schedule:
		if i[3] == Priority.LOW:
			Task_lunch(i[0], i[1], i[2], i[3], quite=i[4])

	Task_print_w(["Executing IDLE priority scheduled items", CC.Normal])
	for i in schedule:
		if i[3] == Priority.IDLE:
			Task_lunch(i[0], i[1], i[2], i[3], quite=i[4])

	Task_print_w(["Executing TRY priority scheduled items", CC.Normal])
	for i in schedule:
		if i[3] == Priority.TRY:
			Task_lunch(i[0], i[1], i[2], i[3], quite=i[4])



if __name__ == '__main__':
	main()
