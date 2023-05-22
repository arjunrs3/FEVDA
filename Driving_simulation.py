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

def get_new_acceleration(Vehicle, engine_state, radius="", direction=""):
    orientation = Vehicle.velocity / np.linalg.norm(Vehicle.velocity)
    if not radius: 
        total_force_tangent = get_total_forces(Vehicle, np.linalg.norm(Vehicle.velocity), engine_state)  
        a = total_force_tangent / Vehicle.equiv_mass * orientation
    else: 
        total_force_tangent = get_total_forces(Vehicle, np.linalg.norm(Vehicle.velocity), engine_state, radius)
        atangent = total_force_tangent / Vehicle.equiv_mass * orientation
        total_a_normal = np.linalg.norm(Vehicle.velocity) ** 2 / radius
        if direction == 'left': 
            anormal = total_a_normal * np.array([-orientation[1], orientation[0]])
        if direction == 'right': 
            anormal = total_a_normal * np.array([orientation[1], -orientation[0]])
        a = atangent + anormal 
    return a

def step(Vehicle, a, dt): 
    Vehicle.position = Vehicle.position + Vehicle.velocity * dt
    Vehicle.velocity = Vehicle.velocity + a * dt
    Vehicle.velocity = Vehicle.velocity.astype(float)
dt = 0.01

Engine = ICE()
Eco = Vehicle(Engine, 0, 0)

positions = []
velocities = []
accelerations = []
t = []
fuel_consumption = [0]
for i in range (1000): 
    t.append(i * dt)
    a = get_new_acceleration(Eco, "burn")
    # print (get_volumetric_fuel_rate(Eco, np.linalg.norm(Eco.velocity)))
    fuel_consumption.append(get_volumetric_fuel_rate(Eco, np.linalg.norm(Eco.velocity)) * dt + fuel_consumption[i])
    positions.append(Eco.position)
    velocities.append(np.linalg.norm(Eco.velocity.astype(float)))
    atangent = np.dot(a, Eco.velocity / np.linalg.norm(Eco.velocity))
    accelerations.append(atangent)
    step(Eco, a, dt)
for i in range (500): 
    t.append(i * dt + 499 * dt)
    a = get_new_acceleration(Eco, "coast")
    fuel_consumption.append(fuel_consumption[i + 499])
    positions.append(Eco.position)
    velocities.append(np.linalg.norm(Eco.velocity))
    atangent = np.dot(a, Eco.velocity / np.linalg.norm(Eco.velocity))
    accelerations.append(atangent)
    step(Eco, a, dt)
for i in range (500): 
    t.append(i * dt + 998 * dt)
    a = get_new_acceleration(Eco, "coast", 15, "right")
    fuel_consumption.append(fuel_consumption[i + 998])
    positions.append(Eco.position)
    velocities.append(np.linalg.norm(Eco.velocity))
    atangent = np.dot(a, Eco.velocity / np.linalg.norm(Eco.velocity))
    accelerations.append(atangent)
    step(Eco, a, dt)
for i in range (500): 
    t.append(i * dt + 1497 * dt)
    a = get_new_acceleration(Eco, "burn")
    # print (get_volumetric_fuel_rate(Eco, np.linalg.norm(Eco.velocity)))
    fuel_consumption.append(get_volumetric_fuel_rate(Eco, np.linalg.norm(Eco.velocity)) * dt + fuel_consumption[i + 1497])
    positions.append(Eco.position)
    velocities.append(np.linalg.norm(Eco.velocity.astype(float)))
    atangent = np.dot(a, Eco.velocity / np.linalg.norm(Eco.velocity))
    accelerations.append(atangent)
    step(Eco, a, dt)

xpositions = np.array(positions)[:, 0]
ypositions = np.array(positions)[:, 1]
velocities = np.array(velocities)
accelerations = np.array(accelerations)
fuel_consumption.pop(0)
fuel_consumption = np.array(fuel_consumption)
t = np.array(t)
fig = plt.figure()
plt.plot(xpositions, ypositions)
plt.title("position")
plt.show()

fig = plt.figure()
plt.plot(t, xpositions)
plt.title("position vs time")
plt.show()

fig = plt.figure()
plt.plot(t, velocities)
plt.title("velocity vs time")
plt.show()

fig = plt.figure()
plt.plot(t, accelerations)
plt.title("tangential acceleration vs time")
plt.show()

fig = plt.figure()
plt.plot(t, fuel_consumption)
plt.title("fuel consumption (ml) vs time")
plt.show()