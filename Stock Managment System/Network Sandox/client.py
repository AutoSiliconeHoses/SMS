import socket, sys

s = socket.socket()
host = '192.168.1.131'
port = 2100

s.connect((host, port))

send = sys.argv[1].encode()
s.send(send)

while exit != True:
    recieve = s.recv(1024).decode()
    print (recieve)

    if recieve == "EXIT":
        print (recieve)
        exit = True
    else:
        exit = True

s.close()
