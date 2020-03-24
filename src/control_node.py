import numpy as np
import matplotlib.pyplot as plt
import render_node
import multiprocessing

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

def run(size):
	threads = []
	threads.append(multiprocessing.Process(target=render_node.mandelbrot, args=(size, "UPPERLEFT")))
	threads.append(multiprocessing.Process(target=render_node.mandelbrot, args=(size, "UPPERRIGHT")))
	threads.append(multiprocessing.Process(target=render_node.mandelbrot, args=(size, "LOWERLEFT")))
	threads.append(multiprocessing.Process(target=render_node.mandelbrot, args=(size, "LOWERRIGHT")))

	for t in threads:
		t.start()

	for t in threads:
		t.join()

	quads = ["UPPERLEFT.png", "UPPERRIGHT.png", "LOWERLEFT.png", "LOWERRIGHT.png"]
	qImages = []

	for q in quads:
		qImages.append(plt.imread(q)[:,:,:3])

	combine_quadrants(qImages, size)
