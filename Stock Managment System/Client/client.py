import socket, sys, re

def runClient(ipaddr="192.168.1.131", args=None):
    if len(sys.argv) > 1:
        args = sys.argv[1]
        print(args)
    elif args is not None:
        None
    else:
        print("Error: No arguments given")
        return

    queue = None
    s = socket.socket()
    host = ipaddr ## server = 131
    port = 2100

    s.connect((host, port))

    send = args.encode()
    s.send(send)

    exitCom = False

    while not exitCom:
        receive = s.recv(1024).decode()
        if receive != "":
            print (receive)
            if re.match("You are #.* in the queue", receive):
                search = re.search("(?<=#).*?(?= )", receive)
                queue = receive[search.start():search.end()]
        if receive == "EXIT":
            exitCom = True

    s.close()
    return queue
