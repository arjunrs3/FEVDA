import scipy
import numpy as np
from Scripts.tires import *
from Scripts.aero import *
from Scripts.engine import *
from Scripts.misc import *
from vehicle_setup import *
import matplotlib.pyplot as plt 

# Let's implement a similar structure except that a new solve_ivp happens when we burn or coast. 
# an input to solve_IVP is then burning or coasting, which will be a global variable that solve_ivp can reset 

def get_acceleration(Vehicle, velocity, orientation, engine_state, radius=None):
    R = np.abs(radius) if radius is not None else None
    total_force_tangent = get_tangent_forces(Vehicle, np.linalg.norm(velocity), engine_state, R)
    accel_tangent = total_force_tangent / Vehicle.equiv_mass * orientation
    if radius is not None: # there will also be a normal force 
        total_a_normal = np.linalg.norm(velocity) ** 2 / R 
        print(total_a_normal)
        if float(radius) > 0: 
            accel_normal = total_a_normal * np.array([-orientation[1], orientation[0]])
        else: 
            accel_normal = total_a_normal * np.array([orientation[1], -orientation[0]])
    else: # going straight, no normal force 
        accel_normal = [0, 0]
    a = accel_tangent + accel_normal
    return a 

def get_tangent_forces(Vehicle, velocity, engine_state, radius=None):
    aero = get_aerodynamic_drag(Vehicle, velocity)
    if radius is None: 
        tire = get_straight_rolling_resistance(Vehicle)
    else: 
        tire, total_force_normal, angle = get_turning_values(Vehicle, velocity, radius)
    misc = get_misc_resistance(Vehicle)
    if engine_state == "burn": 
        engine = get_propulsive_force(Vehicle, velocity)
    else: 
        engine = 0 
    total_force_tangent = engine - aero - tire - misc 
    return (total_force_tangent)

def dy_dt_straight_burning(t, y, vehicle, orientation, initial_position, distance):
    # y = [x, y, vx, vy, ax, ay, fuel_consumed]
    velocity = np.array([y[2], y[3]])
    engine_state = "burn"
    a = get_acceleration(Vehicle=vehicle, velocity=velocity, orientation=orientation, engine_state=engine_state)
    VFR = get_volumetric_fuel_rate(vehicle, np.linalg.norm(velocity))
    dx = velocity[0]
    dy = velocity[1]
    dvx = a[0]
    dvy = a[1]
    y[4] = a[0]
    y[5] = a[1]
    dfuel = VFR
    dy = [dx, dy, dvx, dvy, 0, 0, dfuel]
    return dy

def dy_dt_straight_coasting(t, y, vehicle, orientation, initial_position, distance):
    velocity = np.array([y[2], y[3]])
    engine_state = "coast"
    a = get_acceleration(Vehicle=vehicle, velocity=velocity, orientation=orientation, engine_state=engine_state)
    dx = velocity[0]
    dy = velocity[1]
    dvx = a[0]
    dvy = a[1]
    y[4] = a[0]
    y[5] = a[1]
    dfuel = 0
    dy = [dx, dy, dvx, dvy, 0, 0, dfuel]
    return dy

def dy_dt_turning(t, y, vehicle, radius, angle, initial_orientation): #always coasting on turning
    engine_state = "coast"
    velocity = np.array([y[2], y[3]])
    current_orientation = velocity / np.linalg.norm(velocity)
    a = get_acceleration(Vehicle = vehicle,velocity = velocity, orientation = current_orientation, engine_state = engine_state, radius = radius)
    dx = velocity[0]
    dy = velocity[1]
    dvx = a[0]
    dvy = a[1]
    y[4] = a[0]
    y[5] = a[1]
    dfuel = 0
    dy = [dx, dy, dvx, dvy, 0, 0, dfuel]
    return dy




     
def run_simulation(track, values):
    eco = Vehicle(values)
    y0 = [0, 0, 5, 0, 0, 0, 0]
    initial_orientation = np.array([1, 0])
    initial_position = np.array([0, 0])
    '''     def max_velocity(t, y, vehicle, initial_orientation, initial_position, distance):
        velocity = np.array([y[2], y[3]])
        speed = np.linalg.norm(velocity)
        return vehicle.maxSpeed - speed
    max_velocity.terminal=True


    def min_velocity(t, y, vehicle, initial_orientation, initial_position, distance):
        velocity = np.array([y[2], y[3]])
        speed = np.linalg.norm(velocity)
        return vehicle.minSpeed - speed
    min_velocity.terminal=True


    solution_burn = scipy.integrate.solve_ivp(dy_dt_straight_burning, [0, 500], y0, events=max_velocity, args=(eco, initial_orientation, initial_position, distance), max_step=1)
    solution_coast = scipy.integrate.solve_ivp(dy_dt_straight_coasting, [0, 500], y0, events=min_velocity, args=(eco, initial_orientation, initial_position, distance), max_step=1)
    print(solution_burn.y[0])
    print(solution_coast.y[0])
    plot (solution_burn.t, solution_burn.y[0])
    plot(solution_coast.t, solution_coast.y[0])
    '''
    #solutions, times = straight(eco, y0, initial_orientation, 2000, 0)


    """ solutions, times = turning(eco, y0, initial_orientation, np.radians(90), 0, 20)
    time = np.array([element for sublist in times for element in sublist.tolist()])
    x_positions = [k[0] for k in solutions]
    x_positions = np.array([element for sublist in x_positions for element in sublist.tolist()])
    y_positions = [k[1] for k in solutions]
    y_positions = np.array([element for sublist in y_positions for element in sublist.tolist()])
    velocities = [k[2] for k in solutions]
    velocities = np.array([element for sublist in velocities for element in sublist.tolist()])
    plot(time, velocities)
    plot(x_positions, y_positions)
    plt.show() """

    time_array = []
    general_solutions = []
    y0 = [0,0,0,0,0,0,0]
    y = y0
    t = 0
    orientation = np.array([-1,0])
    track = get_track()
    for i in range (track[:, 0].size):

    
        if track[i][0] == 0:
            # go straight for the specified distance
            target_distance = track[i][1]
            solutions, times = straight(eco, y, orientation, target_distance, t)
            time_array += [element for sublist in times for element in sublist.tolist()]
            general_solutions += solutions
            y = solutions[-1][:, -1]
            t = times[-1][-1]
            
            #print(solutions, times)
        elif track[i][0] == 1:
            solutions, times = turning(eco, track[i][1], np.radians(track[i][2]), t, y)
            time_array += [element for sublist in times for element in sublist.tolist()]
            general_solutions += solutions
            y = solutions[-1][:, -1] 
            t = times[-1][-1]
            
    ys = [a for b in [k.T for k in general_solutions] for a in b]
    x_values = [c[0] for c in ys]
    y_values = [c[1] for c in ys]
    fuel_values = [c[6] for c in ys]

    plot(x_values, y_values)
    plot(time_array, fuel_values)
    plt.show()

def plot(x, y, title=None):
    plt.figure()
    plt.plot(x, y)
    if title is not None: 
        plt.title(title)

def straight(vehicle, y, initial_orientation, distance, t0):
    solution = []
    time = []
    distance_traveled = 0
    y0 = y
    initial_position = np.array([y0[0], y0[1]])

    
    
    def max_velocity(t, y, vehicle, initial_orientation, initial_position, distance):
        velocity = np.array([y[2], y[3]])
        speed = np.linalg.norm(velocity)
        return vehicle.maxSpeed - speed
    max_velocity.terminal=True

    def min_velocity(t, y, vehicle, initial_orientation, initial_position, distance):
        velocity = np.array([y[2], y[3]])
        speed = np.linalg.norm(velocity)
        return vehicle.minSpeed - speed
    min_velocity.terminal=True

    def reached(t, y, vehicle, initial_orientation, initial_position, distance):
        current_position = np.array([y[0], y[1]])
        distance_traveled = np.linalg.norm(current_position - initial_position)
        return (distance - distance_traveled)
    reached.terminal=True
    reached.direction= -1

    # start going straight
    while True:
        initial_velocity = np.array([y0[2], y0[3]])
        initial_speed = np.linalg.norm(initial_velocity)
        if initial_speed <= vehicle.minSpeed: # Burn
            new_solution = scipy.integrate.solve_ivp(dy_dt_straight_burning, [0, 500], y0, events=(max_velocity, reached), args=(vehicle, initial_orientation, initial_position, distance), max_step=50)
            print ("burning")
        else: # coast 
            new_solution = scipy.integrate.solve_ivp(dy_dt_straight_coasting, [0, 500], y0, events=(min_velocity, reached), args=(vehicle, initial_orientation, initial_position, distance), max_step=50)
            print ("coasting")
        # solution has terminated either because speed limits have been reached or because distance has been reached. 
        # Frist, append to global arrays 
        solution.append(new_solution.y)
        new_time = np.array(new_solution.t).astype(float)
        if len(time) == 0: 
            new_time = new_time + t0
        else:
            new_time = time[-1][-1] + new_time
        time.append(new_time)
        # check if it stopped because of distance 
        if not len(new_solution.y_events[1]) == 0: # i.e, reached occured
            return solution, time
        else:
            y0 = new_solution.y_events[0][0]


def turning(vehicle, radius, angle, t0, y):
    solution = []
    time = []
    distance_traveled = 0
    y0 = y
    initial_velocity = np.array([y[2],y[3]])
    initial_orientation = initial_velocity / np.linalg.norm(initial_velocity)
    initial_position = np.array([y0[0], y0[1]])

    def reached(t, y, vehicle, radius, angle, initial_orientation):
        velocity = np.array([y[2], y[3]])
        calculated_orientation = velocity / np.linalg.norm(velocity)
        angle_swept = np.arccos(np.dot(initial_orientation, calculated_orientation))
        return (angle - angle_swept)
    print(radius)
    reached.terminal=True
    reached.direction= -1

    new_solution = scipy.integrate.solve_ivp(dy_dt_turning, [0, 1000], y0, events=(reached), args=(vehicle, radius, angle, initial_orientation), max_step=3)
    solution.append(new_solution.y)
    new_time = np.array(new_solution.t).astype(float)
    new_time = new_time + t0
    time.append(new_time)
    # check if it stopped because of distance 
    # if not len(new_solution.y_events[0]) == 0: # i.e, reached occured
    return solution, time



    





