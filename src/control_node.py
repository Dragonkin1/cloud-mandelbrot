import numpy as np
import matplotlib.pyplot as plt
import multiprocessing

import xmlrpc.client
from xmlrpc.server import SimpleXMLRPCServer
import socket

global client_hostname
client_hostname = None

node1_hostname = "CripDev"
node2_hostname = "CripDev"
node3_hostname = "CripDev"
node4_hostname = "CripDev"
control_hostname = socket.gethostname()

render_socket = 1234
control_socket = 5678
client_socket = 8000

global client
client = None

node1 = xmlrpc.client.ServerProxy("http://" + node1_hostname + ":" + str(render_socket) + "/")
node2 = xmlrpc.client.ServerProxy("http://" + node2_hostname + ":" + str(render_socket) + "/")
node3 = xmlrpc.client.ServerProxy("http://" + node3_hostname + ":" + str(render_socket) + "/")
node4 = xmlrpc.client.ServerProxy("http://" + node4_hostname + ":" + str(render_socket) + "/")

def combine_quadrants(images, qSize):
	hq,wq = (qSize, qSize)
	out = np.zeros(shape=(2*hq, 2*wq, 3))
	out[:hq, :wq]         = images[0]
	out[:hq, wq:2*wq]     = images[1]
	out[hq:2*hq, :wq]     = images[2]
	out[hq:2*hq, wq:2*wq] = images[3]
	plt.imshow(out)
	save(out, 2*qSize)

def save(image, size):
	fig = plt.figure()
	fig.set_size_inches(size / 100, size / 100)
	ax = fig.add_axes([0, 0, 1, 1], frameon=False, aspect=1)
	ax.set_xticks([])
	ax.set_yticks([])
	plt.imshow(image)
	plt.savefig('out.png')
	plt.close()
	sendImage("out.png")

def run(size):
	threads = []
	threads.append(multiprocessing.Process(target=node1.mandelbrot, args=(size, "UPPERLEFT")))
	threads.append(multiprocessing.Process(target=node2.mandelbrot, args=(size, "UPPERRIGHT")))
	threads.append(multiprocessing.Process(target=node3.mandelbrot, args=(size, "LOWERLEFT")))
	threads.append(multiprocessing.Process(target=node4.mandelbrot, args=(size, "LOWERRIGHT")))

	for t in threads:
		print("starting")
		t.start()
		

	for t in threads:
		t.join()
		print("ending")

	quads = ["UPPERLEFT.png", "UPPERRIGHT.png", "LOWERLEFT.png", "LOWERRIGHT.png"]
	qImages = []

	for q in quads:
		qImages.append(plt.imread(q)[:,:,:3])

	combine_quadrants(qImages, size)
	return True

def receiveImage(filename, data):
	print("receiving")
	imagefile = open(filename, "wb")
	print("writing file")
	imagefile.write(data.data)
	print("done")
	imagefile.close()
	return True

def sendImage(filename):
    global client
    print("reading file")
    image = open(filename, "rb")
    data = xmlrpc.client.Binary(image.read())
    print("done")
    image.close()
    print("sending")
    client.receiveImage(filename, data)
    print("done")

def connectInit(host):
	global client_hostname
	global client
	client_hostname = host
	client = xmlrpc.client.ServerProxy("http://" + client_hostname + ":" + str(client_socket) + "/")
	return True

server = SimpleXMLRPCServer((control_hostname, control_socket))
server.register_function(run, "run")
server.register_function(receiveImage, "receiveImage")
server.register_function(connectInit, "connectInit")
server.serve_forever()


