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
    ipaddr = socket.gethostbyname(socket.gethostname())

    for s in config['suppliers']:
        if config['suppliers'][s]['enabled'] is True:
            print(s)
            # Loop through days
            for day in config['suppliers'][s]['days']:
                if config['suppliers'][s]['days'][day]['enabled'] is True:
                    if config['suppliers'][s]['days'][day]['times'] is not None:
                        for schedtime in config['suppliers'][s]['days'][day]['times']:
                            print("\t", day, " @", schedtime)
                            dests = config['suppliers'][s]['days'][day]['times'][schedtime][0]
                            opts = config['suppliers'][s]['days'][day]['times'][schedtime][1]
                            schedStr = "schedule.every()."+day+".at('"+schedtime+"').do(client.runClient, ipaddr='"+ipaddr+"', args='RUN sup=["+s+"] dest=["+dests+"] opt=["+opts+"]')"
                            exec(schedStr)

    while True:
        schedule.run_pending()
        time.sleep(1)
