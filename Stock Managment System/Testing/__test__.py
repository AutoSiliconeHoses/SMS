import socket, sys, pprint

tests = open("Testing/tests.txt")

def serverTest(ipaddr, test):
	s = socket.socket()
	host = ipaddr ## server = 131
	port = 2100
	s.connect((host, port))
	s.send(test.encode())

	while True:
		receive = s.recv(1024).decode()
		if receive != "":
			print(receive)

		if receive == "EXIT":
			break

	s.close()
for row in tests.readlines():
	serverTest("192.168.1.99", str(row)) # Ray: 99 Dan: 110 Server: 13
print("Started tests. Check the server for completion.")
