import viztools as vt
import matplotlib.pyplot as plt
import numpy as np


n = 100
x = range(10)
ys = np.ones([n, len(x)])

colors = vt.rainbowify(n=n, saturation=0)
# colors = vt.monochromify(n=n, base_color='orange')

for ii in range(len(ys)):
	y = ys[ii] * ii
	plt.plot(x, y, color=colors[ii])

plt.show()
