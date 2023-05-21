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
    def __init__(self, diameter, toe, camber, tag):
        self.tag = tag
        self.diameter = diameter
        self.toe = toe
        self.camber = camber
        get_RRcoeff(self, self.camber)
        get_cornering_stiffness(self, self.pressure)
        print (toe)
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
        self.toe = np.radians(toe)
        self.camber = np.radians(camber)
        # initializing wheels
        self.frontl = Wheel(self.wheel_diameter, self.toe, self.camber, "front")
        self.frontr = Wheel(self.wheel_diameter, self.toe, self.camber, "front")
        self.rear = Wheel(self.wheel_diameter, 0, 0, "rear")
        self.wheels = {'frontl': self.frontl, 'frontr': self.frontr, 'rear': self.rear}
        get_base_normal(self)
        for wheel in self.wheels.values(): 
            get_cornering_stiffness(wheel, wheel.pressure)
            get_RRcoeff(wheel, wheel.camber)
            wheel.fLongitudinal = wheel.RRcoeff * wheel.fNormal


# Class to store vehicle positioning attributes
class Position(): 
    pass 

# Class to instantiate different steering geometries (e.g., Ackermann, parallel)
class Steering(): 
    pass

Eco = Vehicle("Ackermann", 0.25, 0)
# plot_vehicle(Eco)

get_straight_rolling_resistance(Eco)





