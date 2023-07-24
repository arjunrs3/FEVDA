import numpy as np
from Utils.helper_functions import *
from vehicle_setup import *
# Define a Theoretical Vehicle Along With Velocity

values = [45, 120, 110, .3,.1,.9, .0556, 0, 0, 20, 60, .426, .09, 15, 20]
eco = Vehicle(values)
nominal_rr_coefficient = .003

#Validating aero drag in relation to total tire drag for PAC Car
def aero_vs_tire_drag():

    camberRRdata = nominal_rr_coefficient / 0.00081 * np.array([[0, 4, 7, 10, 12, 14],[0.000832, 0.001, 0.00099, 0.00105, 0.0011, 0.0012]]) # data from Pac CAR scaled for Michelin Cross-Ply tires

    def get_straight_rolling_resistance(Vehicle):
        total_drag = 0 
        for wheel in Vehicle.wheels.values(): 
            total_drag = total_drag + np.cos((wheel.toe)) * wheel.fLongitudinal + np.sin((wheel.toe)) * wheel.cornering_stiffness * np.degrees(wheel.toe)
        return total_drag

    def get_RRcoeff(wheel, camber): 
        wheel.RRcoeff = np.interp(camber, camberRRdata[0], camberRRdata[1])

    def get_aerodynamic_drag(Vehicle, velocity): 
        rho = 1.293
        return (1/2 * rho * velocity ** 2 * Vehicle.drag_coeff * Vehicle.frontal_area)
    
    aero_drag = get_aerodynamic_drag(eco, 8.3)
    tire_drag = get_straight_rolling_resistance(eco)
    print(f"Aero Drag is {aero_drag} Newtons")
    print(f"Tire Drag is {tire_drag} Newtons") 
    print(f"Aero drag is {(aero_drag/(aero_drag + tire_drag)) * 100}%") 
    print(f"Tire Drag is {(tire_drag/(aero_drag + tire_drag))*100}%")

aero_vs_tire_drag()




