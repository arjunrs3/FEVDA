#!/usr/bin/env python
# coding: utf-8

# In[43]:


# A collection of algorithms to desribe the relationship between steering parameters and rolling resistance 
# For use by Eco Illini Supermileage
# Created by: Arjun Shah 
import numpy as np
import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
# stores unit conversions to m-kg-radians
class Unit_conversions: 
    inches = 0.0254
    feet = 0.3048
    cm = 0.01
    mm = 0.001
    radians = np.radians(1)
    pounds = 0.453592
    gravity = 9.81
    
Units = Unit_conversions()  
# Class to store vehicle parameters
class Vehicle():
    def __init__(self, Steering_type, Toe, Camber): 
        self.Steering_type = Steering_type
        self.Toe = Toe
        self.Camber = Camber
    Vehicle_type = "3-wheel"
    #Vehicle_steering = Steering(Steering_type, Toe, Camber)
    wheelbase = 71.725 * Units.inches
    track_width = 10.75 * 2 * Units.inches
    wheel_diameter = 20 * Units.inches
    COG = np.array([46 * Units.inches, 0, 0]) # see notes on VFCS (Vehicle fixed coordinate system)
    # plots vehicle according to given parameters
    def plot_vehicle(self): 
        theta = np.linspace(0, 2 * np.pi, 101)
        rear_x = self.wheel_diameter / 2 * np.cos(theta)
        rear_y = 0 * theta
        rear_z = self.wheel_diameter / 2 * np.sin(theta)
        
        front_r_x = self.wheelbase + self.wheel_diameter / 2 * np.cos(theta)
        front_r_y = np.full(shape=theta.size, fill_value=self.track_width)
        front_r_z = self.wheel_diameter / 2 * np.sin(theta)
        
        front_l_x = self.wheelbase + self.wheel_diameter / 2 * np.cos(theta)
        front_l_y = np.full(shape=theta.size, fill_value=-self.track_width)
        front_l_z = self.wheel_diameter / 2 * np.sin(theta)
        
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.plot(rear_x, rear_y, rear_z)
        ax.plot(front_r_x, front_r_y, front_r_z)
        ax.plot(front_l_x, front_l_y, front_l_z)
        ax.plot(self.COG[0], self.COG[1], self.COG[2], 'o')
        ax.set_aspect("equal")
        plt.show()
    # obtains baseline normal forces on each wheel through static balance 
    def get_base_normal(self):
        pass

    # obtains baseline rolling resistance
    # assumes level road with a linear relationship betwen weight and rolling resistance without toe or camber
    def get_baseline_resistance(self):
        pass

    # obtains straight-line rolling resistance (Toe included)
    def get_straight_resistance(self): 
        pass
# Class to store vehicle positioning attributes
class Position(): 
    pass 

# Class to instantiate different steering geometries (e.g., Ackermann, parallel)
class Steering(): 
    pass


# In[44]:


Eco = Vehicle("Ackermann", 0, 0)
Eco.plot_vehicle()


# In[ ]:




