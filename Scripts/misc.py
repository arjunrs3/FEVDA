# accounts for other weight dependent resistances (i.e., Hub friction)
def get_misc_resistance(Vehicle): 
    return (Vehicle.misc_drag_coeff * Vehicle.total_weight)
