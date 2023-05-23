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
from Scripts.aero import *
from Scripts.misc import *

Units = create_units()

# class to store wheel forces and moments
class Wheel(): 
    fLongitudinal = 0
    fLateral = 0
    fNormal = 0
    mOverturning = 0 
    mRolling = 0 
    mAligning = 0
    I = 0.05
    def __init__(self, diameter, toe, camber, pressure, tag):
        self.tag = tag
        self.diameter = diameter
        self.toe = toe
        self.camber = camber
        self.pressure = pressure * Units.psi
        get_RRcoeff(self, self.camber)
        get_cornering_stiffness(self, self.pressure)

# class to store ICE parameters 
class ICE(): 
    fuel_density = 742.9 # kg / m ** 3 
    def __init__(self, BSFC, I):
        self.BSFC = BSFC / 60 / 60 # kg / s /kW
        self.I = I 
        self.torque_polynomial = get_torque_polynomial() # Nm
        self.power_polynomial = get_power_polynomial() # kW

# Class to store vehicle parameters
class Vehicle():
    # vehicle parameters
    vehicle_type = "3-wheel"
    wheelbase = 1.5 # 71.725 * Units.inches
    track_width = 0.5 # 10.75 * 2 * Units.inches
    #wheel_diameter = 20 * Units.inches
    #COG = np.array([45, 0, 0]) * Units.inches # see notes on VFCS (Vehicle fixed coordinate system)
    #vehicle_mass = 120 * Units.pounds
    #driver_mass = 110 * Units.pounds
    #total_mass = vehicle_mass + driver_mass
    #total_weight = total_mass * Units.gravity
    #frontal_area = 0.18 * 2
    #drag_coeff = 0.1
    misc_drag_coeff = 0
    #gear_ratio = 1 / 18 #gear ratio from engine to wheel
    #powertrain_efficiency = 0.9
    position = np.array([0, 0]).astype(float)
    velocity = np.array([0.01, 0.01]).astype(float)
    fuel_consumed = 0
    distance = 0
    ''' def __init__(self, powerplant, toe, camber): 
        self.powerplant = powerplant
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
            wheel.fLongitudinal = wheel.RRcoeff * wheel.fNormal '''
        # self.equiv_mass = self.total_mass + 4 / (self.wheel_diameter ** 2) * (self.powerplant.I * self.gear_ratio ** 2 / self.powertrain_efficiency + 3 * self.rear.I)
    def __init__(self, values):
        COG = values[0]
        vmass = values[1]
        dmass = values[2]
        area = values[3]
        cd = values[4]
        epower = values[5]
        gratio = values[6]
        toe = values[7]
        camber = values[8]
        diameter = values[9]
        pressure = values[10]
        BSFC = values[11]
        eInertia = values[12]
        minSpeed = values[13]
        maxSpeed = values[14]
        self.COG = np.array([COG, 0, 0]) * Units.inches
        self.vehicle_mass= vmass * Units.pounds
        self.driver_mass = dmass * Units.pounds
        self.total_mass = self.vehicle_mass + self.driver_mass
        self.total_weight = self.total_mass * Units.gravity
        self.frontal_area = area 
        self.drag_coeff = cd 
        self.powertrain_efficiency = epower
        self.gear_ratio = gratio
        self.toe = np.radians(toe)
        self.camber = np.radians(camber)
        self.wheel_diameter = diameter * Units.inches
        self.wheel_pressure = pressure
        self.frontl = Wheel(self.wheel_diameter, self.toe, self.camber, self.wheel_pressure, "front")
        self.frontr = Wheel(self.wheel_diameter, self.toe, self.camber, self.wheel_pressure, "front")
        self.rear = Wheel(self.wheel_diameter, 0, 0, self.wheel_pressure, "rear")
        self.wheels = {'frontl': self.frontl, 'frontr': self.frontr, 'rear': self.rear}
        get_base_normal(self)
        for wheel in self.wheels.values(): 
            get_cornering_stiffness(wheel, wheel.pressure)
            get_RRcoeff(wheel, wheel.camber)
            wheel.fLongitudinal = wheel.RRcoeff * wheel.fNormal
        self.powerplant = ICE(BSFC, eInertia)
        self.minSpeed = minSpeed * Units.mph
        self.maxSpeed = maxSpeed * Units.mph
        self.equiv_mass = self.total_mass + 4 / (self.wheel_diameter ** 2) * (self.powerplant.I * self.gear_ratio ** 2 / self.powertrain_efficiency + 3 * self.rear.I)



