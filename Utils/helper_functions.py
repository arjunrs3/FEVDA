import numpy as np
import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
# creates a Units class for attribute style access
class Units(dict):
    def __init__(self, *args, **kwargs):
        super(Units, self).__init__(*args, **kwargs)
        self.__dict__ = self
# initializes Units class
def create_units(): 
    Conversions = {'inches': 0.0254, 
                   'feet': 0.3048, 
                   'cm': 0.01, 
                   'mm': 0.001, 
                   'radians': np.radians(1),
                   'pounds': 0.453592,
                   'gravity': 9.81}
    return Units(Conversions)

# plot the vehicle for setup validation
def plot_vehicle(self):
    theta = np.linspace(0, 2 * np.pi, 51)
    camber = self.camber
    toe = self.toe

    rear_x = self.wheel_diameter / 2 * np.cos(theta)
    rear_y = 0 * theta
    rear_z = self.wheel_diameter / 2 * np.sin(theta)
    
    front_r_x = self.wheelbase - self.wheel_diameter / 2 * np.cos(theta) * np.cos(toe)
    front_r_y = np.full(shape=theta.size, fill_value=-self.track_width / 2) - self.wheel_diameter / 2 * np.cos(theta) * np.sin(toe) + self.wheel_diameter / 2 * np.sin(theta) * np.sin(camber)
    front_r_z = self.wheel_diameter / 2 * np.sin(theta) * np.cos(camber)
    
    front_l_x = self.wheelbase + self.wheel_diameter / 2 * np.cos(theta) * np.cos(toe)
    front_l_y = np.full(shape=theta.size, fill_value= self.track_width / 2) - self.wheel_diameter / 2 * np.cos(theta) * np.sin(toe) - self.wheel_diameter / 2 * np.sin(theta) * np.sin(camber)
    front_l_z = self.wheel_diameter / 2 * np.sin(theta) * np.cos(camber)
    
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot(rear_x, rear_y, rear_z)
    ax.plot(front_r_x, front_r_y, front_r_z, color='blue')
    ax.plot(front_l_x, front_l_y, front_l_z)
    ax.plot(self.COG[0], self.COG[1], self.COG[2], 'o')
    ax.set_aspect("equal")
    plt.show()