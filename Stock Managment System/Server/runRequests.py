import socket, collections, time

# List of accepted commands
comlist = ["RUN", "CNFED", "UPDATE"]

# Checks commands
def commandCheck(c, args, q):
    if args[0] in comlist:  # Accepted commands
        q.append(args)  # Add to queue
        c.send(("You are #" + str(len(q)) + " in the queue").encode())
    elif args[0] == "QUEUE":  # give client everything in queue
        comq = ""
        for element in q:
            comq = comq + str(element) + "\n"
        c.send(comq.encode())
    else:  # Unknown command
        print("Command not recognized")
        c.send("Command not recognized".encode())  # change

def runRequests(q):
    # Get socket ready for use
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    port = 2100
    s.bind(('', port))

    # Start listening for connections
    s.listen(5)
    print("Listening on " + str(port))
    while True:
        # Connect with incoming client
        c, addr = s.accept()
        print('Connection established with: ', addr)

        # Receive command from client and split
        receive = c.recv(1024).decode()
        args = receive.split(" ")

        commandCheck(c, args, q)

        time.sleep(0.01)
        c.send("EXIT".encode())
        c.close()
