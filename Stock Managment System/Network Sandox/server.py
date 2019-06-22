import socket, sys

s = socket.socket()
#host = socket.gethostname()
port = 2100
s.bind(('', port))

s.listen(5)
print("Listening on " + str(port))
while True:
    c, addr = s.accept()

    print ('Connection established with: ', addr)

    recieve = c.recv(1024).decode()
    print(recieve)
    if recieve == "TEST":
        c.send("EXIT".encode())
    else:
        print("Command not recognized")
        c.send("Command not recognized".encode())

    c.close()
