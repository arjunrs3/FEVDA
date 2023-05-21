import numpy as np
import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from sympy import Symbol, Eq, solve
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
                   'gravity': 9.81,
                   'psi': 6894.75}
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

camberRRdata = 0.0024 / 0.00081 * np.array([[0, 4, 7, 10, 12, 14],[0.000832, 0.001, 0.00099, 0.00105, 0.0011, 0.0012]]) # data from Pac CAR scaled for Michelin Cross-Ply tires

def get_RRcoeff(wheel, camber): 
    #wheel.RRcoeff = np.interp(camber, camberRRdata[0], camberRRdata[1])
    wheel.RRcoeff = 0.00081
# get the cornering stiffness according to a simplified form of the Magic Formula
def get_cornering_stiffness(wheel, pressure): 
    a30 = 57.806
    a31 = 15.101
    a40 = -0.082
    a41 = 0.186
    print (wheel.fNormal)
    wheel.cornering_stiffness = (a30 + a31 * pressure * 10 ** -5) * np.sin(2 * np.arctan(float(wheel.fNormal/1000/(a40 + a41  * pressure * 10 ** -5))))
    print (wheel.cornering_stiffness)

# obtains baseline normal forces on each wheel through static balance 
def get_base_normal(self):
    f_front = Symbol('front')
    f_rear = Symbol('rear')
    F_balance = Eq(f_front + f_rear - self.total_weight, 0)
    M_balance = Eq(f_front * self.wheelbase -self.total_weight * self.COG[0], 0)
    normals = solve([F_balance, M_balance], f_front, f_rear, dict=True)[0]

    self.frontl.fNormal = normals[f_front] # double the weight
    self.frontr.fNormal = normals[f_front] # double the weight
    self.rear.fNormal = normals[f_rear]

# obtains the longitudinal force on each wheel given the normal forces
def get_f_longitudinal(self):
    for wheel in self.wheels.values(): 
        wheel.fLongitudinal = wheel.fNormal * wheel.RR_coeff