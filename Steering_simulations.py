# A collection of algorithms to desribe the relationship between steering parameters and rolling resistance 
# For use by Eco Illini Supermileage
# Created by: Arjun Shah 
import numpy as np
from sympy import Symbol, solve, Eq
import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
# stores unit conversions to m-kg-radians
from Utils.helper_functions import *
from Scripts.tires import *
Units = create_units()
# class to store wheel forces and moments
class Wheel(): 
    fLongitudinal = 0
    fLateral = 0
    fNormal = 0
    mOverturning = 0 
    mRolling = 0 
    mAligning = 0
    pressure = 87.022 * Units.psi
    def __init__(self, diameter, toe, camber):
        self.diameter = diameter
        self.toe = toe
        self.camber = camber
        get_RRcoeff(self, self.camber)
        get_cornering_stiffness(self, self.pressure)
# Class to store vehicle parameters
class Vehicle():
    # vehicle parameters
    vehicle_type = "3-wheel"
    wheelbase = 1.5 # 71.725 * Units.inches
    track_width = 0.5 # 10.75 * 2 * Units.inches
    wheel_diameter = 20 * Units.inches
    COG = np.array([1, 0, 0]) # see notes on VFCS (Vehicle fixed coordinate system)
    vehicle_mass = 165.35 * Units.pounds
    driver_mass = 0 * Units.pounds
    total_mass = vehicle_mass + driver_mass
    total_weight = total_mass * Units.gravity
    def __init__(self, steering_type, toe, camber): 
        self.steering_type = steering_type
        self.toe = toe * Units.radians
        self.camber = camber * Units.radians
        # initializing wheels
        self.frontl = Wheel(self.wheel_diameter, toe, camber)
        self.frontr = Wheel(self.wheel_diameter, toe, camber)
        self.rear = Wheel(self.wheel_diameter, 0, 0)
        self.wheels = {'frontl': self.frontl, 'frontr': self.frontr, 'rear': self.rear}


# Class to store vehicle positioning attributes
class Position(): 
    pass 

# Class to instantiate different steering geometries (e.g., Ackermann, parallel)
class Steering(): 
    pass

Eco = Vehicle("Ackermann", 0, 0)
# plot_vehicle(Eco)

get_turning_values(Eco, 8.33333, 15)





