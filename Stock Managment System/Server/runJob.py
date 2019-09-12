import collections, multiprocessing, pickle, os, sys, py_compile, time, yaml, re
import Server.configedit as configedit
import Server.Send.Amazon.amazon as amazon
import Server.Send.Ebay.ebay as ebay

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
            suppliers = destinations = options = [] # Sets all to a blank array to avoid reference issues

            if job[0] == "RUN":  # Runs  the supplier scripts
                args = job[1:len(job)]  # Breaks down the arguments given into components using RegEx
                for arg in args: 
                    if re.search(r"(?<=sup=\[).*?(?=\])",arg):
                        suppliers = re.search(r"(?<=sup=\[).*?(?=\])",arg).group(0).split(",")
                    elif re.search(r"(?<=dest=\[).*?(?=\])",arg):
                        destinations = re.search(r"(?<=dest=\[).*?(?=\])",arg).group(0).split(",")
                    elif re.search(r"(?<=opt=\[).*?(?=\])",arg):
                        options = re.search(r"(?<=opt=\[).*?(?=\])",arg).group(0).split(",")
                print(suppliers,destinations,options)
                if ('' not in suppliers) and suppliers:
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

                    # Destination checks
                    if "amazon" in destinations:
                        print("Sending files to Amazon")
                        if "prime" in options:
                            prime = True
                        else:
                            prime = False
                        mws = amazon.AmazonMWS()
                        newfiles = []
                        for supplier in suppliers:
                            newfile = mws.format("Server/Send/StockFiles/"+supplier+".tsv",prime=prime)
                            newfiles.append(newfile)
                        # NOTE: Uncomment when ready to run
                        # results = mws.SubmitFeed(newfiles)
                        # TODO: Determine Success/Fail, report and move file accordingly (Can also be done in amazon.py)
                        print("Sent")

                    if "ebay" in destinations:
                        print("Sending files to Ebay")
                        eb = ebay.EbayAPI()
                        # NOTE: Change to True when ready to run
                        eb.process(suppliers=suppliers,upload=False)
                        print("Sent")

                    if "dropship" in destinations:
                        print("Dropship not yet implemented")
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
