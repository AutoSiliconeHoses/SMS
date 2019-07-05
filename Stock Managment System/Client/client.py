import socket, sys

def runClient():
    s = socket.socket()
    host = '192.168.1.131' ## server = 131
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
