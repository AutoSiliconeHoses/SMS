import importlib, socket, sys, time, string, os, yaml, threading, multiprocessing, queue, subprocess, py_compile, pickle, collections
import psutil
from os.path import getmtime
import Server.configedit as configedit

# Read config file
with open("config.yml", 'r') as cfg:
	config = yaml.load(cfg, Loader=yaml.FullLoader)

# import suppliers, itterates through config.yml and imports the modules using names
for s in config['suppliers']:
	if config['suppliers'][s]['enabled'] == True:
		impstring = "from Suppliers."+s.upper()+"."+s+" import "+s
		try:
			exec(impstring)
			print("Succesfuly imported", s)
		except:
			print("Could not import", s)

# List of accepted commands
comlist = ["RUN","CNFED","UPDATE"]

# Files "watches" itself, used for UPDATE
WATCHED = [__file__]
WATCHED_FILES = [(f, getmtime(f)) for f in WATCHED]

# Initiate queue d
q = collections.deque()

# for row in open("import_queue.txt").readlines():
# 	", ".join(str(row))
# 	print(row)
# 	q.put(row)

# file = open('import_queue', 'rb')
# data = pickle.load(file)
# file.close()
# q.put(data)
#
# comq = ""
# for element in list(q.queue):
# 	comq = comq + str(element)
# print(comq)


# Restarts program with UPDATE
def restart_program(): # change
	file = open('import_queue', 'wb')
	while q:
		command = q.popleft()
		pickle.dump(command, file)
	#	q.task_done() # change
	file.close()

	p = psutil.Process(os.getpid())
	for handler in p.connections():
		os.close(handler.fd)

	python = sys.executable
	os.execl(python, python, *sys.argv)

# Checks commands
def commandCheck(c, args):
	if args[0] in comlist: # Accepted commandserg
		q.append(args)	 # Add to queue
		c.send(("You are #" + str(len(q)) + " in the queue").encode())
	elif args[0] == "QUEUE":
		comq = ""
		for element in q:
			comq = comq + str(element) + "\n"
		c.send(comq.encode())
	else:   # Unknown command
		print("Command not recognized")
		c.send("Command not recognized".encode())

def runJob():
	while True:
		if q:
			job = q.popleft()
			if job[0] == "RUN": # Runs  the supplier scripts
				suppliers = job[1:len(job)] # Makes a list of suppliers to go through
				processPool = multiprocessing.Pool() # Makes process pool
				for s in suppliers:
					try:
						processPool.apply_async(eval(s)) # Creates pool in processPool for each supplier
					except:
						print("Could not execute:", s)
				processPool.close()
				processPool.join()
			elif job[0] == "CNFED":	# Config edit
				try:
					configedit.update(job[1],job[2]) # cant give it c because it is made in main but not passed to runJob
					print("Congig.yml updated")
					# When putting in a command it needs to be in format "CNFED ['suppliers'][*supplier*][*attribute*] *value*"
				except:
					print("Error: Config Update Unsuccessful\nConfig Unaffected")
			elif job[0] == "UPDATE": # Update server
				for f, mtime in WATCHED_FILES:
					if getmtime(f) != mtime:
						print("Updating....")
						try:
							py_compile.compile('Server/server.py', doraise=True)
							print("Compilation Check Successful")
							restart_program()
						except py_compile.PyCompileError:
							print("Error: Update Unsuccessful")
							#print("Error: Failed to restart server.")
					else:
						print("No changes made")
			#q.task_done()
		time.sleep(5)

def runRequests():
	# Get socket ready for use
	s = socket.socket()
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	port = 2100
	s.bind(('', port))

	# Start listening for connections
	s.listen(5)
	print("Listening on " + str(port))
	while True:
		# Connect with incoming client
		c, addr = s.accept()
		print ('Connection established with: ', addr)

		# Receive command from client and split
		receive = c.recv(1024).decode()
		args = receive.split(" ")

		commandCheck(c, args)

		time.sleep(0.01)
		c.send("EXIT".encode())
		c.close()

def runServer():
	try:
		rTh = threading.Thread(target = runRequests)
		rTh.start()
		jTh = threading.Thread(target = runJob)
		jTh.start()
		print("Successfully created threads")
	except:
		print("There was an error")
		exit()
