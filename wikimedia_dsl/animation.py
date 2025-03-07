from matplotlib.animation import FuncAnimation
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np


# creating a blank window
# for the animation
fig = plt.figure()
axis = plt.axes(xlim=(-50, 50),
                ylim=(-50, 50))

line, = axis.plot([], [], lw=2)

# what will our line dataset
# contain?


def init():
    line.set_data([], [])
    return line,


# initializing empty values
# for x and y co-ordinates
xdata, ydata = [], []

# animation function


def animate(i):
    # t is a parameter which varies
    # with the frame number
    t = 0.1 * i

    # x, y values to be plotted
    x = t * np.sin(t)
    y = t * np.cos(t)

    # appending values to the previously
    # empty x and y data holders
    xdata.append(x)
    ydata.append(y)
    line.set_data(xdata, ydata)

    return line,


# calling the animation function
anim = animation.FuncAnimation(fig, animate,
                               init_func=init,
                               frames=500,
                               interval=20,
                               blit=True)

# saves the animation in our desktop
anim.save('growingCoil.mp4', writer='ffmpeg', fps=30)

# %%


fig, ax = plt.subplots()
xdata, ydata = [], []
ln, = ax.plot([], [], 'ro')


def init():
    ax.set_xlim(0, 2*np.pi)
    ax.set_ylim(-1, 1)
    return ln,


def update(frame):
    xdata.append(frame)
    ydata.append(np.sin(frame))
    ln.set_data(xdata, ydata)
    return ln,


ani = FuncAnimation(fig, update, frames=np.linspace(0, 2*np.pi, 128),
                    init_func=init, blit=True)
plt.show()

# %%
