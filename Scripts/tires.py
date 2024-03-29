import numpy as np
import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from sympy import *
from scipy.optimize import fsolve
from Utils.helper_functions import *

# Solve the bicycle problem for a turn of given radius
'''Adequate for determining drag on tires while cornering, the bicycle model treats the front two wheels of a three wheel car
    as a single wheel which is supposed to connect to the rear wheel via a rigid chassis. The the steering angle is assumed as the average
    of the steering angle of the front two/inner and outer wheels. It assumes CG operates as the axis of symmetry on the longitudinal plane'''
def get_turning_values(Vehicle, velocity, radius):
    # Define relevant quantities for bicycle problem, combining quantities according to model 
    R = radius
    Xg = Vehicle.COG[0]
    Fc = Vehicle.total_mass * velocity ** 2 / R #centripetal contribution
    L = Vehicle.wheelbase
    Cf = (Vehicle.frontl.cornering_stiffness_turning + Vehicle.frontr.cornering_stiffness_turning) / 2
    Cr = Vehicle.rear.cornering_stiffness
    Fxf = Vehicle.frontl.fLongitudinal + Vehicle.frontr.fLongitudinal # combined for bicycle problem
    Fxr = Vehicle.rear.fLongitudinal
    #Solving the bicycle problem model function; defines a series of equations whose roots are solved for. See Pac CAR II: World's Most Efficient Vehicle book page 76 for more details.
    def func(x): 
        return [np.sin(x[3]) - (Xg - x[4])/R,
                np.tan(x[0] - x[1])-(L-x[4]) / (R * np.cos(x[3])),
                np.tan(x[2]) - x[4]/(R * np.cos(x[3])),
                x[5] - Cf * np.degrees(x[1]), 
                x[6] - Cr * np.degrees(x[2]),
                x[7] - Fxr - Fxf * np.cos(x[0]) + Fc * np.sin(x[3]) -x[5] * np.sin(x[0]),
                x[6] - Fxf * np.sin(x[0]) - Fc * np.cos(x[3]) +x[5] * np.cos(x[0]),
                -Xg * x[6] + (L - Xg) * (x[5] * np.cos(x[0]) - Fxf * np.sin(x[0]))]
    turning_values = fsolve(func, [0.1, 0.005, 0.005, 0.05, 1, 50, 50, 1])
    #Unpack solved values
    delta = turning_values[0]
    alphaf = turning_values[1]
    alphar = turning_values[2]
    beta = turning_values[3]
    e = turning_values[4]
    fflateral = turning_values[5]
    rflateral = turning_values[6]
    T = turning_values[7]
    #Return drag, centripital force contribution, and 
    return(T, Fc, beta)

# solve the straight line problem for a given toe
def get_straight_rolling_resistance(Vehicle):
    total_drag = 0 
    #Iterate through wheel items within vehicle, evaluate tire drag for rear and front two wheels separately, accounting for toe angle
    #and corresponding cornering stiffness for front two tires
    for tag, wheel in Vehicle.wheels.items():
        if tag == "rear":
            total_drag += wheel.fLongitudinal
        else:
            total_drag = total_drag + np.cos((wheel.toe)) * wheel.fLongitudinal + np.sin((wheel.toe)) * wheel.cornering_stiffness * np.degrees(wheel.toe) 
    return total_drag
