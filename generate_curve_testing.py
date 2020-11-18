from generate_curve import generate_curve
import matplotlib.pyplot as plt
from vector import *
import random
import numpy as np

seedx = random.uniform(0, 1000)
seedy = random.uniform(0, 1000)
Pi = Vector(1, 1)
Pf = Vector(4, 3)
wl = 1
phi_i = 0
phi_f = 0
n = 100
b = 1
w = 0.05
B = Vector(0, 0) - Khat

_, x1, y1 = generate_curve(Pi, Pf, 
    n, b, 1, phi_i, phi_f, w, wl, B, seedx, seedy)

plt.plot(x1, y1)
plt.show()


plt.ion()

fig = plt.figure()
ax = fig.add_subplot(111)
line1, = ax.plot(x1, y1, 'r-')

# for phase in np.linspace(0, 10*np.pi, 500):
#     line1.set_ydata(np.sin(x + phase))
#     fig.canvas.draw()
#     fig.canvas.flush_events()


while True:
    _, x1, y1 = generate_curve(Pi, Pf, 
        n, b, 1, phi_i, phi_f, w, wl, B, seedx, seedy)

    # _, x2, y2 = generate_curve(Pi, Pf, 
    #     n, b, 1, phi_i, phi_f, w, wl, B, seedx, seedy)

    # _, x3, y3 = generate_curve(Pi, Pf, 
    #     n, b, 2, phi_i, phi_f, w, wl, B, seedx, seedy)

    seedy += 0.03

    line1.set_xdata(x1)
    line1.set_ydata(y1)
    fig.canvas.draw()
    fig.canvas.flush_events()


# plt.plot(x1, y1, color = "blue")
# # plt.plot(x2, y2, color = "blue")
# # plt.plot(x3, y3, color = "blue")
# plt.scatter([Pi.x, Pf.x], [Pi.y, Pf.y], color = "red")
# # plt.xlim([0, 5])
# # plt.ylim([0, 5])
# plt.show()
