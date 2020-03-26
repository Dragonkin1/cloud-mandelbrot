import sys

# networking stuff
import xmlrpc.client
import socket

# get client hostname
hostname = socket.gethostname()
control_hostname = hostname

# socket constants
render_socket = 1234
control_socket = 5678
client_socket = 8000

# control node server
control_node = xmlrpc.client.ServerProxy("http://" + control_hostname + ":" + str(control_socket) + "/")

# ask user for input
def ask():
	quit = 3
	size = 9000
	while size>8000 or size<200:
		size = int(int(input("How large (tall and wide) do you want the image to be (in pixels, must be 8000 or less, ans greater than 200): "))/2)
	imagedata  = control_node.run(size) # generate mandelbrot with nodes
	out = open("outRECEIVED.png", "wb")
	out.write(imagedata.data) # write outbut bytes to a png file
	out.close()
	while not quit==1 and not quit==2:
		try:
			quit = int(input("Do you want to (1) quit or (2) render another?"))
			if quit==1:
				sys.exit(0)
			elif quit==2:
				ask()
		except Exception as e:
			pass # if answer isn't 1 or 2, ask again

# start run loop
while True:
	ask()
