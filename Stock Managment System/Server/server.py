import importlib, socket, sys, time, string, os, yaml, threading, multiprocessing, queue
import psutil
from os.path import getmtime
import Server.configedit as configedit
import Server.suppliers as import_suppliers

# Read config file
with open("config.yml", 'r') as cfg:
    config = yaml.load(cfg, Loader=yaml.FullLoader)

comlist = ["RUN","CNFED","UPDATE","QUEUE"]

WATCHED = [__file__]
WATCHED_FILES = [(f, getmtime(f)) for f in WATCHED]

q = queue.Queue()

def restart_program():
    p = psutil.Process(os.getpid())
    for handler in p.connections():
        os.close(handler.fd)

    python = sys.executable
    os.execl(python, python, *sys.argv)

def commandCheck(c, args):
    if args[0] in comlist: # Accepted commands
        q.put(args)     # Add to queue
        c.send(("You are #" + str(q.qsize()) + " in the queue").encode())
    else:   # Unknown command
        print("Command not recognized")
        c.send("Command not recognized".encode())

def runJob():
    while True:
        if not q.empty():
            job = q.get()
            if job[0] == "RUN":
                suppliers = job[1:len(job)]
                for s in suppliers:
                    # try:
                    print("Running", s)
                    procStr = "multiprocessing.Process(target="+s+").start()"
                    exec(procStr)
                    print("Succesfuly executed", s)
                    # except:
                        # print("Could not execute:", s)

            elif job[0] == "CNFED":     # Config edit
                try:
                    configedit.update(args[1],args[2])
                    c.send("UPDATE SUCCESFUL".encode())
                except:
                    c.send("Update error, please check log".encode())

            elif job[0] == "UPDATE":    # Update server
                # try:
                for f, mtime in WATCHED_FILES:
                    if getmtime(f) != mtime:
                        print("Updating....")
                        restart_program()
                    else:
                        print("No changes made")
            elif job[0] == "QUEUE":
                for j in q:
                    print(j)
            q.task_done()


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
    import_suppliers.import_suppliers()
    try:
        rTh = threading.Thread(target = runRequests)
        rTh.start()
        jTh = threading.Thread(target = runJob)
        jTh.start()
    except:
        print("There was an error")
        exit()
