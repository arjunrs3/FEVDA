import matplotlib.pyplot as plt
from Utils.helper_functions import *

Units = create_units()

def plot(t, x, y, velocities, fuel):
    plt.figure()
    plt.scatter(x, y, c = velocities, cmap = 'RdYlGn')
    plt.title("position")

    plt.figure()
    plt.plot(t, np.array(velocities) / Units.mph)
    plt.title("velocity vs. time")

    plt.figure()
    plt.plot(t, fuel)
    plt.title("fuel consumption vs. time")
    plt.show()