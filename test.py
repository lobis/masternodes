import matplotlib.pyplot as plt
import numpy as np

# draw the figure so the animations will work
fig = plt.gcf()
fig.show()
fig.canvas.draw()

while True:
    # compute something
    plt.plot([1], [2])  # plot something

    # update canvas immediately
    plt.xlim([0, 100])
    plt.ylim([0, 100])
    # plt.pause(0.01)  # I ain't needed!!!
fig.canvas.draw()