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
from Scripts.engine import *
from vehicle_setup import * 

Units = create_units()

# Force buildup 
def get_total_forces(Vehicle, velocity, engine_state, radius=""): 
    aero = get_aerodynamic_drag(Vehicle, velocity)
    if not radius: 
        tire = get_straight_rolling_resistance(Vehicle)
        total_force_normal = 0
    else: 
        tire, total_force_normal, angle = get_turning_values(Vehicle, velocity, radius)
    misc = get_misc_resistance(Vehicle)
    if engine_state == "burn": 
        engine = get_propulsive_force(Vehicle, velocity)
    else: 
        engine = 0
    total_force_tangent = engine - aero - tire - misc
    return (total_force_tangent)

def get_new_acceleration(Vehicle, engine_state, radius):
    orientation = Vehicle.velocity / np.linalg.norm(Vehicle.velocity)
    R = np.abs(float(radius)) 
    total_force_tangent = get_total_forces(Vehicle, np.linalg.norm(Vehicle.velocity), engine_state, R)
    atangent = total_force_tangent / Vehicle.equiv_mass * orientation
    total_a_normal = np.linalg.norm(Vehicle.velocity) ** 2 / R
    if float(radius) > 0: 
        anormal = total_a_normal * np.array([-orientation[1], orientation[0]])
    else: 
        anormal = total_a_normal * np.array([orientation[1], -orientation[0]])
    a = atangent + anormal 
    return a
def get_straight_acceleration(Vehicle, engine_state):
    orientation = Vehicle.velocity / np.linalg.norm(Vehicle.velocity)
    total_force_tangent = get_total_forces(Vehicle, np.linalg.norm(Vehicle.velocity), engine_state)  
    a = total_force_tangent / Vehicle.equiv_mass * orientation
    return a

def step(Vehicle, a, dt): 
    Vehicle.position = Vehicle.position + Vehicle.velocity * dt + 1/2 * a * dt ** 2
    Vehicle.velocity = Vehicle.velocity + a * dt
    Vehicle.position = Vehicle.position.astype(float)
    Vehicle.velocity = Vehicle.velocity.astype(float)
def reverse_step(Vehicle, a, dt): 
    Vehicle.position = Vehicle.position - Vehicle.velocity * dt - 1/2 * a * dt ** 2
    Vehicle.velocity = Vehicle.velocity - a * dt 
    Vehicle.position = Vehicle.position.astype(float)
    Vehicle.velocity = Vehicle.velocity.astype(float)


Engine = ICE()
Eco = Vehicle(Engine, 0, 0)

track = get_track()
Eco.position = np.array([0, 0]).astype(float)
Eco.velocity = np.array([-445.7664, 4.3831]) / 10000
dt_0 = 0.1
dt = 0.1
t = 0
burning = false
position_data = []
velocity_data = []
fuel_consumption = []
plt.axis([-800, 800, -100, 800])
for i in range (track[:, 0].size): 
    if track[i][0] == 0:
        # go straight for the specified distance
        target_distance = track[i][1]
        original_pos = Eco.position
        distance_traveled = 0 
        print (t)
        while distance_traveled < target_distance:
            t += dt
            if np.linalg.norm(Eco.velocity) < 15 * Units.mph and burning == false: 
                acc_straight = get_straight_acceleration(Eco, "burn")
                burning = true
                VFR = get_volumetric_fuel_rate(Eco, np.linalg.norm(Eco.velocity))
                Eco.fuel_consumed += VFR * dt
                print (VFR)
            elif np.linalg.norm(Eco.velocity) > 20 * Units.mph: 
                acc_straight = get_straight_acceleration(Eco, "coast")
                burning = false
            elif burning == true: 
                acc_straight = get_straight_acceleration(Eco, "burn")
                burning = true
                VFR = get_volumetric_fuel_rate(Eco, np.linalg.norm(Eco.velocity))
                Eco.fuel_consumed += VFR * dt
                print (VFR)
            else: 
                acc_straight = get_straight_acceleration(Eco, "coast")
                burning = false
            step(Eco, acc_straight, dt)
            distance_traveled = np.linalg.norm(Eco.position - original_pos)
            position_data.append([t, Eco.position[0], Eco.position[1]])
            velocity_data.append(np.linalg.norm(Eco.velocity))
            fuel_consumption.append(Eco.fuel_consumed)

    else: 
        target_radius = track[i][1]
        initial_orientation = Eco.velocity / np.linalg.norm(Eco.velocity)
        target_angle_turned = track[i][2]
        angle_turned = 0
        burning = false
        while angle_turned < target_angle_turned: 
            t += dt
            a_turn = get_new_acceleration(Eco, "coast", target_radius)
            step(Eco, a_turn, dt)
            current_orientation = Eco.velocity / np.linalg.norm(Eco.velocity)
            angle_turned = np.arccos(np.dot(current_orientation, initial_orientation))
            angle_turned = np.degrees(angle_turned)
            print (t)
            if angle_turned - target_angle_turned > 0.1: 
                t = t - dt
                reverse_step(Eco, a_turn, dt)
                angle_turned = np.arccos(np.dot(current_orientation, initial_orientation))
                angle_turned = np.degrees(angle_turned)
                dt = 1/2 * dt
                continue
            dt = dt_0
            position_data.append([t, Eco.position[0], Eco.position[1]])
            velocity_data.append(np.linalg.norm(Eco.velocity))
            fuel_consumption.append(Eco.fuel_consumed)
positions = np.array(position_data)
velocities = np.array(velocity_data)
fuel = np.array(fuel_consumption)
t = positions[:, 0]
x = positions[:, 1]
y = positions[:, 2]
plt.plot(x, y)
plt.title("position")
plt.show()

plt.plot(t, velocities / Units.mph)
plt.title("velocity vs. time")
plt.show()

plt.plot(t, fuel)
plt.title("fuel consumption vs. time")
plt.show()

for i in range(x.size): 
    if i > 0: 
        Eco.distance += np.linalg.norm(np.array([x[i], y[i]])- np.array([x[i-1], y[i-1]]))
total_mpg = Eco.distance * 0.00062137 / (Eco.fuel_consumed * 0.000264172)
print (Eco.distance * 0.00062137)
print (total_mpg)

            
