from Utils.helper_functions import create_units
Units = create_units()

def get_engine_rpm(Vehicle, velocity): 
    omega_wheel = velocity / (Vehicle.wheel_diameter / 2)
    omega_engine = omega_wheel / Vehicle.gear_ratio
    rpm = omega_engine * Units.radps
    if rpm < 2000: 
        rpm = 2000
    if rpm > 8000: 
        rpm = 8000
    return (rpm)

def get_propulsive_force(Vehicle, velocity): 
    rpm = get_engine_rpm(Vehicle, velocity)
    torque = Vehicle.powerplant.torque_polynomial(rpm)
    power = Vehicle.powerplant.power_polynomial(rpm)
    fPropulsive = torque / (0.5 * Vehicle.wheel_diameter) / Vehicle.gear_ratio * 1
    return fPropulsive

def get_volumetric_fuel_rate(Vehicle, velocity): 
    rpm = get_engine_rpm(Vehicle, velocity)
    torque = Vehicle.powerplant.torque_polynomial(rpm)
    power = Vehicle.powerplant.power_polynomial(rpm)
    volumetric_fuel_rate = power * Vehicle.powerplant.BSFC / (Vehicle.powerplant.fuel_density * 1 * 10 ** -6) 
    return volumetric_fuel_rate # ml / s
