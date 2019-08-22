import threading, yaml, collections, sys, os, pickle, time
from Server.runSchedule import runSchedule
from Server.runJob import runJob
from Server.runRequests import runRequests

def runServer():

    q = collections.deque()

    try:  # tries to find a previously loaded queue. Used for update
        file = open('import_queue', 'rb')
        data = pickle.load(file)
        file.close()
        for item in data:
            q.append(item)
        os.remove('import_queue')
    except:
        None

    time.sleep(0.5)

    # try:
    rTh = threading.Thread(target=runRequests, args=(q,))
    rTh.start()
    jTh = threading.Thread(target=runJob, args=(q,))
    jTh.start()
    sTh = threading.Thread(target=runSchedule)
    sTh.start()
    print("Successfully created threads")
    # except:
    #     print("There was an error")
    #     exit()
runServer()
