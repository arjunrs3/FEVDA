def get_aerodynamic_drag(Vehicle, velocity): 
    rho = 1.293
    return (1/2 * rho * velocity ** 2 * Vehicle.drag_coeff * Vehicle.frontal_area)
