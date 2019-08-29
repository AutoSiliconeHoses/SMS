# https://pypi.org/project/schedule/
import time
import schedule
import sys
import yaml
import socket

sys.path.append(".")
from Client import client as client

# Read config file
def runSchedule():
    with open("config.yml", 'r') as cfg:
        config = yaml.load(cfg, Loader=yaml.FullLoader)

    for s in config['suppliers']:
        if config['suppliers'][s]['enabled'] is True:
            print(s)
            # Loop through days
            for day in config['suppliers'][s]['days']:
                if config['suppliers'][s]['days'][day] is True:
                    if config['suppliers'][s]['times'] is not None:
                        for times in config['suppliers'][s]['times']:
                            print("\t", day, " @", times)
                            schedStr = "schedule.every()."+day+".at('"+times+"').do(client.runClient, ipaddr='"+socket.gethostbyname(socket.gethostname())+"', args='RUN "+s+"')"
                            # print(schedStr)
                            exec(schedStr)

    # print(schedule.jobs)
    while True:
        schedule.run_pending()
        time.sleep(1)
