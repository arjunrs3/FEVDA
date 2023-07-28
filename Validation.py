import numpy as np
import matplotlib.pyplot as plt
from Utils.helper_functions import *
from vehicle_setup import *
# Define a Theoretical Vehicle Along With Velocity

eco1_values = [45, 176.37, 0, .3,.1,.9, .0556, 0, 0, 19.685, 87.0226, .426, .09, 15, 20]
eco1 = Vehicle(eco1_values)
eco2_values = [40, 165.347, 0, .3,.1,.9, .0556, 0, 0, 19.685, 87.0226, .426, .09, 15, 20] 
eco2 = Vehicle(eco2_values)



def get_straight_rolling_resistance1(Vehicle):
    total_drag = 0 
    cornering_stiffness = 100
    for wheel in Vehicle.wheels.values(): 
        total_drag = total_drag + np.cos((wheel.toe)) * wheel.fLongitudinal + np.sin((wheel.toe)) * cornering_stiffness * np.degrees(wheel.toe)
    return total_drag


def get_aerodynamic_drag(Vehicle, velocity): 
    rho = 1.2
    return (1/2 * rho * velocity ** 2 * Vehicle.drag_coeff * Vehicle.frontal_area)

def get_turning_values1(Vehicle, velocity, radius): 
    R = radius
    Xg = Vehicle.COG[0]
    Fc = Vehicle.total_mass * velocity ** 2 / R #centripetal contribution
    L = Vehicle.wheelbase
    Cf = 100# (Vehicle.frontl.cornering_stiffness_turning + Vehicle.frontr.cornering_stiffness_turning) / 2
    Cr = 100#Vehicle.rear.cornering_stiffness
    Fxf = Vehicle.frontl.fLongitudinal + Vehicle.frontr.fLongitudinal # combined for bicycle problem
    Fxr = Vehicle.rear.fLongitudinal

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
    delta = turning_values[0]
    alphaf = turning_values[1]
    alphar = turning_values[2]
    beta = turning_values[3]
    e = turning_values[4]
    fflateral = turning_values[5]
    rflateral = turning_values[6]
    T = turning_values[7]
    return(T, Fc, beta)

#Validating aero drag in relation to total tire drag for PAC Car

def aero_vs_tire_drag():
    aero_drag = get_aerodynamic_drag(eco1, 8.3)
    tire_drag = get_straight_rolling_resistance1(eco1)
    print(f"Aero Drag is {aero_drag} Newtons")
    print(f"Tire Drag is {tire_drag} Newtons") 
    print(f"Aero drag is {(aero_drag/(aero_drag + tire_drag)) * 100}% of total drag") 
    print(f"Tire Drag is {(tire_drag/(aero_drag + tire_drag))*100}% of total drag")
    print("---------------")


def aero_vs_tire_drag_while_cornering():
    aero_drag = get_aerodynamic_drag(eco1, 8.3)
    straight_drag = get_straight_rolling_resistance1(eco1)
    turning_drag = get_turning_values1(eco1, 8.3, 40)[0]
    print(f"Aero Drag is {aero_drag} Newtons")
    print(f"Tire Drag is {turning_drag} Newtons") 
    print(f"Aero drag is {(aero_drag/(aero_drag + turning_drag)) * 100}% of total drag while cornering") 
    print(f"Tire Drag is {(turning_drag/(aero_drag + turning_drag))*100}% of total drag while cornering")
    print("---------------")

def tire_drag_vs_toe_angle_straight():
    x_values = []
    y_values = []
    cornering_stiffness = 100
    def get_straight_rolling_resistance2(Vehicle, toe):
        total_drag = 0 
        for tag, wheel in Vehicle.wheels.items():
            if tag == "rear":
                total_drag += wheel.fLongitudinal
            else:
                total_drag = total_drag + np.cos((toe)) * wheel.fLongitudinal + np.sin((toe)) * wheel.cornering_stiffness * np.degrees(toe) 
        return total_drag

# Iterate through the decimal values with the specified step size

    start_value = 0
    end_value = .3
    step_size = 0.05
    values = np.arange(start_value, end_value + step_size, step_size)

    for value in values:
        toe = np.radians(value)
        x_values.append(value)
        tire_drag = get_straight_rolling_resistance2(eco2, toe)
        y_values.append(tire_drag)
    plt.figure(1)
    plt.plot(x_values, y_values, linestyle='-', color='blue', marker='o', linewidth=2)
    plt.xlabel('Toe Angle (Degrees)')
    plt.ylabel('Tire Drag (Newtons)')
    plt.title('Toe Angle vs Tire Drag')
    

def tire_drag_vs_turn_radius_with_velocity():
    kvelocity = [15,20,25,30,35,40]
    velocities = [4.16667,5.55556,6.94444,8.33333,9.72222,11.1111] #m/s conversions from 15,20,25,30,35,40 km/hr
    turning_radius=range(20,110,1)
    color = ["blue","black","green", "red", "orange", "teal"]
    
    

    for velocity in velocities:
        tire_drag=[]
        for radii in turning_radius:
            tire_drag.append(get_turning_values(eco2,velocity,radii)[0])
        plt.figure(2)
        plt.plot(turning_radius, tire_drag, linestyle='-', color=color[velocities.index(velocity)], linewidth=2,label=(kvelocity[velocities.index(velocity)], "km/hr"))
    plt.xlabel('Turning Radius (Meters)')
    plt.ylabel('Tire Drag (Newtons)')
    plt.title('Toe Angle vs Tire Drag')
    plt.legend()
    plt.show()



aero_vs_tire_drag()
aero_vs_tire_drag_while_cornering()
tire_drag_vs_toe_angle_straight()
tire_drag_vs_turn_radius_with_velocity()




