import sys

import xmlrpc.client
from xmlrpc.server import SimpleXMLRPCServer
import socket

hostname = socket.gethostname()
control_hostname = "CripDev"

render_socket = 1234
control_socket = 5678
client_socket = 8000

control_node = xmlrpc.client.ServerProxy("http://" + control_hostname + ":" + str(control_socket) + "/")

def ask():
	quit = 3
	size = 9000
	while size>8000 or size<0:
		size = int(int(input("How large (tall and wide) do you want the image to be (in pixels, must be 8000 or less): "))/2)
	control_node.connectInit(hostname)
	control_node.run(size)
	while not quit==1 and not quit==2:
		try:
			quit = int(input("Do you want to (1) quit or (2) render another?"))
			if quit==1:
				sys.exit(0)
			elif quit==2:
				ask()
		except Exception as e:
			pass

def receiveImage(filename, data):
	imagefile =  open(filename[:-4] + "_recv.png", "wb")
	print("writing file")
	imagefile.write(data.data)
	print("done")
	imagefile.close()
	return True

server = SimpleXMLRPCServer((hostname, client_socket))
server.register_function(receiveImage, "receiveImage")

while True:
	ask()
	server.handle_request()

