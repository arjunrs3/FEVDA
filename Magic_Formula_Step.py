import scipy
import numpy as np
from Scripts.tires import *
from Scripts.aero import *
from Scripts.engine import *
from Scripts.misc import *
from vehicle_setup import *
import matplotlib.pyplot as plt 

def get_new_acceleration(Vehicle, velocity, engine_state, radius = None):
    orientation = velocity / np.linalg.norm(velocity)
    
    total_force_tangent = get_total_forces(Vehicle, np.linalg.norm(velocity), engine_state, radius)
    atangent = total_force_tangent / Vehicle.equiv_mass * orientation
    if float(radius) == 0:
        anormal = [0,0]
        total_a_normal = 0
    else:
        total_a_normal = np.linalg.norm(velocity) ** 2 / radius
        R = np.abs(float(radius)) 
    if float(radius) > 0: 
        anormal = total_a_normal * np.array([-orientation[1], orientation[0]])
    else: 
        anormal = total_a_normal * np.array([orientation[1], -orientation[0]])
    a = atangent + anormal 
    return a

def get_total_forces(Vehicle, velocity, engine_state, radius=""): 
    aero = get_aerodynamic_drag(Vehicle, velocity)

    if radius == 0: 
        tire = get_straight_rolling_resistance(Vehicle)
        total_force_normal = 0
    else: 
        tire, total_force_normal, angle = get_turning_values(Vehicle, velocity, radius)
    misc = get_misc_resistance(Vehicle)
    if engine_state == true: 
        engine = get_propulsive_force(Vehicle, velocity)
    else: 
        engine = 0
    total_force_tangent = engine - aero - tire - misc
    return (total_force_tangent)


def dy_dt(t, y, Vehicle, maneuver, radius, initial_position, initial_velocity):
    burning = true if y[10] == 1 else false
    Eco = Vehicle
    current_position = np.array([y[0], y[1]])
    current_velocity = np.array([y[2], y[3]])
    velocity_norm = np.linalg.norm(current_velocity)
    current_orientation = current_velocity / np.linalg.norm(current_velocity)
    if maneuver == "straight":
        distance = np.linalg.norm(current_position - initial_position)
        if burning == true:
            VFR = get_volumetric_fuel_rate(Eco, np.linalg.norm(current_velocity))
        else:
            VFR = 0

        if np.linalg.norm(current_velocity) < 9 and burning == false: 
            burning = true
        elif np.linalg.norm(current_velocity) > 10: 
            burning = false
        elif burning == true: 
            burning = true
        else: 
            burning = false
    else:
        burning = false
    acceleration = get_new_acceleration(Vehicle, current_velocity, burning, radius)
    y[4] = acceleration[0]
    y[5] = acceleration[1]
    #y[6] = distance
    dp_x = y[2]
    dp_y = y[3]
    dv_x = y[4]
    dv_y = y[5]
    burning_val = 1 if burning else 0
    y[10] = burning_val


    dy = [dp_x,dp_y,dv_x,dv_y,0,0,1,VFR,0,0,0]

    return dy

    

def step(Vehicle, a, dt):
    Vehicle.position = Vehicle.position + Vehicle.velocity * dt + 1/2 * a * dt ** 2
    Vehicle.velocity = Vehicle.velocity + a * dt
    Vehicle.position = Vehicle.position.astype(float)
    Vehicle.velocity = Vehicle.velocity.astype(float)

def magic_main(track, values):
    y0 = [0,0,1,0,0,0,0,0,0,0,0] #position(x,y) velocity(x,y), acceleration(x,y), distance,total fuel consumption, aero drag, tire drag, engine force
    eco = Vehicle(values)
    total_distance = 100
    def reached(t,y,Vehicle,maneuver,radius,initial_position,initial_velocity):
        total_distance = 100
        print (y[6] - total_distance)
        return float((y[6]) - total_distance)
    reached.terminal = true

    solution = scipy.integrate.solve_ivp(dy_dt,[0,500],y0,events = reached, args = (eco,"straight", 0, [0,0], [1,0]), max_step=10) #magic formula magic
    variables = solution.y
    accelerations = np.c_[variables[4], variables[5]]
    velocities = np.c_[variables[2], variables[3]]
    veloc_norm = np.array([np.linalg.norm(a) for a in velocities])
    time = solution.t
    accel_norm = np.array([np.linalg.norm(k) for k in accelerations])
    print(solution.y[0])
    print (solution.y[6])
    print("Done")

    veloc_fig = plt.figure()
    plt.plot(time, veloc_norm)

    fig1 = plt.figure()
    plt.plot(time, accel_norm)

    fig2 = plt.figure()
    plt.plot(solution.y[0], solution.y[1])

    plt.show()
