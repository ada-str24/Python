# langton's ant simulation

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

N = 0
E = 1
S = 2
W = 3

n = 30
a = np.zeros((2*n+1, 2*n+1))
antx, anty = n, n
ant_dir = N


def move_ant():
    global antx, anty, ant_dir
    if a[antx][anty] == 0:
        a[antx][anty] = 1
        ant_dir = (ant_dir+1) % 4
    else:
        a[antx][anty] = 0
        ant_dir = (ant_dir + 3) % 4
    if ant_dir == N:
        anty -= 1
    elif ant_dir == S:
        anty += 1
    elif ant_dir == W:
        antx -= 1
    else:
        antx += 1


# animation
fps = 14

fig = plt.figure()
im = plt.imshow(a, origin='lower', vmin=0, vmax=1)


def init():
    return im


def animate_func(i):
    move_ant()
    im.set_array(a)
    return im


anim = animation.FuncAnimation(fig, animate_func, interval=1000 / fps,)
plt.show()
