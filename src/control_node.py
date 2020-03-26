import numpy as np
import matplotlib.pyplot as plt
import multiprocessing
from multiprocessing import Pool

import xmlrpc.client
from xmlrpc.server import SimpleXMLRPCServer
import socket

node1_hostname = socket.gethostname()
node2_hostname = socket.gethostname()
node3_hostname = socket.gethostname()
node4_hostname = socket.gethostname()
control_hostname = socket.gethostname()

render_socket = 1234
control_socket = 5678
client_socket = 8000

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
	return save(out, 2*qSize)

def save(image, size):
	fig = plt.figure()
	fig.set_size_inches(size / 100, size / 100)
	ax = fig.add_axes([0, 0, 1, 1], frameon=False, aspect=1)
	ax.set_xticks([])
	ax.set_yticks([])
	plt.imshow(image)
	plt.savefig('out.png')
	plt.close()
	return sendImage("out.png")

global currentData
global data
data = []
currentData = None

def launchProc(nodeQuad):
	global currentData
	global data
	currentData = nodeQuad[0].mandelbrot(nodeQuad[1], nodeQuad[2])
	print(currentData)
	data.append(currentData)

def run(size):
	global currentData
	global data

	nodeJobs = []
	nodeJobs.append(multiprocessing.Process(target=launchProc, args=([[node1, size, "UPPERLEFT"]])))
	nodeJobs.append(multiprocessing.Process(target=launchProc, args=([[node2, size, "UPPERRIGHT"]])))
	nodeJobs.append(multiprocessing.Process(target=launchProc, args=([[node3, size, "LOWERLEFT"]])))
	nodeJobs.append(multiprocessing.Process(target=launchProc, args=([[node4, size, "LOWERRIGHT"]])))

	print("starting")

	for j in nodeJobs:
		j.start()
	for j in nodeJobs:
		j.join()

	print("ending")
	for datum in data:
		datafile = open(datum[0], "wb")
		datafile.write(datum[1])
		datafile.close()

	quads = ["UPPERLEFT.png", "UPPERRIGHT.png", "LOWERLEFT.png", "LOWERRIGHT.png"]
	qImages = []

	for q in quads:
		qImages.append(plt.imread(q)[:,:,:3])

	return combine_quadrants(qImages, size)

def sendImage(filename):
    global client
    print("reading file")
    image = open(filename, "rb")
    data = xmlrpc.client.Binary(image.read())
    print("done")
    image.close()
    print("sending")
    return data.data

server = SimpleXMLRPCServer((control_hostname, control_socket))
server.register_function(run, "run")
server.register_introspection_functions()
server.serve_forever()


