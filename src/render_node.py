from __future__ import division
 
import numpy as np
import matplotlib.pyplot as plt

offset = 0.8

def mandelbrot(size, quadrant):
    m = size
    n = size
    Z = np.full((n, m), 0 + 0j)
    s = size - 50

    if(quadrant == "UPPERRIGHT"):
        x = np.linspace(0-offset, (m / s)-offset, num=m).reshape((1, m))
        y = np.linspace(0, n / s, num=n).reshape((n, 1))
        C = np.tile(x, (n, 1)) + 1j * np.tile(y, (1, m))
    elif(quadrant == "UPPERLEFT"):
        x = np.linspace((-m / s)-offset, 0-offset, num=m).reshape((1, m))
        y = np.linspace(0, n / s, num=n).reshape((n, 1))
        C = np.tile(x, (n, 1)) + 1j * np.tile(y, (1, m))
    elif(quadrant == "LOWERRIGHT"):
        x = np.linspace(0-offset, (m / s)-offset, num=m).reshape((1, m))
        y = np.linspace(-n / s, 0, num=n).reshape((n, 1))
        C = np.tile(x, (n, 1)) + 1j * np.tile(y, (1, m))
    elif(quadrant == "LOWERLEFT"):
        x = np.linspace((-m / s)-offset, 0-offset, num=m).reshape((1, m))
        y = np.linspace(-n / s, 0, num=n).reshape((n, 1))
        C = np.tile(x, (n, 1)) + 1j * np.tile(y, (1, m))
    else:
        print("ERROR: quadant's value is not set right")
        x = np.linspace(-m / s, m / s, num=m).reshape((1, m))
        y = np.linspace(-n / s, n / s, num=n).reshape((n, 1))
        C = np.tile(x, (n, 1)) + 1j * np.tile(y, (1, m))

    M = np.full((n, m), True, dtype=bool)
    N = np.zeros((n, m))
    for i in range(256):
        Z[M] = Z[M] * Z[M] + C[M]
        M[np.abs(Z) > 2] = False
        N[M] = i
    saveImage(quadrant, size, N)

def saveImage(name, size, colorArray):
    fig = plt.figure()
    fig.set_size_inches(size / 100, size / 100)
    ax = fig.add_axes([0, 0, 1, 1], frameon=False, aspect=1)
    ax.set_xticks([])
    ax.set_yticks([])
    plt.imshow(np.flipud(colorArray), cmap='Spectral')
    plt.savefig(name + '.png')
    plt.close()


