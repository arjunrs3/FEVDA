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

Units = create_units()
# class to store wheel forces and moments
class Wheel(): 
    fLongitudinal = 0
    fLateral = 0
    fNormal = 0
    mOverturning = 0 
    mRolling = 0 
    mAligning = 0
    def __init__(self, diameter, toe, camber):
        self.diameter = diameter
        self.toe = toe
        self.camber = camber
# Class to store vehicle parameters
class Vehicle():
    # vehicle parameters
    vehicle_type = "3-wheel"
    wheelbase = 71.725 * Units.inches
    track_width = 10.75 * 2 * Units.inches
    wheel_diameter = 20 * Units.inches
    COG = np.array([40 * Units.inches, 0, 0]) # see notes on VFCS (Vehicle fixed coordinate system)
    vehicle_mass = 120 * Units.pounds
    driver_mass = 110 * Units.pounds
    total_mass = vehicle_mass + driver_mass
    total_weight = total_mass * Units.gravity
    RR_coeff = 0.0024 # Rolling Resistance Coefficient
    def __init__(self, steering_type, toe, camber): 
        self.steering_type = steering_type
        self.toe = toe * Units.radians
        self.camber = camber * Units.radians
        # initializing wheels
        self.frontl = Wheel(self.wheel_diameter, toe, camber)
        self.frontr = Wheel(self.wheel_diameter, toe, camber)
        self.rear = Wheel(self.wheel_diameter, 0, 0)
        self.wheels = {'frontl': self.frontl, 'frontr': self.frontr, 'rear': self.rear}
    # obtains baseline normal forces on each wheel through static balance 
    def get_base_normal(self):
        f_front = Symbol('front')
        f_rear = Symbol('rear')
        F_balance = Eq(f_front + f_rear - self.total_weight, 0)
        M_balance = Eq(f_front * self.wheelbase -self.total_weight * self.COG[0], 0)
        normals = solve([F_balance, M_balance], f_front, f_rear, dict=True)[0]

        self.frontl.fNormal = normals[f_front]/2
        self.frontr.fNormal = normals[f_front]/2
        self.rear.fNormal = normals[f_rear]

    # obtains the longitudinal force on each wheel given the normal forces
    def get_f_longitudinal(self):
        for wheel in self.wheels.values(): 
            wheel.fLongitudinal = wheel.fNormal * self.RR_coeff

# Class to store vehicle positioning attributes
class Position(): 
    pass 

# Class to instantiate different steering geometries (e.g., Ackermann, parallel)
class Steering(): 
    pass

Eco = Vehicle("Ackermann", 20, 20)
plot_vehicle(Eco)
Eco.get_base_normal()
Eco.get_f_longitudinal()
print (Eco.frontl.fLongitudinal, Eco.rear.fLongitudinal)





