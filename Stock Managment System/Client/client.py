import socket, sys

def runClient(ipaddr):
    s = socket.socket()
    host = ipaddr ## server = 131
    port = 2100

    s.connect((host, port))

    send = sys.argv[1].encode()
    s.send(send)

    exitCom = False

    while not exitCom:
        receive = s.recv(1024).decode()
        if receive != "":
            print (receive)

        if receive == "EXIT":
            exitCom = True

    s.close()
