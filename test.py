from __future__ import division
 
import numpy as np
import matplotlib.pyplot as plt
 
m = 480
n = 320
quadant = "LOWERRIGHT"
 
s = 300  # Scale.
Z = np.full((n, m), 0 + 0j)

if(quadant == "UPPERRIGHT"):
    x = np.linspace(0, m / s, num=m).reshape((1, m))
    y = np.linspace(0, n / s, num=n).reshape((n, 1))
    C = np.tile(x, (n, 1)) + 1j * np.tile(y, (1, m))
elif(quadant == "UPPERLEFT"):
    x = np.linspace(-m / s, 0, num=m).reshape((1, m))
    y = np.linspace(0, n / s, num=n).reshape((n, 1))
    C = np.tile(x, (n, 1)) + 1j * np.tile(y, (1, m))
elif(quadant == "LOWERRIGHT"):
    x = np.linspace(0, m / s, num=m).reshape((1, m))
    y = np.linspace(-n / s, 0, num=n).reshape((n, 1))
    C = np.tile(x, (n, 1)) + 1j * np.tile(y, (1, m))
elif(quadant == "LOWERLEFT"):
    x = np.linspace(-m / s, 0, num=m).reshape((1, m))
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
 
# Save with Matplotlib using a colormap.
fig = plt.figure()
fig.set_size_inches(m / 100, n / 100)
ax = fig.add_axes([0, 0, 1, 1], frameon=False, aspect=1)
ax.set_xticks([])
ax.set_yticks([])
plt.imshow(np.flipud(N), cmap='plasma')
plt.savefig('julia-plt.png')
plt.close()

# https://matplotlib.org/3.1.0/tutorials/colors/colormaps.html
# https://tomroelandts.com/articles/how-to-compute-colorful-fractals-using-numpy-and-matplotlib
# https://tomroelandts.com/articles/how-to-compute-the-mandelbrot-set-using-numpy-array-operations