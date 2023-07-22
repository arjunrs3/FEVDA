# Documentation
Code documentation for FEVDA, last updated 7/22/2023 
## Tire modeling 
### Files: 
- Scripts/tires.py
- Utils/helper_functions.py
### Inputs: 
- Turning radius (or None if straight)
- Vehicle Velocity
- Tire radius
- Cornering stiffnesses
- Rolling resistance coefficients
- Camber
- Toe
### Returns: 
- Longitudinal drag force on the tires (normal force is calculated during he timestepping procedure)
### Methodology: 
- Populate tire parameters:
  - get rolling resistance coefficient as a function of camber using helper_functions/get_RRcoeff
  - get cornering stiffnesses as a function of pressure using helper_functions/get_cornering_stiffness
  - get normal forces on each tire using helper_functions/get_base_normal
- If turning
  - Use tire parameters to solve the eight equations of Pacejka's magic formula (see func in tires/get_turning_values
  - return the longitudinal tire drag as found by the solution to these equations
  - currently, the centripetal force determines the tire force towards the center of the turn but it can also be extracted from this solution
- If going straight
  - Get the longitudinal drag on each tire using helper_functions/get_f_longitudinal
    - Simply the normal force multiplied by the rolling resistance coefficient
  - If there is any toe, the longitudinal force is scaled by the cosine of the toe angle, and the cornering stiffness is multiplied by the angle of turn
    - Assumes that the wheels with toe have the same drag as a wheel turning at the same sideslip angle.
### Assumptions: 
- No tire slip (will need to be validated later)
- no shifting of normal forces during turns (bicycle model combines the two front wheels into one effective front wheel)
- Pacejka's magic formula applicable for these types of tires (this is what PAC car used in their analysis)
## Aero modeling
### File: 
- Scripts/aero.py
### Inputs: 
- Coefficient of drag
- Frontal Area
- Vehicle Velocity
### Returns: 
- Aerodynamic drag force acting on the car
### Methodology: 
- uses definition of drag force to return 1/2 * rho * v ** 2 * Cd * frontal_area
## Engine modeling
### Files: 
- Scripts/engine.py
- Utils/helper_functions.py
### Inputs: 
- Torque Polynomial curve (csv file)
- Power Polynomial curve (csv file)
  - For the Honda GX50, webplotdigitizer was used to convert this image into csv files for the torque and power polynomials
    ![torque and power polynomials for the Honda GX 50](https://www.honda-engines-eu.com/files/images/1800x_/powercurve-gx50-big.jpg)
- BSFC (Brake specific fuel consumption)
- Fuel density
- Vehicle velocity
### Returns: 
- Engine force
- Volumetric fuel flow rate
### Methodology: 
- Obtains the engine RPM using the vehicle velocity and wheel RPM
- Get the propulsive force by obtaining the torque from the torque csv and propogating it through the drivetrain
- Get the operating power using the power csv
- Obtain volumetric flow rate by power * BSFC / fuel_density
### Assumptions: 
- No wheel slip (likely will need to be validated)
- Constant BSFC (likely a reasonable assumption)
- Engine RPM a function of wheel RPM (needs to be validated)
## Battery model 
Not yet implemented
## Mission modeling
