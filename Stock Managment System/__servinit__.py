import threading, yaml, collections, sys, os, pickle, time
from Server.runSchedule import runSchedule
from Server.runJob import runJob
from Server.runRequests import runRequests

def runServer():

    q = collections.deque()
    if os.path.exists('import_queue'):  # tries to find a previously loaded queue. Used for update
        with open('import_queue', 'rb') as file:
            data = pickle.load(file)
            file.close()
        for item in data:
            q.append(item)
        os.remove('import_queue')

    try:
        rTh = threading.Thread(target=runRequests, args=(q,))
        rTh.start()
        jTh = threading.Thread(target=runJob, args=(q,))
        jTh.start()
        sTh = threading.Thread(target=runSchedule)
        sTh.start()
        print("Successfully created threads")
    except e:
        print("There was an error creating threads.")
        exit()
runServer()
