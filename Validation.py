import numpy as np
import matplotlib.pyplot as plt
from Utils.helper_functions import *
from vehicle_setup import *
from Scripts.aero import *
# Define two vehicles for two validation experiments provided by Pac CAR
#COG-position, vehicle mass, driver mass, frontal area, drag coefficient, drivetrain efficiency, gear ratio,toe, camber, wheel diameter, pressure, Average BSFC, Inertia, Lower Speed Limit, Upper Speed Limit
eco1_values = [45, 176.37, 0, .3,.1,.9, .0556, 0, 0, 19.685, 87.0226, .426, .09, 15, 20]
eco1 = Vehicle(eco1_values)
eco2_values = [40, 165.347, 0, .3,.1,.9, .0556, 0, 0, 19.685, 87.0226, .426, .09, 15, 20] 
eco2 = Vehicle(eco2_values)
#Rolling resistance coefficient and camber data is hardcoded in regular simulation; it is redefined here in accordance with Pad CAR validation data
nominal_RR1 = .003
camberRRdata1 = nominal_RR1/.00081 * np.array([[0, 4, 7, 10, 12, 14],[0.000832, 0.001, 0.00099, 0.00105, 0.0011, 0.0012]]) # data from Pac CAR scaled for Michelin Cross-Ply tires
nominal_RR2 = .00081
camberRRdata2 = nominal_RR2/.00081 * np.array([[0, 4, 7, 10, 12, 14],[0.000832, 0.001, 0.00099, 0.00105, 0.0011, 0.0012]]) # data from Pac CAR scaled for Michelin Cross-Ply tires

#manually redefine the rolling ressitance coefficient, longitudinal forces, and conering stiffness per Pac CAR validation parameters
for wheel in eco1.wheels.values(): 
    get_RRcoeff(wheel, wheel.camber,camberRRdata1)
    wheel.fLongitudinal = wheel.RRcoeff * wheel.fNormal
    wheel.cornering_stiffness = 100
    wheel.cornering_stiffness_turning = 100

for wheel in eco2.wheels.values():
    get_RRcoeff(wheel, wheel.camber,camberRRdata2)
    wheel.fLongitudinal = wheel.RRcoeff * wheel.fNormal
    wheel.cornering_stiffness = 100
    wheel.cornering_stiffness_turning = 100

#Validating aero drag in relation to total tire drag for Pac CAR while traveling in a straight line

def aero_vs_tire_drag():
    aero_drag = get_aerodynamic_drag(eco1, 8.3)
    tire_drag = get_straight_rolling_resistance(eco1)
    print(f"Aero Drag is {aero_drag} Newtons")
    print(f"Tire Drag is {tire_drag} Newtons") 
    print(f"Aero drag is {(aero_drag/(aero_drag + tire_drag)) * 100}% of total drag") 
    print(f"Tire Drag is {(tire_drag/(aero_drag + tire_drag))*100}% of total drag")
    print("---------------")

#Validating aero drag in relation to total tire drag for Pac CAR while cornering
def aero_vs_tire_drag_while_cornering():
    aero_drag = get_aerodynamic_drag(eco1, 8.3)
    straight_drag = get_straight_rolling_resistance(eco1)
    turning_drag = get_turning_values(eco1, 8.3, 40)[0]
    print(f"Aero Drag is {aero_drag} Newtons")
    print(f"Tire Drag is {turning_drag} Newtons") 
    print(f"Aero drag is {(aero_drag/(aero_drag + turning_drag)) * 100}% of total drag while cornering") 
    print(f"Tire Drag is {(turning_drag/(aero_drag + turning_drag))*100}% of total drag while cornering")
    print("---------------")

#Validating tire drag as toe angle is changed while traveling straight for Pac CAR
def tire_drag_vs_toe_angle_straight():
    x_values = []
    y_values = []
    cornering_stiffness = 100

# Iterate through the decimal values with the specified step size

    start_value = 0
    end_value = .3
    step_size = 0.05
    values = np.arange(start_value, end_value + step_size, step_size)

    for value in values:
        eco2.frontl.toe= np.radians(value)
        eco2.frontr.toe = np.radians(value)
        x_values.append(value)
        tire_drag = get_straight_rolling_resistance(eco2)
        y_values.append(tire_drag)
    plt.figure(1)
    plt.plot(x_values, y_values, linestyle='-', color='blue', marker='o', linewidth=2)
    plt.xlabel('Toe Angle (Degrees)')
    plt.ylabel('Tire Drag (Newtons)')
    plt.title('Toe Angle vs Tire Drag')
    
#Validating tire drag at various turn radii for discretized velocity set against Pac CAR
def tire_drag_vs_turn_radius_with_velocity():
    
    kmvelocity = [15,20,25,30,35,40]
    velocities = [4.16667,5.55556,6.94444,8.33333,9.72222,11.1111] #m/s conversions from 15,20,25,30,35,40 km/hr
    turning_radius=range(20,110,1)
    color = ["blue","black","green", "red", "orange", "teal"]
    
    

    for velocity in velocities:
        tire_drag=[]
        for radii in turning_radius:
            tire_drag.append(get_turning_values(eco2,velocity,radii)[0])
        plt.figure(2)
        plt.plot(turning_radius, tire_drag, linestyle='-', color=color[velocities.index(velocity)], linewidth=2,label=(kmvelocity[velocities.index(velocity)], "km/hr"))
    plt.xlabel('Turning Radius (Meters)')
    plt.ylabel('Tire Drag (Newtons)')
    plt.title('Toe Angle vs Tire Drag')
    plt.legend()
    plt.show()



aero_vs_tire_drag()
aero_vs_tire_drag_while_cornering()
tire_drag_vs_toe_angle_straight()
tire_drag_vs_turn_radius_with_velocity()




