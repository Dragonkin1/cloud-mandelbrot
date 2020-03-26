#Authors: Reilly, Evan, and Guy
#Class: CS-351
#Purpose: This file will define what the control node does and acts within the mandelbrot computer grid

#import Python Libraries
import numpy as np
import matplotlib.pyplot as plt
import multiprocessing
from multiprocessing import Pool

#import Server Libraries
import xmlrpc.client
from xmlrpc.server import SimpleXMLRPCServer
import socket

#Get the host names of nodes
node1_hostname = socket.gethostname()
node2_hostname = socket.gethostname()
node3_hostname = socket.gethostname()
node4_hostname = socket.gethostname()
control_hostname = socket.gethostname()

#Set the port numbers of all of the nodes
render_socket = 1234
control_socket = 5678
client_socket = 8000

#Establish connection of RPC servers
node1 = xmlrpc.client.ServerProxy("http://" + node1_hostname + ":" + str(render_socket) + "/")
node2 = xmlrpc.client.ServerProxy("http://" + node2_hostname + ":" + str(render_socket) + "/")
node3 = xmlrpc.client.ServerProxy("http://" + node3_hostname + ":" + str(render_socket) + "/")
node4 = xmlrpc.client.ServerProxy("http://" + node4_hostname + ":" + str(render_socket) + "/")

#This function will combine the png files into a single big file
def combine_quadrants(images, qSize):
	hq,wq = (qSize, qSize)
	out = np.zeros(shape=(2*hq, 2*wq, 3))
	out[:hq, :wq]         = images[0]
	out[:hq, wq:2*wq]     = images[1]
	out[hq:2*hq, :wq]     = images[2]
	out[hq:2*hq, wq:2*wq] = images[3]
	plt.imshow(out)
	return save(out, 2*qSize)

#This Function will save the image to the local directory
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

#Make currentData and data gobals outside of any function
global currentData
global data
data = []
currentData = None

#This function will execute the order for rendernode to start working on a quadrant
def launchProc(nodeQuad):
	global currentData
	global data
	currentData = nodeQuad[0].mandelbrot(nodeQuad[1], nodeQuad[2])
	print(currentData)
	data.append(currentData)

#This function is the main function of control node. It will be called by the client node
def run(size):
	#Use the gobal currentData and Data
	global currentData
	global data

	#Append the different node jobs into a list and then process each job in different threads.
	nodeJobs = []
	nodeJobs.append(multiprocessing.Process(target=launchProc, args=([[node1, size, "UPPERLEFT"]])))
	nodeJobs.append(multiprocessing.Process(target=launchProc, args=([[node2, size, "UPPERRIGHT"]])))
	nodeJobs.append(multiprocessing.Process(target=launchProc, args=([[node3, size, "LOWERLEFT"]])))
	nodeJobs.append(multiprocessing.Process(target=launchProc, args=([[node4, size, "LOWERRIGHT"]])))

	#Let the user know that the program is starting
	print("starting")

	#itereate through the jobs and start each one
	for j in nodeJobs:
		j.start()
	
	#Wait for all of the jobs to be compelete
	for j in nodeJobs:
		j.join()

	#All of the jobs have been finished now 
	print("ending")

	#Writing all of the quadrants images down to the local directory
	for datum in data:
		datafile = open(datum[0], "wb")
		datafile.write(datum[1])
		datafile.close()

	quads = ["UPPERLEFT.png", "UPPERRIGHT.png", "LOWERLEFT.png", "LOWERRIGHT.png"]
	qImages = []

	for q in quads:
		qImages.append(plt.imread(q)[:,:,:3])

	#return a list with the filename and the data for the combined image
	return combine_quadrants(qImages, size)

#This function will send the combined image back to the client
def sendImage(filename):
    global client
    print("reading file")
    image = open(filename, "rb")
    data = xmlrpc.client.Binary(image.read())
    print("done")
    image.close()
    print("sending")
    return data.data

#Setting up the RPC server
server = SimpleXMLRPCServer((control_hostname, control_socket))
server.register_function(run, "run")
server.register_introspection_functions()
server.serve_forever()


