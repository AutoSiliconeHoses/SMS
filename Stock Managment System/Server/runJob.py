import collections, multiprocessing, pickle, os, sys, py_compile, time, yaml
import Server.configedit as configedit

# Read config file
with open("config.yml", 'r') as cfg:
    config = yaml.load(cfg, Loader=yaml.FullLoader)

# import suppliers, iterates through config.yml and imports the modules using names
for s in config['suppliers']:
    if config['suppliers'][s]['enabled']:
        impstring = "from Suppliers." + s.upper() + "." + s + " import " + s
        try:
            exec(impstring)
            print("Succesfuly imported", s)
        except:
            print("Could not import", s)

# List of accepted commands
comlist = ["RUN", "CNFED", "UPDATE"]

def runJob(q):
    time.sleep(1)
    while True:
        if q:
            job = q.popleft()
            if job[0] == "RUN":  # Runs  the supplier scripts
                suppliers = job[1:len(job)]  # Makes a list of suppliers to go through
                if suppliers:
                    processPool = multiprocessing.Pool()  # Makes process pool
                    supplierslist = []
                    for s in suppliers:
                        if s not in supplierslist:
                            supplierslist.append(s)
                            try:
                                processPool.apply_async(eval(s))  # Creates pool in processPool for each supplier
                            except:
                                print("Could not execute:", s)
                        else:
                            print("Error: " + s + " will only run once per request")
                    processPool.close()
                    processPool.join()

                else:
                    print("Error: No suppliers given")
            elif job[0] == "CNFED":  # Config edit
                configedit.update(job[1], job[2])
            elif job[0] == "UPDATE":  # Update server
                print("Updating....")
                try:
                    py_compile.compile('__servinit__.py', doraise=True)
                    print("Compilation Check Successful")
                    restart_program(q)
                except py_compile.PyCompileError:
                    print("Error: Update Unsuccessful")
        # q.task_done()
        time.sleep(5)

def restart_program(q):
    if q:  # check if queue is empty, if false create file and load it with all commands following update
        file = open('import_queue', 'wb')
        pickle.dump(q, file)
        file.close()

    python = sys.executable
    os.execl(python, python, *sys.argv)
